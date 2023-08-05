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
from . import helpers


def __expand(img, dtype):
    """Transform the color scale of a renormalized image, i.e. an image with the
    gray scale [0, 1]. The new color scale will be fitted to the maximum range
    of values accepted by dtype

    Parameters
    ----------
    img : np.ndarray
        NumPy image to be expanded
    dtype : np.dtype
        Destiny image type descriptor

    Returns
    -------
    output : np.ndarray
        Casted NumPy image
    """
    idtype = np.iinfo(dtype)
    output = img * (idtype.max - idtype.min) + idtype.min
    # Clamp eventually wrong values
    output[output > idtype.max - 1] = idtype.max - 1
    output[output < idtype.min + 1] = idtype.min + 1
    # Return the image casting to the new type
    return output.astype(dtype)


def __add(I, M):
    """Adds the image M to the image of I. See
    https://docs.gimp.org/en/gimp-concepts-layer-modes.html
    and
    https://github.com/jamieowen/glsl-blend/blob/master/add.glsl
    Renormalized images are assumed, i.e. colors range = [0, 1]

    Parameters
    ----------
    I : np.ndarray
        Left side operator
    M : np.ndarray
        Right side operator

    Returns
    -------
    E : np.ndarray
        Added image
    """
    E = I + M
    E[E > 1] = 1
    return E


def __substract(I, M):
    """Substract the image M to the image of I. See
    https://docs.gimp.org/en/gimp-concepts-layer-modes.html
    and
    https://github.com/jamieowen/glsl-blend/blob/master/substract.glsl
    Renormalized images are assumed, i.e. colors range = [0, 1]

    Parameters
    ----------
    I : np.ndarray
        Left side operator
    M : np.ndarray
        Right side operator

    Returns
    -------
    E : np.ndarray
        Substracted image
    """
    E = I - M
    E[E < 0] = 0
    return E


def enhance(vtk_img, args):
    """Enhance the image to split the air from the tissue

    The tool is thresholding and renormalizing the image. After that, a canny
    detector is used to look for subpixel airflow cavities, and a Laplacian is
    used for pixel precision holes digging.

    The image returned is expanded to fit in the range of values accepted by the
    original VTK image.

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
    print('Images enhancement...')
    # Threshold and renormalize the image
    result = helpers.vtkImageToNumPy(vtk_img)
    img_type = result.dtype
    result[result < args.enhance_air] = args.enhance_air
    result[result > args.enhance_tissue] = args.enhance_tissue
    result, _, _ = helpers.renormalize(result, only_positive=True)
    if args.debug:
        helpers.print_dicom(result,
                            'DBG_003a_threshold',
                            cmin=0.0,
                            cmax=1.0)

    # Save the tissues to restore later the eventually affected ones
    tissue_mask = result > 0.99

    # Apply a unsharp masking
    USM_FACTOR = 0.5
    mask = np.ones(result.shape, dtype=result.dtype)
    mask -= ndimage.gaussian_filter(result, 1)
    mask *= USM_FACTOR
    result = __add(result, mask)
    result -= USM_FACTOR
    result /= (1.0 - USM_FACTOR)
    result[result < 0.0] = 0.0
    result[result > 1.0] = 1.0
    if args.debug:
        helpers.print_dicom(mask,
                            'DBG_003b_usm_mask',
                            cmin=0.0,
                            cmax=1.0)
        helpers.print_dicom(result,
                            'DBG_003b_usm_result',
                            cmin=0.0,
                            cmax=1.0)

    # Use a canny edge detector to highlight the subpixels precision borders
    edges = np.zeros(result.shape, dtype=result.dtype)
    for s in range(result.shape[1]):
        edges[:,s,:] = feature.canny(result[:,s,:], sigma=1)
    edges = ndimage.binary_dilation(edges, iterations=1).astype(edges.dtype)
    edges = ndimage.binary_fill_holes(edges).astype(edges.dtype)
    # edges = ndimage.binary_erosion(edges, iterations=1).astype(edges.dtype)
    result[edges > 0.5] = result[edges > 0.5]**3
    if args.debug:
        helpers.print_dicom(edges,
                            'DBG_003c_canny_edges',
                            cmin=0.0,
                            cmax=1.0)
        helpers.print_dicom(result,
                            'DBG_003c_canny_result',
                            cmin=0.0,
                            cmax=1.0)

    # Use a Laplacian operator to dig the large cavities in the image. Since we
    # are just interested into digging, the negative values of the Laplacian
    # are neglected, as well as the really low one (which may be arising from
    # noise)
    ddx = ndimage.gaussian_filter(result, 1, order=[2,0,0])
    ddz = ndimage.gaussian_filter(result, 1, order=[0,0,2])
    lap_1 = ddx + ddz
    lap_1 /= np.max(lap_1)
    ddx = ndimage.gaussian_filter(result, 3, order=[2,0,0])
    ddz = ndimage.gaussian_filter(result, 3, order=[0,0,2])
    lap_2 = ddx + ddz
    lap_2 /= np.max(lap_2)
    lap = lap_1 + lap_2
    lap[lap < 0.05] = 0
    lap = lap**0.5
    result = __substract(result, 2 * lap)
    if args.debug:
        helpers.print_dicom(lap,
                            'DBG_003d_lap_edges',
                            cmin=0.0,
                            cmax=1.0)
        helpers.print_dicom(result,
                            'DBG_003d_lap_result',
                            cmin=0.0,
                            cmax=1.0)

    # Restore the eventually affected tissues. This is called to become a
    # barrier to avoid the artifacts arising from noise becomes connected to the
    # actual airflow geometry
    result[tissue_mask] = 1.0
    if args.debug:
        helpers.print_dicom(result,
                            'DBG_003_enhanced',
                            cmin=0.0,
                            cmax=1.0)

    # Recover the original image gray scale, optimizing the resulting image
    # values to fit in such scale
    result = __expand(result, img_type)
    return helpers.numPyTovtkImage(vtk_img, result)
