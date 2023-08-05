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
from skimage.feature import peak_local_max
from skimage.morphology import watershed
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from . import helpers


def __center(img):
    """Compute the pixel coordinates of the "center" of an image, i.e. the local
    maximum peak distance from the boundary

    Parameters
    ----------
    img : np.ndarray
        Numpy image to compute

    Returns
    -------
    result : [x, y, z]
        Pixel coordinates of the center
    """
    # Using a distance transform is not a good idea, because becoming a thin
    # body, likely all the voxels would become in contact with the background,
    # and therefore have the same distance. It is better to compute the
    # centroid, and then look for the closest voxel
    hits = np.nonzero(img)
    r = np.asarray([hits[i] - np.mean(hits[i]) for i in range(3)])
    dists = np.linalg.norm(r, axis=0)
    hit_id = np.argmin(dists)
    peak = np.asarray([hits[i][hit_id] for i in range(3)])
    return peak


def __watershed(img, seeds):
    """Randomk walker algorithm to separate objects.

    Parameters
    ----------
    img : np.ndarray
        Numpy image to segmentate
    seeds : list
        List of seeds to start growing.

    Returns
    -------
    result : np.ndarray
        Numpy image with labeled objects (one label per seed, 0 is reserved for
        the background).
    """
    # Build up an image of seeds
    seed_img = np.zeros(img.shape, dtype=np.int)
    for i,seed in enumerate(seeds):
        seed_img[tuple(seed)] = i + 1
    # Try to advance by coronal sections
    advance_profile = np.transpose(np.tile(np.arange(
        img.shape[1]), (img.shape[0], img.shape[2], 1)), axes=(0, 2, 1))
    return watershed(advance_profile, seed_img, mask=img)


def rhinometry(img, in_right, in_left, args):
    """Carry out the rhinometry (if queried)

    Parameters
    ----------
    img : vtk.vtkImageData
        VTK image of the nasal cavity
    in_right : vtk.vtkImageData
        VTK image of the right nostril boundary
    in_left : vtk.vtkImageData
        VTK image of the left nostril boundary
    args : dict
        Program arguments
    """
    print('Rhinometry...')
    if not args.rhinometry_data and not args.rhinometry_graph:
        return

    spacing = np.asarray(img.GetSpacing())
    img = helpers.vtkImageToNumPy(img)
    # Get the "center" of each nostril as seeds
    has_bd = []
    seeds = []
    for bd in (in_right, in_left):
        hits = np.nonzero(bd)
        if not len(hits[0]):
            has_bd.append(False)
            continue
        has_bd.append(True)
        seeds.append(__center(bd))
    assert True in has_bd
    # Create 2 separate bodies for the left and right nostrils, using a random
    # walker algorithm
    labels = __watershed(img, seeds)
    if args.debug:
        helpers.print_dicom(labels,
                            'DBG_006_rhinometry',
                            cmin=0.0,
                            cmax=2.0)
    if has_bd[0]:
        right_img = labels == 1
        left_img = labels == 2
    else:
        right_img = np.zeros(img.shape, dtype=np.bool)
        left_img = labels == 1
    # Y coordinates
    hits = np.nonzero(img)
    start = np.min(hits[1])
    end = np.max(hits[1])
    y = np.arange(0, end + 1 - start).astype(np.float) * spacing[1] * 1E2
    # Contact slices and areas
    pixel_area = spacing[0] * spacing[1] * 1E4
    contact = np.zeros(len(y), dtype=np.int)
    right = np.zeros(len(y), dtype=np.float)
    left = np.zeros(len(y), dtype=np.float)
    contact_img = np.logical_and(np.roll(right_img, 1, axis=0), left_img)
    for i,s in enumerate(range(start, end + 1)):
        contact[i] = np.any(contact_img[:,s,:])
        right[i] = np.sum(right_img[:,s,:]) * pixel_area
        left[i] = np.sum(left_img[:,s,:]) * pixel_area
    contact, ncontacts = ndimage.measurements.label(contact)

    # Save csv file
    if args.rhinometry_data:
        with open(os.path.join(args.output, 'rhinometry.csv'), 'w') as f:
            f.write('"Distance from nostril [cm]",' \
                    '"Contact between left and right [0/1]",' \
                    '"Right cavity area [cm^2]",' \
                    '"Left cavity area [cm^2]"\n')
            for i in range(len(y)):
                f.write('{},{},{},{}\n'.format(y[i],
                                               contact[i],
                                               right[i],
                                               left[i]))

    # Plot
    if args.rhinometry_graph:
        maxwidth = int(max(np.max(right), np.max(left))) + 1.0
        rline, = plt.plot(right, y,
                         linewidth=2.0,
                         linestyle='-',
                         color='red')
        lline, = plt.plot(-left, y,
                         linewidth=2.0,
                         linestyle='-',
                         color='blue')
        for i in range(1, ncontacts + 1):
            hits = np.nonzero(contact == i)
            ymin = y[np.min(hits)]
            ymax = y[np.max(hits)]
            rect = patches.Rectangle((-2 * maxwidth, ymin),
                                     4 * maxwidth,
                                     ymax - ymin,
                                     alpha=0.25,
                                     edgecolor='none',
                                     facecolor='green')
            rect = plt.gca().add_patch(rect)
        plt.grid()
        if ncontacts:
            plt.legend((rline, lline, rect),
                       ("Right", "Left", "Contact"),
                       loc='best')
        else:
            plt.legend((rline, lline),
                       ("Right", "Left"),
                       loc='best')
        ymax = int(np.max(y)) + 1.0
        plt.xlim((-maxwidth, maxwidth))
        plt.ylim((0, ymax))
        values = plt.gca().xaxis.get_ticklocs()
        labels = []
        for v in values:
            labels.append("{}".format(abs(v)))
        plt.gca().set_xticklabels(labels)
        plt.xlabel(r"Coronal slice area [$\mathrm{cm}^2$]")
        plt.ylabel(r"Distance to nostrils [$\mathrm{cm}$]")
        plt.savefig(os.path.join(args.output, 'rhinometry.png'),
                    dpi=300)
