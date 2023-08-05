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
import sys
import numpy as np
from scipy import ndimage
from skimage import filters, feature
from skimage.morphology import convex_hull_image
import vtk
from . import helpers


def _watershed(img, win, seeds, in_value=1, out_value=0):
    """Growing/watershed algorithm to segmentate a NumPy of arbitrary
    number of dimensions (including of course 3D images).

    Parameters
    ----------
    img : np.ndarray
        Numpy image to segmentate
    win : [Imin, Imax]
        Minimum and maximum radiosity bounds to consider the pixel inside. If
        win[0] is None, all the values lower than win[1] will be considered
        inside, and in the same way, if win[1] is None, then all the values
        bigger than win[0] will be considered inside
    seeds : list/np.ndarray
        List of seeds to start the growing algorithm. each seed should have the
        same dimensions than the input image, img. In case a seed is placed in
        the non-selected region (value out of win bounds), it will be neglected.
        Also a boolean image can be provided.
    in_value : scalar
        The hit pixels/voxels values will be replaced by this one. None if such
        pixels' values should not be replaced
    in_value : scalar
        The non-selected pixels/voxels values will be replaced by this one. None
        if such pixel values should not be replaced

    Returns
    -------
    result : np.ndarray
        Copy of the input image with the values conveniently replaced.
    """
    assert win[0] is not None or win[1] is not None
    # Build up an image of seeds (only the labels found in the seeds will be
    # considered)
    seed_img = np.zeros(img.shape, dtype=bool)
    try:    
        seed_img[seeds] = True
    except IndexError:
        for seed in seeds:
            seed_img[seed] = True
    # Determine the region of the image with valid values, thresholding the
    # image: win[0] < img < win[1]
    upper = np.ones(img.shape, dtype=bool)
    lower = np.ones(img.shape, dtype=bool)
    if win[0] is not None:
        upper = img >= win[0]
    if win[1] is not None:
        lower = img <= win[1]
    thrimg = np.logical_and(lower, upper)
    # Labelize the image, and select the found regions with seeds inside
    lmap, _ = ndimage.label(thrimg, structure=None)
    lids = np.unique(lmap[seed_img])
    region = np.zeros(img.shape, np.bool)
    for lid in lids:
        region |= lmap == lid
    # Exclude the regions eventually seeded from invalid values
    region = np.logical_and(region, thrimg)
    # Setup and return the result
    result = np.copy(img)
    if in_value is not None:
        result[region] = in_value
    if out_value is not None:
        result[np.logical_not(region)] = out_value
    return result


def __voxelization(img, Imax):
    """Threshold the 3D image, departing from the well known background points,
    which is surely connected to the nasal cavity.

    Parameters
    ----------
    img : np.ndarray
        Numpy image to segmentate
    Imax : scalar
        Maximum value to consider that a voxel belong to air

    Returns
    -------
    result : np.ndarray
        The thresholded image (same dtype than input image)
    """
    slice_idx = 1
    while True:
        # Launch the algorithm
        seeds = (10, 10, slice_idx),
        thrimg = _watershed(img, [None, Imax], seeds)
        if np.sum(thrimg) != 0:
            # Success!
            return thrimg

        # It seems that the selected slice have not a valid background
        slice_idx += 1


def __rough_background(img, axis=2):
    """Get a rough approximation of the background using 2D slices.

    Parameters
    ----------
    img : np.ndarray
        Numpy image to segmentate
    axis : {0, 1, 2}
        Slicing axis to make the background filtering, i.e. axis=0,1,2 for
            sagittal,coronal,axial slices based respectively

    Returns
    -------
    result : np.ndarray
        The background image
    """
    result = np.copy(img)
    # Transpose the image according to the selected axis
    indexes = np.roll(np.arange(3), 2 - axis)
    result = result.transpose(*indexes)
    # Filter the background
    seeds = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for slice_idx in range(result.shape[2]):
        result[:,:,slice_idx] = _watershed(result[:,:,slice_idx], 
                                            (0.5, None),
                                            seeds)
    # Untranspose the result to recover the original axes
    indexes = np.roll(np.arange(3), axis - 2)
    return result.transpose(*indexes)


