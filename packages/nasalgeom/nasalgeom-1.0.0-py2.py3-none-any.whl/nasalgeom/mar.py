# --------------------------------------------------------------------------
#
#    Copyright 2016 Jose Luis Cercos-Pita
#
#    This file is part of NASAL-GEOM.
#
#    NASAL-GEOM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    NASAL-GEOM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------

import os
import multiprocessing
import threading
import time
import numpy as np
import vtk
from scipy import ndimage, interpolate, misc
from skimage.transform import radon, iradon, iradon_sart
from .denoise import _gaussian
from .segmentation import _watershed
from . import helpers


HU_AIR = -1000
HU_TISSUE = 0
HU_BONE = 3000
HU_METAL = 6000  # To be eventually modified by mar function


def prior_image(img, sigma=3):
    """Generate the so called prior image, also known as synthetic image, used
    to carry out the NMAR or the AMAR algorithms.

    To obtain such prior image, first the image is denoise using edge-preserving
    noise removal techniques, followed by an image segmentation.

    Parameters
    ----------
    img : 2d np.ndarray
        Image that should be converted
    sigma : int
        Window size to perform the edge preserving noise removal

    Returns
    -------
    pimg : 2d np.ndarray
        Resulting prior image
    """
    # Denoise the image
    img = _gaussian(ndimage.filters.median_filter(img, size=sigma), size=sigma)

    # Set the constant air value
    pimg = np.copy(img)
    mask = img < 0.5 * (HU_AIR + HU_TISSUE)
    pimg[mask] = HU_AIR
    # Set the constant tissue value
    mask = np.logical_and(np.logical_not(mask),
                          img < HU_BONE)
    pimg[mask] = HU_TISSUE
    # And the bones
    mask = img >= HU_BONE 
    pimg[mask] = HU_TISSUE

    return pimg


