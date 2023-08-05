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
import scipy.misc
import matplotlib.pyplot as plt
import vtk
from vtk.util import numpy_support


def vtkImageToNumPy(img):
    """Create a numpy array from the VTK image raw data

    Parameters
    ----------
    img : vtk.vtkImageData
        VTK image to be converted

    Returns
    -------
    output : np.ndarray
        Converted image
    """
    _extent = img.GetExtent()
    shape = [_extent[1] - _extent[0] + 1,
             _extent[3] - _extent[2] + 1,
             _extent[5] - _extent[4] + 1]

    data = img.GetPointData()
    data_type = numpy_support.get_numpy_array_type(data.GetArray(0).GetDataType())
    flatten_array = np.asarray(numpy_support.vtk_to_numpy(data.GetArray(0)),
                               dtype=data_type)
    inv_array = flatten_array.reshape(shape[::-1])
    return inv_array.transpose(2,1,0)


def numPyTovtkImage(img, np_array):
    """Set the VTK image raw data from a numpy array

    Parameters
    ----------
    img : vtk.vtkImageData
        VTK image to become filled with the data
    np_array : np.ndarray
        Data to fill the VTK image

    Returns
    -------
    img : vtk.vtkImageData
        Modified VTK image
    """
    flatten_array = np_array.transpose(2,1,0).flatten()
    data = numpy_support.numpy_to_vtk(num_array=flatten_array,
                                      deep=True,
                                      array_type=img.GetScalarType())
    img.GetPointData().SetScalars(data)
    return img


def renormalize(img, only_positive=False):
    """Renormalize a float image to become between -1 and 1

    Parameters
    ----------
    img : np.ndarray
        Numpy image to become renormalized
    only_positive : bool
        True if the resulting image should have values in range [0, 1], instead
        of [-1, 1]

    Returns
    -------
    img : np.ndarray
        Renormalized image
    cmin : float
        Minimum value used to renormalize
    cmax : float
        Maximum value used to renormalize
    """
    img = np.copy(img).astype(np.float)
    cmax = np.max(img)
    cmin = np.min(img)
    if not only_positive:
        vmax = np.max((np.abs(cmax), np.abs(cmin)))
        return img / vmax, -vmax, vmax
    return (img - cmin) / (cmax - cmin), cmin, cmax


def np_show(img, title=None, margin=0.05, dpi=40):
    """Plot a numpy image (2D)

    Parameters
    ----------
    img : np.ndarray
        Numpy image to become renormalized
    title : str
        Title of the plot
    margin : float
        Window to plot margin
    dpi : int
        Resolution (Dots Per Inch)
    """
    figsize = (1 + margin) * img.shape[1] / dpi, (1 + margin) * img.shape[0] / dpi
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])

    plt.set_cmap("gray")
    ax.imshow(img.transpose(1,0), interpolation=None, origin='lower')
    
    if title is not None:
        plt.title(title)
    
    plt.show()


def print_slices(img, path, cmin=0.0, cmax=1.0, axis=2):
    """Save the slices of an image to the desired folder

    Parameters
    ----------
    img : np.ndarray
        Numpy image to become renormalized
    path : str
        File path where the image should be saved
    cmin : float
        Value corresponding to black color
    cmax : float
        Value corresponding to white color
    axis : {0, 1, 2}
        0 for sagittal slices, 1 for coronal, 2 for axial
    """
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(img.shape[axis]):
        slc = [slice(None)] * len(img.shape)
        slc[axis] = i
        scipy.misc.toimage(img[slc].transpose(1,0)[::-1, :],
                           cmin=cmin, cmax=cmax).save(
            os.path.join(path, '{:04d}.png'.format(i)))

def print_dicom(img, path, cmin=0.0, cmax=1.0):
    """Save all the slices of an image in the desired folder, into 3 subfolder,
    1 for each slice direction (i.e. sagittal, coronal and axial). 

    Parameters
    ----------
    img : np.ndarray
        Numpy image to become renormalized
    path : str
        File path where the image should be saved
    cmin : float
        Value corresponding to black color
    cmax : float
        Value corresponding to white color
    """
    if not os.path.exists(path):
        os.makedirs(path)
    for axis,name in enumerate(('sagittal', 'coronal', 'axial')):
        print_slices(img,
                     os.path.join(path, name),
                     cmin=cmin,
                     cmax=cmax,
                     axis=axis)


def save_surface(surface, fname, mode='binary'):
    """Save a VTK surface with the specified name.

    Parameters
    ----------
    surface : vtk.vtkPolyData
        Surface to be saved
    fname : str
        File path where the image should be saved
    mode : {'binary', 'ascii'}
        Set the file format. 'binary' is strongly recommended
    """
    assert mode in ('binary', 'ascii')
    folder = os.path.dirname(os.path.realpath(fname))
    if not os.path.exists(folder):
        os.makedirs(folder)
    writer = vtk.vtkPolyDataWriter()
    try:
        writer.SetInputConnection(surface.GetOutputPort())
    except:
        if vtk.VTK_MAJOR_VERSION <= 5:
            writer.SetInput(surface)
        else:
            writer.SetInputData(surface)
    writer.SetFileName(fname)
    if mode == "binary":
        writer.SetFileTypeToBinary()
    elif mode == "ascii":
        writer.SetFileTypeToASCII()
    writer.Write()


class ProgressBar(object):
    """A simple but powerful progress bar implementation

    To use it, just simply call the constructor and the progress bar will be
    automatically initialized. After that, you can call update method to set
    the percentage of work done. When the 100% of work is accomplished, the
    progress bar will be automatically destroyed (and further calls to update
    will not have any effect)
    """
    def __init__(self, width=50):
        """Initialize the progress bar.

        Parameters
        ----------
        width : int
            Width (in chars) of the progress bar
        """
        self.__symbols = ('-', '\\', '|', '/')
        self.__active_symbol = 0
        self.__width = width
        self.__complete = False
        sys.stdout.write("[{}] 000.00%".format(" " * width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (width+9))
        self.update(0.0)

    def update(self, done):
        """Update the progress bar percentage done.

        In case the percentage is bigger than 1, the progress bar will be
        finished.

        Parameters
        ----------
        done : float
            Percentage done, in range [0, 1]
        """
        if self.__complete == True:
            return

        if done >= 1.0:
            self.__complete = True
            sys.stdout.write("{}] 100.00%".format("-" * self.__width))
            sys.stdout.write("\n")
            return

        if done < 0.0:
            done = 0.0

        # Print the new state of the progress bar
        width = int(self.__width * done)
        sys.stdout.write("{}".format("-" * width))
        sys.stdout.write(self.__symbols[self.__active_symbol])
        sys.stdout.write("{}".format(" " * (self.__width - width - 1)))
        sys.stdout.write("] {:06.2f}%".format(done * 100))
        sys.stdout.flush()
        sys.stdout.write("\b" * (9 + self.__width))
        # Change the symbol for the next time
        self.__active_symbol += 1
        if self.__active_symbol >= len(self.__symbols):
            self.__active_symbol = 0
