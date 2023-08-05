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
from . import helpers


def segmentation(img, segmentated):
    """Evaluate Dice Similarity Coefficient, and the Jaccard and Jaccard (also
    known as Tannimoto) coefficient. See: see L. R. Dice, "Measures of the
    amount of ecologic association between species", Ecology, vol. 26,
    pp. 297-302, 1945, and P. Jaccard, "Nouvelles recherches sur la distribution
    florale", Bulletin de la Societe Vaudoise des Sciences Naturelles, vol. 44,
    pp. 223-270, 1908.

    To do that, we are considering as X the segmented air cavity, while we are
    considering as Y everything with a value higher than -500 HU, the
    theoretical value for air.

    Parameters
    ----------
    img : ndarray
        Original image
    segmentated : ndarray
        Selected air voxels

    Returns
    -------
    J : scalar
        Jaccard Similarity Coefficient
    D : scalar
        Dice Similarity Coefficient
    """
    C = -500

    X = (segmentated > 0.5)
    Y = (img > C)

    X_and_Y = np.logical_and(X, Y).astype(np.float)
    X_or_Y = np.logical_or(X, Y).astype(np.float)

    J = np.sum(X_and_Y) / np.sum(X_or_Y)
    D = 2 * np.sum(X_and_Y) / (np.sum(X) + np.sum(Y))

    return J, D