def __select_body(img, spacing, min_vol=15.0E-6):
    """Select the nasal cavity from all the available bodies.

    Parameters
    ----------
    img : np.ndarray
        Voxelization of the "inner" bodies, from which we should determine the
        nasal cavity
    spacing : [spacing_1, spacing_2, spacing_3]
        Voxels size along each axis
    min_vol : scalar
        Minimum volume [m^3] to consider a volume as a candidate to become the
        nasal cavity

    Returns
    -------
    result : np.ndarray
        The nasal cavity voxelization
    out : np.ndarray
        Image with just the voxels associated with the pharynx
    """
    min_vol /= np.prod(spacing)
    z_start = 1 # We must take into account that we added background layers

    # Get the total collection of bodies
    labels, nbodies = ndimage.label(img)

    # Select the valid candidates
    valid_labels = []
    vols = []
    bottom_labels = labels[:,:,z_start]
    for label in range(1, nbodies + 1):
        if not np.any(bottom_labels == label):
            # Discard the bodies without intersection with the bottom
            continue
        vol = np.sum((labels == label).astype(np.float))
        if vol < min_vol:
            # Discard the too small bodies
            continue
        valid_labels.append(label)
        vols.append(vol)

    if not len(valid_labels):
        raise ValueError('No valid nasal cavity candidates found')

    # Compute the x variable standard deviation of each body
    stds = []
    for i,label in enumerate(valid_labels):
        cx = labels.shape[0] // 2
        hits = np.nonzero(labels == label)
        stds.append(np.sum((np.asarray(hits[0]) - cx)**2) / vols[i])

    # Select the body with standard deviation (i.e. the best centered one)
    label = valid_labels[np.argmin(stds)]

    result = np.zeros(img.shape, dtype=np.float)
    result[labels == label] = 1.0

    # Compute the outflow
    out = np.zeros(result.shape)
    labels, nbodies = ndimage.label(result[:,:,z_start])
    if nbodies == 1:
        out[:,:,z_start] = result[:,:,z_start]
    else:
        # Get the y coordinate, the area and the inertia
        y = np.zeros(nbodies, dtype=np.float)
        a = np.zeros(nbodies, dtype=np.float)
        i = np.ones(nbodies, dtype=np.float)
        for label in range(1, nbodies + 1):
            mask = (labels == label).astype(np.float)
            hits = np.nonzero(mask)
            y[label - 1] = np.mean(hits[1])
            a[label - 1] = np.sum(mask)
            i[label - 1] = np.sum((np.asarray(hits[0]) - cx)**2) / a[label - 1]
        # Renormalize
        y /= labels.shape[1]
        a /= np.max(a)
        i /= np.max(i)
        # Compute the utility function (we are looking for maximum y, maximum
        # area, and minimum inertia)
        f = y * a * (1.0 - i)
        label = np.argmax(f) + 1
        out[:,:,z_start][labels == label] = result[:,:,z_start][labels == label]

    return result, out


def __contact(img, bck):
    """Get the contact between the rough approximation of the nasal cavity and
    its associated background

    Parameters
    ----------
    img : np.ndarray
        Nasal cavity voxelization
    bck : np.ndarray
        Background voxelization

    Returns
    -------
    labels : np.ndarray
        Contact image. It may eventually have 1 and 2 values correspoding to the
        2 nostrils (if the nostrils are connected, just 1 values will be
        returned)
    """
    struct = ndimage.generate_binary_structure(3, 3)

    # Look for the contact between the body and the background
    bck = np.copy(bck)
    # Contact points in the caps cannot be considered
    bck[:,:,:2] = 0
    bck[:,:,-2:] = 0
    # bck = ndimage.binary_dilation(bck, structure=struct).astype(bck.dtype)
    bck_rolled = np.roll(bck, 1, axis=2)
    contact = img + bck_rolled
    contact[contact < 1.5] = 0
    contact[contact >= 1.5] = 1

    if np.max(contact) == 0:
        raise AssertionError('No contact between the nasal body and the ' \
                             'background can be found')

    # label the contact bodies to look for left and right inflows
    labels, nbodies = ndimage.label(contact, structure=struct)
    if nbodies > 2:
        print('WARNING: More than 2 contact zones between the nasal body and ' \
              'the background have been found. I am trying to heuristically ' \
              'get the good ones')
        # Discard the bodies to close from the upper slice
        labels[:,:,int(0.9 * labels.shape[2]):] = 0
        # And also the ones too close to the bottom slice
        labels[:,:,:int(0.05 * labels.shape[2])] = 0
        # Compute the size of each body
        bodies = []
        for i in range(nbodies):
            body = np.zeros(labels.shape, dtype=int)
            body[labels == i + 1] = 1
            bodies.append([i + 1, np.sum(body)])
        # Sort them by size
        bodies = np.array(bodies)
        bodies = bodies[bodies[:, 1].argsort()]
        # Remove all the bodies except the 2 largest ones
        old_labels = labels
        labels = np.zeros(old_labels.shape, dtype=int)
        labels[old_labels == bodies[-2, 0]] = 1
        labels[old_labels == bodies[-1, 0]] = 2
    return labels