class MarThread(threading.Thread):
    """Perform a traditional Metal Artifact Reduction (MAR) in a specific slice.
    This class is used to carry out the job in parallel
    """
    def __init__(self, img, s, thetas, mask, dbg=False):
        """Initialize the tool

        Parameters
        ----------
        img : 3d np.ndarray
            Image to become corrected (it is overwritten)
        s : int
            Slice of the image to become corrected
        thetas : list
            List of projection angles
        mask : 2d np.ndarray
            Already computed metal body mask
        dbg : bool
            True if the temporal images should be saved for debug purposes,
            False otherwise
        """
        threading.Thread.__init__(self)
        self.img = img
        self.s = s
        self.thetas = thetas
        self.mask = mask
        self.dbg = dbg

    def inpaint(self, img, mask, direction=None):
        """Inpaint the masked area of the sinogram by linear interpolation
        """
        # get a subset of the image surrounding the metal bodies
        orig = np.logical_and(
            np.logical_not(mask),
            ndimage.binary_dilation(mask,
                                    ndimage.generate_binary_structure(2, 2),
                                    iterations=5))
        if direction is None:
            # Bilinear interpolation
            inpaint = interpolate.griddata(np.where(orig),
                                           img[orig],
                                           np.where(mask),
                                           'linear')
            img[np.where(mask)] = inpaint
            return img
        # Linear interpolation along x/y direction
        axis = 0 if direction == 'v' else 1
        for i in range(img.shape[axis]):
            slc = [slice(None)] * len(img.shape)
            slc[axis] = i
            interp_mask = np.where(mask[slc])[0]
            img_mask = np.where(orig[slc])[0]
            img[slc][interp_mask] = np.interp(interp_mask,
                                              img_mask,
                                              img[slc][img_mask])
        return img

    def mar(self):
        """Traditional Metal Artifact Reduction (MAR). MAR is based in the
        following steps:
            1.- The metal body is extracted from the original image. Here this
                is an input (self.mask)
            2.- The sinograms are computed both, for the original image and the
                metal body mask
            3.- The sinogram of the original image is inpainted along the pixels
                signaled by the sinogram of the metal body mask
            4.- The corrected sinogram is projected back
            5.- The metal body is restored

        Returns
        -------
        img_iradon : 2d np.ndarray
            Corrected image
        img_sino : 2d np.ndarray
            Sinogram of the original image
        mask_sino : 2d np.ndarray
            Sinogram of the metal body mask
        sino : 2d np.ndarray
            Sinogram of the corrected image
        """
        s = self.s
        img = np.copy(self.img[:, :, s])
        thetas = self.thetas
        mask = self.mask
        # Dilate the metal body a bit
        """
        mask = ndimage.binary_dilation(mask,
                                       ndimage.generate_binary_structure(2, 2),
                                       iterations=1)
        """
        # Get the sinograms of the image and metal body mask
        img_sino = radon(img, theta=thetas, circle=False)
        mask_sino = radon(mask, theta=thetas, circle=False) >= 1
        """
        mask_sino = ndimage.binary_dilation(
            mask_sino, ndimage.generate_binary_structure(2, 2), iterations=1)
        """
        # Inpaint the sinogram of the image along the mask
        if np.any(mask_sino):
            # sino = inpaint_biharmonic(img_sino, mask_sino)
            # sino = inpaint.inpaint(np.copy(img_sino), mask_sino)
            sino = self.inpaint(np.copy(img_sino), mask_sino)
        # Revert back the Radon transform
        img_iradon = iradon(sino, theta=thetas, circle=False)
        if img_iradon.shape[0] > img.shape[0]:
            S = img_iradon.shape[0]
            s = img.shape[0]
            img_iradon = img_iradon[(S - s) // 2:(S + s) // 2,:]
        if img_iradon.shape[1] > img.shape[1]:
            S = img_iradon.shape[1]
            s = img.shape[1]
            img_iradon = img_iradon[:,(S - s) // 2:(S + s) // 2]
        # Restore the metal body
        # img_iradon[np.where(mask)] = img[np.where(mask)]
        img_iradon[np.where(mask)] = HU_BONE

        # Save debug snapshots
        if not self.dbg:
            return img_iradon, img_sino, mask_sino, sino
        misc.toimage(mask.transpose(1,0)[::-1, :], cmin=0, cmax=1).save(
            'DBG_001_MAR/{:04d}_mask.png'.format(s))
        misc.toimage(img_sino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_img_sino.png'.format(s))
        misc.toimage(mask_sino.transpose(1,0)[::-1, :], cmin=0, cmax=1).save(
            'DBG_001_MAR/{:04d}_mask_sino.png'.format(s))
        misc.toimage(sino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_sino.png'.format(s))
        misc.toimage(img_iradon.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_mar.png'.format(s))
        return img_iradon, img_sino, mask_sino, sino

    def run(self):
        """Just simply relegate the work on the MAR function (similar to an
        abstract method).
        """
        self.img[:, :, self.s], _, _, _ = self.mar()


class NMarThread(MarThread):
    """Perform a Normalized Metal Artifact Reduction (NMAR) in a specific slice.
    This class is used to carry out the job in parallel

    See:
    Esther Meyer, Rainer Raupach, Michael Lell, Bernhard Schmidt, Marc
    Kachelrie. Normalized Metal Artifact Reduction (NMAR) in Computed
    Tomography. Medical Physics 37, 2010.
    """
    def __init__(self, img, s, thetas, mask, dbg=False):
        """Initialize the tool

        Parameters
        ----------
        img : 3d np.ndarray
            Image to become corrected (it is overwritten)
        s : int
            Slice of the image to become corrected
        thetas : list
            List of projection angles
        mask : 2d np.ndarray
            Already computed metal body mask
        dbg : bool
            True if the temporal images should be saved for debug purposes,
            False otherwise
        """
        MarThread.__init__(self, img, s, thetas, mask, dbg=dbg)
        self.epsilon = 1

    def nmar(self, img, sino, sino_mask):
        """Adaptative Metal Artifact Reduction (NMAR) step.

        Parameters
        ----------
        img : 2d np.ndarray
            Image already corrected by a MAR algortihm
        sino : 2d np.ndarray
            Sinogram of the original image (not img)
        sino_mask : 2d np.ndarray
            Sinogram of the metal mask

        Returns
        -------
        nimg : 2d np.ndarray
            Corrected image
        sino : 2d np.ndarray
            Sinogram of the original image
        amask : 2d np.ndarray
            Sinogram of the correction area mask
        nsino : 2d np.ndarray
            Corrected image sinogram
        """
        thetas = self.thetas
        mask = self.mask
        s = self.s
        orig = self.img[:, :, s]

        # Get the prior/synthetic image
        pimg = prior_image(img)
        # Build the prior/systhetic sinogram
        psino = radon(pimg, theta=thetas, circle=False)
        # renormalize the original sinogram
        psino[np.where(np.abs(psino) <= self.epsilon)] = self.epsilon
        nsino = sino - psino

        # Adapt the mask depending on the gradient. Only the gradient blocks
        # matching with the original sinogram will be kept. However, the
        # watershed alkgorithm consider valid growing blocks in the vertical and
        # the horizontal directions, while we only want to consider horizontal
        # connections. Alonf this line, we are hacking the watershed just
        # spliting the mask in odds and even rows, such that the watershed
        # algorithm cannot grow in the vertical direction
        """
        gmask = 2 * np.abs(ndimage.gaussian_filter(ndimage.sobel(nsino, 0),
                                                    sigma=1)) > 1.0
        gmask1 = np.copy(gmask)
        gmask1[:,::2] = 0
        gmask2 = gmask - gmask1
        gmask1 = _watershed(gmask1,
                            (1.0, None),
                            sino_mask)
        gmask2 = _watershed(gmask2,
                            (1.0, None),
                            sino_mask)
        gmask = gmask1 + gmask2

        amask = ndimage.binary_dilation(
            np.logical_or(sino_mask, gmask),
            ndimage.generate_binary_structure(2, 2),
            iterations=1).astype(np.float)
        """
        amask = sino_mask

        # Inpaint the sinogram of the image along the mask
        if np.any(amask):
            # nsino = self.inpaint(nsino, amask, direction = 'h')
            nsino = self.inpaint(nsino, amask)
            nsino = ndimage.gaussian_filter(nsino, sigma=1)

        # Denormalize the sinogram. To avoid restoring high luminosity
        # artifacts, we can create the prior image sinogram image again, but
        # This time we can limit the top values
        nsino = nsino + psino
        # Revert back the Radon transform
        nimg = iradon(nsino, theta=thetas, circle=False)
        if nimg.shape[0] > orig.shape[0]:
            S = nimg.shape[0]
            s = orig.shape[0]
            nimg = nimg[(S - s) // 2:(S + s) // 2,:]
        if nimg.shape[1] > img.shape[1]:
            S = nimg.shape[1]
            s = orig.shape[1]
            nimg = nimg[:,(S - s) // 2:(S + s) // 2]
        # Restore the metal body (as bone)
        nimg[np.where(mask)] = HU_BONE

        # Save debug snapshots
        if not self.dbg:
            return nimg, sino, amask, nsino
        misc.toimage(pimg.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it0_0prior.png'.format(s))
        misc.toimage(psino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_it0_1psino.png'.format(s))
        misc.toimage(amask.astype(np.float).transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_it0_2amask.png'.format(s))
        misc.toimage(nsino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_it0_3nsino.png'.format(s))
        misc.toimage(nimg.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it0_4nimg.png'.format(s))

        return nimg, sino, amask, nsino

    def run(self):
        """Carry out the NMAR using a conventional MAR to setup the prior image
        (some sort of guide to make the sinogrqam more homogeneous).
        """
        s = self.s

        # Make a traditional MAR correction
        mar_img, sino, mask_sino, _ = self.mar()

        # Make normalized MAR correction on top of that
        mar_img, _, _, _ = self.nmar(mar_img, sino, mask_sino)

        self.img[:, :, self.s] = mar_img


class AMarThread(NMarThread):
    """Perform an Adaptative Metal Artifact Reduction (AMAR) in a specific slice.
    This class is used to carry out the job in parallel

    See:
    Koehler, Thomas, Bernhard Brendel, and Kevin M. Brown. A New Method for
    Metal Artifact Reduction in CT. In The Second International Conference on
    Image Formation in X-Ray Computed Tomography, 29--32, 2012.
    """
    def __init__(self, img, s, thetas, mask, dbg=False):
        """Initialize the tool

        Parameters
        ----------
        img : 3d np.ndarray
            Image to become corrected (it is overwritten)
        s : int
            Slice of the image to become corrected
        thetas : list
            List of projection angles
        mask : 2d np.ndarray
            Already computed metal body mask
        dbg : bool
            True if the temporal images should be saved for debug purposes,
            False otherwise
        """
        NMarThread.__init__(self, img, s, thetas, mask, dbg=dbg)
        self.iterations = 2
        self.it = 0

    def amar(self, img, sino, sino_mask):
        """Adaptative Metal Artifact Reduction (AMAR) step.

        Parameters
        ----------
        img : 2d np.ndarray
            Image already corrected by a MAR algortihm
        sino : 2d np.ndarray
            Sinogram of the original image (not img)
        sino_mask : 2d np.ndarray
            Sinogram of the metal mask

        Returns
        -------
        aimg : 2d np.ndarray
            Corrected image
        sino : 2d np.ndarray
            Sinogram of the original image
        sino_mask : 2d np.ndarray
            Sinogram of the metal body mask
        csino : 2d np.ndarray
            Correction sinogram
        """
        thetas = self.thetas
        mask = self.mask
        s = self.s
        orig = self.img[:, :, s]

        # Get the prior/synthetic image
        pimg = prior_image(img)
        pimg[np.where(mask)] = HU_METAL
        # Build the prior/systhetic sinogram
        psino = radon(pimg, theta=thetas, circle=False)
        # Get the error sinogram
        esino = sino - psino
        # Smooth the mask sinogram
        msino = ndimage.binary_dilation(sino_mask,
                                        ndimage.generate_binary_structure(2, 2),
                                        iterations=1).astype(np.float)
        msino = ndimage.gaussian_filter(msino, 5)
        # So we can compute the correction sinogram and image
        csino = esino * msino
        cimg = iradon(csino, theta=thetas, circle=False)
        # And finally correct the original image
        aimg = orig - cimg

        # Save debug snapshots
        if not self.dbg:
            return aimg, sino, sino_mask, csino
        misc.toimage(pimg.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it{}_0prior.png'.format(s, self.it + 1))
        misc.toimage(psino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_it{}_1psino.png'.format(s, self.it + 1))
        misc.toimage(esino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_it{}_2esino.png'.format(s, self.it + 1))
        misc.toimage(msino.transpose(1,0)[::-1, :], cmin=0, cmax=1).save(
            'DBG_001_MAR/{:04d}_it{}_3msino.png'.format(s, self.it + 1))
        misc.toimage(csino.transpose(1,0)[::-1, :]).save(
            'DBG_001_MAR/{:04d}_it{}_4csino.png'.format(s, self.it + 1))
        misc.toimage(cimg.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it{}_4cimg.png'.format(s, self.it + 1))
        misc.toimage(aimg.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it{}_5amar.png'.format(s, self.it + 1))

        return aimg, sino, sino_mask, csino

    def run(self):
        """Just simply relegate the work on the MAR function (similaqr to an
        abstract method).
        """
        s = self.s

        # Make a traditional MAR correction
        mar_img, sino, mask_sino, _ = self.mar()

        # Make normalized MAR correction
        mar_img, sino, mask_sino, _ = self.nmar(mar_img, sino, mask_sino)

        # Make adaptative MAR correction
        for self.it in range(self.iterations):
            mar_img, _, _, _ = self.amar(mar_img, sino, mask_sino)

        self.img[:, :, self.s] = mar_img


class FSMarThread(NMarThread):
    """Perform a Frequency Split Metal Artifact Reduction (FSMAR), on top of a
    Normalize Metal Artifact Reduction (NMAR), in a specific slice.
    This class is used to carry out the job in parallel

    See:
    Esther Meyer, Rainer Raupach, Michael Lell, Bernhard Schmidt, Marc
    Kachelrie. Frequency split metal artifact reduction (FSMAR) in computed
    tomography. Medical Physics 39, 2012.
    """
    def __init__(self, img, s, thetas, mask, spacing, dbg=False):
        """Initialize the tool

        Parameters
        ----------
        img : 3d np.ndarray
            Image to become corrected (it is overwritten)
        s : int
            Slice of the image to become corrected
        thetas : list
            List of projection angles
        mask : 2d np.ndarray
            Already computed metal body mask
        spacing : np.array
            Spacing between pixels [m]
        dbg : bool
            True if the temporal images should be saved for debug purposes,
            False otherwise
        """
        NMarThread.__init__(self, img, s, thetas, mask, dbg=dbg)
        self.spacing = spacing
        self.epsilon = 1

    def fsmar(self, mar, sigma=3/2.355):
        """Adaptative Metal Artifact Reduction (NMAR) step.

        Parameters
        ----------
        mar : 2d np.ndarray
            NMAR corrected image
        sigma : float
            Gaussian filter sigma function (i.e. it is later multiplied by the
            image spacing [cm])

        Returns
        -------
        fsimg : 2d np.ndarray
            Frequency split image
        """
        mask = self.mask
        s = self.s
        img = np.copy(self.img[:, :, s])
        sigmas = sigma * 100 * self.spacing[:2]  # Discard data along z
        sigmas = np.asarray(
            [max(sigma, sigma * 100 * self.spacing[i]) for i in range(2)])

        # Get the low frequency images
        img_lo = ndimage.gaussian_filter(img, sigmas)
        mar_lo = ndimage.gaussian_filter(mar, sigmas)

        # Get the high frequency image just simply substracting them
        img_hi = img - img_lo
        mar_hi = mar - mar_lo

        # Get the spatial kernel to filter out the NMAR results
        W = ndimage.gaussian_filter(mask.astype(np.float), 10 * sigmas)
        W /= np.max(W)

        # Compute the frequency split image
        fsimg = mar_lo + W * img_hi + (1.0 - W) * mar_hi

        # Save debug snapshots
        if not self.dbg:
            return fsimg
        misc.toimage(img_lo.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it1_0img_lo.png'.format(s))
        misc.toimage(mar_lo.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it1_1mar_lo.png'.format(s))
        misc.toimage(img_hi.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it1_2img_hi.png'.format(s))
        misc.toimage(mar_hi.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it1_3mar_hi.png'.format(s))
        misc.toimage(W.transpose(1,0)[::-1, :], cmin=0, cmax=1).save(
            'DBG_001_MAR/{:04d}_it1_4W.png'.format(s))
        misc.toimage(fsimg.transpose(1,0)[::-1, :], cmin=-1000, cmax=1000).save(
            'DBG_001_MAR/{:04d}_it1_5fsimg.png'.format(s))

        return fsimg

    def run(self):
        """Create a NMAR corrected image, and then use the low frequency of such
        image, and a combination of the high frequencies of the original and the
        corrected image. More specifically, close to the metal body the high
        freq components of the original image are used, while far away the
        corrected image is chosen
        """
        s = self.s

        # Make a NMAR correction
        mar_img, sino, mask_sino, _ = self.mar()
        mar_img, _, _, _ = self.nmar(mar_img, sino, mask_sino)

        # Make the frequency split
        self.img[:, :, self.s] = self.fsmar(mar_img)


def __smooth(img_orig, img_mar, sigma=5.0):
    """Smooth the image in the most affected areas to reduce the noise bad
    effects on the Laplacian edge detector.

    Parameters
    ----------
    img_orig : np.ndarray
        Original 3D image
    img_mar : np.ndarray
        MAR corrected 3D image

    Returns
    -------
    img : np.ndarray
        Smoothed 3D image
    """
    # Get the smoothing weights
    w = np.abs(img_orig - img_mar) / 750.0
    w[w > 1.0] = 1.0
    # Carry out the 2D slices based smooth filter
    for s in range(img_orig.shape[2]):
        if not np.any(w[:,:,s]):
            # This slice was not affected by MAR
            continue
        # Smooth the weights image, as well as the MAR corrected image
        w[:,:,s] = ndimage.gaussian_filter(w[:,:,s], sigma)
        img = ndimage.gaussian_filter(img_mar[:,:,s], sigma)
        # Make a weighted interpolation between the corrected and the
        # uncorrected images
        img_mar[:,:,s] = w[:,:,s] * img + (1.0 - w[:,:,s]) * img_mar[:,:,s]

    return img_mar


def __gamma_correction(img_orig, img_mar, thresholds):
    """Perform an adaptative limunosity/radiosity correction to restore the
    lost energy due to the metal body removal.

    Parameters
    ----------
    img_orig : np.ndarray
        Original 3D image
    img_mar : np.ndarray
        MAR corrected 3D image
    thersholds : [air, tissue]
        Selected thresholds

    Returns
    -------
    img : np.ndarray
        Corrected 3D image
    """
    # Get a renormalized image
    cmin = thresholds[0]
    cmax = thresholds[1]
    img_unclamp = (np.copy(img_mar.astype(np.float)) - cmin) / (cmax - cmin)
    img = np.copy(img_unclamp)
    img[img > 1.0] = 1.0
    img[img < 0.0] = 0.0

    # Compute the radiosity curve, and list the affected images
    radiosity = np.mean(img, axis=(0,1))
    affected = np.any(img_orig - img_mar, axis=(0,1))

    # Get the radiosity targets
    if np.all(affected):
        # Everything is affected by metal
        target = [np.mean(img)] * img.shape[2]
    else:
        target = np.copy(radiosity)
        inpaint = interpolate.griddata(np.where(np.logical_not(affected)),
                                       radiosity[np.logical_not(affected)],
                                       np.where(affected),
                                       'nearest')
        target[np.where(affected)] = inpaint

    # Unfortunately, the non-linear application can not be precalculated, so we
    # should iteratively look for the best new tissue threshold for each slice
    for s in range(img.shape[2]):
        if not affected[s]:
            continue
        img_slc = np.copy(img[:,:,s].astype(np.float))
        rad_slc = target[s]
        # Get the error for several gamma values
        tissues = np.linspace(0.5, 1.0, num=11)[::-1]
        errors = np.empty(tissues.shape, dtype=np.float)
        for i,tissue in enumerate(tissues):
            img_slc[img_slc > tissue] = 1.0
            errors[i] = np.abs(np.mean(img_slc) - rad_slc)
        # Get the best threshold value, and perform the new renormalization
        tissue = tissues[np.argmin(errors)]
        img[:,:,s][img[:,:,s] > tissue] = 1.0

    # Restore the unclamped values, i.e. those outside the air-tissue interval
    mask = np.logical_or(img_unclamp < 0.0, img_unclamp > 1.0)
    img[mask] = img_unclamp[mask]

    # Restore the original levels
    img = img * (cmax - cmin) + cmin
    return img.astype(img_mar.dtype)


def __eyes_protector(img, metal_thresholds, thresholds, remove_small_bodies):
    """Detects and returns a mask eventually containing the eyes protector.
    Eyes protectors are dense bodies designed to reduce the radiation received
    by the eyes. They are therefore big bodies which generates tiny metal
    artifacts, and therefore the MAR should not be applied to them.
    
    This method detects such bodies, and return a mask identifying it.
    
    Parameters
    ----------
    img : np.ndarray
        Original 3D image
    metal_thresholds : [min, max]
        Threshold values to consider a voxel as a metal body
    thresholds : [air, tissue]
        Air and tissue selected threshold values
    remove_small_bodies: bool
        Should the small metal bodies neglected?

    Returns
    -------
    mask : np.ndarray
        Mask of the eyes protector body.
    """
    # Get the best aproximation as possible of the head size
    x, _, _ = np.where(img >= thresholds[1])
    DX = np.max(x) - np.min(x)
    # Get the mask of all the metal bodies
    metal_mask = np.logical_or(img >= metal_thresholds[1],
                               img <= metal_thresholds[0]).astype(np.int)
    if remove_small_bodies:
        metal_mask = np.logical_and(metal_mask,
            ndimage.binary_dilation(ndimage.binary_erosion(
                metal_mask, iterations=1), iterations=1))
    metal_mask = ndimage.binary_dilation(metal_mask, iterations=3)
    # Labelize the bodies, to analyze them one by one
    labels, n = ndimage.label(metal_mask, structure=None)
    xsize = 0
    label = -1
    for l in range(1, n + 1):
        # Look for long bodies in the x direction
        x, _, _ = np.where(labels == l)
        dx = np.max(x) - np.min(x)
        if dx < 0.65 * DX:
            continue
        # Check if there are a better candidate
        if dx < xsize:
            continue
        # Pick this body
        label = l
        xsize = dx

    return labels == label

def mar(vtk_img, args):
    """Performs a Metal Artifact Reduction, based on a Radon transform and a
    biharmonic inpaint. The process can be summarized as follows:

    1.- A threshold operation is carried out to find the metal body
    2.- A radon transform is applied to the original image and the metal body,
        in order to get the sinogram, and the metal mask
    3.- The sinogram is inpainted along the mask
    4.- The radon transform is inverted to obtain the corrected image

    Parameters
    ----------
    vtk_img : vtk.vtkImageData
        VTK image to become filtered. It will be overwritten
    args : dict
        Program arguments

    Returns
    -------
    output : vtk.vtkImageData
        Modified VTK image
    """
    print('Metal Artifact Reduction...')
    threads = args.threads or multiprocessing.cpu_count()
    if threads < 1:
        threads = 1
    img = helpers.vtkImageToNumPy(vtk_img)
    if args.mar_smooth:
        img_orig = np.copy(img)
    if args.mar_threshold < np.max(img):
        threshold_up = args.mar_threshold
        remove_small_bodies = False
    else:
        # Some images has very restricted color levels (-3024, 3071). In that
        # case, the metal bodies cannot be eventually located using the
        # threshold value (which is usually bigger than 3071). As a partial fix,
        # we are considering as metal bodies all the pixels with the maximum
        # color level. However, to avoid noise may ruins all the process, the
        # small bodies will be removed
        threshold_up = np.max(img)
        remove_small_bodies = True
    threshold_down = -args.mar_threshold
    global HU_METAL
    HU_METAL = threshold_up
    thetas = np.linspace(0.,
                         180.,
                         args.mar_resolution or np.max(img.shape[0:2]),
                         endpoint=False)
    if args.debug and not os.path.exists('DBG_001_MAR'):
        os.makedirs('DBG_001_MAR')

    neglect = __eyes_protector(img,
                               (threshold_down, threshold_up),
                               (args.enhance_air, args.enhance_tissue),
                               remove_small_bodies)

    pbar = helpers.ProgressBar()
    for s in range(img.shape[2]):
        pbar.update(float(s) / (img.shape[2] - 1))
        mask = np.logical_or(img[:,:,s] >= threshold_up,
                             img[:,:,s] <= threshold_down).astype(np.int)
        mask = np.logical_and(mask,
                              np.logical_not(neglect[:,:,s]))
        if remove_small_bodies:
            mask = np.logical_and(mask,
                ndimage.binary_dilation(ndimage.binary_erosion(
                    mask, iterations=1), iterations=3))
        if not np.any(mask) and not args.mar_all:
            # Not metal body has been found, and the user is not asking to do
            # the job anyway
            continue
        # Launch the job in a parallel thread
        t = NMarThread(img, s, thetas, mask, dbg=args.debug)
        # t = FSMarThread(img, s, thetas, mask, np.asarray(vtk_img.GetSpacing()),
        #                 dbg=args.debug)
        while threading.activeCount() - 1 >= threads:
            time.sleep(0.1)
        t.start()

    # Wait for the pending jobs
    while threading.activeCount() > 1:
        time.sleep(0.1)

    if args.mar_smooth:
        img = __smooth(img_orig, img)
        img = __gamma_correction(img_orig, img, (args.enhance_air,
                                                 args.enhance_tissue))

    if args.debug:
        helpers.print_dicom(img,
                            'DBG_001_MAR',
                            cmin=-1000.0,
                            cmax=1000.0)
    helpers.numPyTovtkImage(vtk_img, img)
    return vtk_img