def __nostrils(img, bck, contact):
    """Refine the geometry description of the nostrils.

    Parameters
    ----------
    img : np.ndarray
        Nasal cavity voxelization
    bck : np.ndarray
        Background voxelization
    contact : np.ndarray
        Contact between the nasal cavity and the background

    Returns
    -------
    nostrils : np.ndarray
        Voxels to become added to the nasal cavity and substracted from the
        background.
    """
    struct = ndimage.generate_binary_structure(2, 2)

    # Setup the hull to look for the convex bodies.
    hull = np.zeros(bck.shape, dtype=bck.dtype)
    hull[bck < 0.5] = 1.0
    hull[img > 0.5] = 1.0
    # Get the bounds where looking for convex bodies
    hits = np.nonzero(contact)
    zmax = np.max(hits[2]) + 1
    ymax = np.max(hits[1]) + 2
    hits = np.nonzero(img[:,:ymax,:])
    zmin = np.min(hits[2]) - 2
    # Remove all the voxels of the hull outside
    hull_back = hull
    hull = np.zeros(bck.shape, bck.dtype)
    hull[:, :ymax, zmin:zmax] = hull_back[:, :ymax, zmin:zmax]
    # Get the remaining bounds
    hits = np.nonzero(hull)
    ymin = np.min(hits[1]) - 1
    xmin = np.min(hits[0]) - 1
    xmax = np.max(hits[0]) + 2

    # Now we can process the slides to look for convex hulls
    nostrils = np.zeros(hull.shape, dtype=hull.dtype)
    for z in range(zmin, zmax):
        if not np.any(hull[:,:,z] > 0):
            continue
        nostril = convex_hull_image(hull[:,:,z]).astype(hull.dtype)
        nostril -= hull[:,:,z]
        # Clean up small generated noise (along the external boundary of the
        # nostril image)
        nostril = ndimage.binary_erosion(nostril).astype(nostril.dtype)
        nostril = ndimage.binary_dilation(nostril,
                                          structure=struct,
                                          iterations=2).astype(nostril.dtype)
        nostril[hull[:,:,z] > 0] = 0
        # Store the result
        nostrils[:,:,z] += nostril
    for y in range(ymin, ymax):
        if not np.any(hull[:,y,:] > 0):
            continue
        nostril = convex_hull_image(hull[:,y,:]).astype(hull.dtype)
        nostril -= hull[:,y,:]
        # Clean up small generated noise (along the external boundary of the
        # nostril image)
        nostril = ndimage.binary_erosion(nostril).astype(nostril.dtype)
        nostril = ndimage.binary_dilation(nostril,
                                          structure=struct,
                                          iterations=2).astype(nostril.dtype)
        nostril[hull[:,y,:] > 0] = 0
        # Store the result
        nostrils[:,y,:] += 2 * nostril
    for x in range(xmin, xmax):
        if not np.any(hull[x,:,:] > 0):
            continue
        nostril = convex_hull_image(hull[x,:,:]).astype(hull.dtype)
        nostril -= hull[x,:,:]
        # Clean up small generated noise (along the external boundary of the
        # nostril image)
        nostril = ndimage.binary_erosion(nostril).astype(nostril.dtype)
        nostril = ndimage.binary_dilation(nostril,
                                          structure=struct,
                                          iterations=2).astype(nostril.dtype)
        nostril[hull[x,:,:] > 0] = 0
        # Store the result
        nostrils[x,:,:] += nostril

    # Get the voxels covered by at least 2 slices, where one of them should be
    # a coronal slice (which has a double weight)
    nostrils[nostrils < 2.5] = 0
    nostrils[nostrils > 0] = 1

    # Fix eventual holes generated by the noise removal
    nostrils += hull
    nostrils = ndimage.binary_closing(nostrils).astype(nostrils.dtype)
    nostrils -= hull    

    return nostrils


def __contact_nostrils(nostrils, bck, n_in=2, cx=None):
    """Get the contact between the refined nasal cavity and its associated
    background

    Parameters
    ----------
    nostrils : np.ndarray
        Nostrils refined volume
    bck : np.ndarray
        Background voxelization
    n_in : int
        1 or 2, depending on the number of open nostril airways
    cx : scalar
        Center of the nose (in the x direction). It is required if n_in is 2

    Returns
    -------
    bounds : [np.ndarray, np.ndarray]
        Contact images, corresponding to the right and left nostrils
        respectively.
    """
    assert n_in in (1, 2)
    if n_in == 1:
        assert cx is not None

    struct = ndimage.generate_binary_structure(3, 3)
    struct2D = np.copy(struct)
    struct2D[:,0,:] = 0
    struct2D[:,2,:] = 0

    # Find the new contact surface voxelization
    bck_dilated = ndimage.binary_dilation(bck,
                                          structure=struct2D).astype(bck.dtype)
    contact = nostrils + bck_dilated
    contact[contact < 1.5] = 0
    contact[contact >= 1.5] = 1
    if np.max(contact) == 0:
        raise AssertionError('No contact between the nasal body and the ' \
                             'background can be found')

    # label the contact bodies to look for left and right inflows
    labels, nbodies = ndimage.label(contact, structure=struct)
    if nbodies > n_in:
        print('WARNING: Found {} nostrils. The {} largest ones will be ' \
              'chosen'.format(nbodies, n_in))
        # Compute the size of each body
        bodies = []
        for i in range(nbodies):
            body = np.zeros(labels.shape, dtype=int)
            body[labels == i + 1] = 1
            bodies.append([i + 1, np.sum(body)])
        # Sort them by size
        bodies = np.array(bodies)
        bodies = bodies[bodies[:, 1].argsort()]
        # Remove all the bodies except the 2 largest ones
        old_labels = labels
        labels = np.zeros(old_labels.shape, dtype=int)
        for i in range(n_in):
            labels[old_labels == bodies[-2 + i, 0]] = 1 + i
    elif nbodies == 1:
        print('WARNING: Just 1 nostril found.')
            
    # Create the 2 boundaries
    bounds = []
    x = []
    for i in 1, 2:
        b = np.zeros(nostrils.shape, dtype=nostrils.dtype)
        b[labels == i] = 1.0
        bounds.append(b)
        hits = np.nonzero(b)
        if len(hits[0]):
            x.append(0.5 * (np.min(hits[0]) + np.max(hits[0])))
        else:
            x.append(None)

    # Sort as right and left
    if None in x:
        idx = 0 if x[0] is not None else 1
        if x[idx] < cx:
            bounds = [bounds[idx], bounds[1 - idx]]
        else:
            bounds = [bounds[1 - idx], bounds[idx]]
    elif x[0] > x[1]:
        bounds = bounds[::-1]

    return bounds[0], bounds[1]


def segmentation(vtk_img, args):
    """Get the voxelizations of the nasal cavity and the background (the air
    surrounding the head).

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
    print('Segmentation...')
    img = helpers.vtkImageToNumPy(vtk_img)
    # Get the top thershold value
    idtype = np.iinfo(img.dtype)
    Imax = 0.5 * (idtype.max - idtype.min) + idtype.min
    # Get the 3D voxelization of the nasal cavity and background
    voxels = __voxelization(img, Imax)
    if args.debug:
        helpers.print_dicom(voxels,
                            'DBG_004a_voxels',
                            cmin=0.0,
                            cmax=1.0)

    # Add a layer of background surrounding the DICOM, in order to close the
    # head
    voxels = np.lib.pad(voxels,
                        ((1, 1), (1, 1), (1, 1)),
                        mode='constant',
                        constant_values=1)

    # Find a rough approximation of the background using the 2D slices
    coronal_background = __rough_background(voxels, axis=1)
    axial_background = __rough_background(voxels, axis=2)
    background = coronal_background + axial_background
    if args.debug:
        helpers.print_dicom(background[1:-1,1:-1,1:-1],
                            'DBG_004b_background1',
                            cmin=0.0,
                            cmax=2.0)
    background[background < 1.5] = 0.0
    background[background >= 1.5] = 1.0
    # Sometimes, both nostrils might be totally connected in the axial slice by
    # the nasal cavity, such that it will try to add the wrong nostril as
    # background. To avoid that, we can make a second pass, when we can assert
    # that the interior of the nasal cavity has been already removed
    coronal_background = __rough_background(background, axis=1)
    axial_background = __rough_background(background, axis=2)
    background = coronal_background + axial_background
    if args.debug:
        helpers.print_dicom(background[1:-1,1:-1,1:-1],
                            'DBG_004b_background2',
                            cmin=0.0,
                            cmax=2.0)
    background[background < 1.5] = 0.0
    background[background >= 1.5] = 1.0

    # And we can just get the rough approximation of the air cavity just simply
    # substracting the background to the total voxelization
    cavity = voxels - background
    if args.debug:
        helpers.print_dicom(cavity[1:-1,1:-1,1:-1],
                            'DBG_004b_cavity',
                            cmin=0.0,
                            cmax=1.0)

    # Right now the cavity may contain some non-desired objects, so we must
    # filter out them
    cavity, out_bd = __select_body(cavity,
                                   vtk_img.GetSpacing())
    if args.debug:
        helpers.print_dicom(cavity[1:-1,1:-1,1:-1],
                            'DBG_004_cavity',
                            cmin=0.0,
                            cmax=1.0)

    # Remove the additional added layers, not required anymore
    voxels = voxels[1:-1,1:-1,1:-1]
    background = background[1:-1,1:-1,1:-1]
    cavity = cavity[1:-1,1:-1,1:-1]
    out_bd = out_bd[1:-1,1:-1,1:-1]

    # Get the contact between the rough nostrils and the background
    contact = __contact(cavity, background)
    n_in = np.max(contact)
    if args.debug:
        helpers.print_dicom(contact,
                            'DBG_005a_contact',
                            cmin=0.0,
                            cmax=2.0)

    # Refine the nostrils
    nostrils = __nostrils(cavity, background, contact)
    hits = np.nonzero(nostrils)
    nose_cx = 0.5 * (np.min(hits[0]) + np.max(hits[0]))
    if n_in == 1:
        # Remove the nostril body without contact with the cavity
        struct = ndimage.generate_binary_structure(3, 3)
        labels, nbodies = ndimage.label(nostrils, structure=struct)
        best_label = 0
        best_area = 0
        for label in range(1, nbodies + 1):
            common = np.logical_and(np.roll(labels == label, 1, axis=2),
                                    contact > 0)
            area = np.sum(common.astype(int))
            if area > best_area:
                best_area = area
                best_label = label
        nostrils = np.zeros(nostrils.shape, dtype=nostrils.dtype)
        nostrils[labels == best_label] = 1
    cavity += nostrils
    cavity[cavity > 1] = 1
    background -= nostrils
    background[background < 0] = 0

    # Get the inflow boundaries (nostrils)
    in_right, in_left = __contact_nostrils(nostrils,
                                           background,
                                           n_in=n_in,
                                           cx=nose_cx)

    # Set the background as the total voxelization, substracting the cavity
    background = voxels - cavity
    background[background < 0] = 0
    if args.debug:
        helpers.print_dicom(cavity,
                            'DBG_005_cavity',
                            cmin=0.0,
                            cmax=1.0)
        helpers.print_dicom(background,
                            'DBG_005_background',
                            cmin=0.0,
                            cmax=1.0)
        helpers.print_dicom(out_bd + 2 * in_right + 3 * in_left,
                            'DBG_005_boundaries',
                            cmin=0.0,
                            cmax=3.0)

    # Prepare the VTK images
    vtk_bck_img = vtk.vtkImageData()
    vtk_bck_img.DeepCopy(vtk_img)
    helpers.numPyTovtkImage(vtk_img, cavity)
    helpers.numPyTovtkImage(vtk_bck_img, background)

    return vtk_img, vtk_bck_img, out_bd, in_right, in_left
