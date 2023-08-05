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
import dicom
import numpy as np
import vtk
import gdcm
import vtkgdcm


def __filter_by_series(files):
    """Read a list of DICOM files, and extract the most popular series, i.e.
    the series with more files. If the resulting number of files is too sort,
    then the original list of files is returned

    This function is quite useful to neglect "strange" slices, like the
    localizer

    Parameters
    ----------
    files : list
        Original list of files

    Returns
    -------
    series : list
        List of files filtered by series number
    """
    series = {}
    for f in files:
        dcm = dicom.read_file(f, force=True)
        # Get the series number, if available
        try:
            num = dcm.SeriesNumber
        except AttributeError:
            num = None
        # Append the files to the corresponding series
        try:
            series[num].append(f)
        except KeyError:
            series[num] = [f]

    # Look for the biggest series
    s_key = list(series.keys())[0]
    for key in series.keys():
        if len(series[s_key]) >= len(series[key]):
            continue
        s_key = key

    # If the resulting list is too small, keep the old one
    if len(series[s_key]) <= 0.5 * len(files):
        return files
    return series[s_key]


def __sort_by_position(files):
    """Sort the slices using the ImagePositionPatient parameter.

    ImagePositionPatient is in general more convenient to SliceThickness, and
    should be used if possible.

    Parameters
    ----------
    files : list
        List of files to become read (sorted by filename)

    Returns
    -------
    sorted_files : list
        List of files to become read, sorted by its slice position
    thickness : scalar
        distance between slices
    slice_axis : {0, 1, 2}
        Index os the axis associated to the slicing direction
    """
    # Setup a list of slices with their position
    slices = np.zeros((len(files), 4))
    for i,f in enumerate(files):
        try:
            dcm = dicom.read_file(f, force=True)
        except:
            print("Failure reading '{}'".format(f))
            continue
        try:
            slices[i, 0] = i
            slices[i, 1:] = list(map(float, dcm.ImagePositionPatient))
        except AttributeError:
            print("'{}' has not ImagePositionPatient attribute!".format(f))
            continue
    # Get the growing axis
    slice_axis = np.argmax(
        [np.max(slices[:, i + 1]) - np.min(slices[:, i + 1]) for i in range(3)])
    # Sort the slices according to such axis
    sorted_slices = slices[slices[:, slice_axis + 1].argsort()]
    sorted_files = [files[int(i)] for i in sorted_slices[:, 0]]
    # Compute the spacing
    positions = slices[:, slice_axis + 1]
    thickness = (np.max(positions) - np.min(positions)) / (len(files) - 1)
    return sorted_files, thickness, slice_axis


def __sort_by_location(files):
    """Sort the slices using the SliceLocation parameter.

    ImagePositionPatient is in general more convenient, however, it is sometimes
    not available

    Parameters
    ----------
    files : list
        List of files to become read (sorted by filename)

    Returns
    -------
    sorted_files : list
        List of files to become read, sorted by its slice position
    thickness : scalar
        distance between slices
    slice_axis : {0, 1, 2}
        Index os the axis associated to the slicing direction
    """
    # Setup a list of slices with their position
    slices = np.zeros((len(files), 2))
    for i,f in enumerate(files):
        try:
            dcm = dicom.read_file(f, force=True)
        except:
            print("Failure reading '{}'".format(f))
            continue
        try:
            slices[i, 0] = i
            slices[i, 1] = float(dcm.SliceLocation)
        except AttributeError:
            print("'{}' has not SliceLocation attribute!".format(f))
            continue
    # Sort the slices
    sorted_slices = slices[slices[:, 1].argsort()]
    sorted_files = [files[int(i)] for i in sorted_slices[:, 0]]
    # Compute the spacing
    positions = slices[:, 1]
    thickness = (np.max(positions) - np.min(positions)) / (len(files) - 1)
    return sorted_files, thickness, 2


def __sort_by_instance(files):
    """Sort the slices using the InstanceNumber parameter.

    This is the last reliable way to sort the files. We are relying in
    SliceThickness, and using InstanceNumber to sort them

    Parameters
    ----------
    files : list
        List of files to become read (sorted by filename)

    Returns
    -------
    sorted_files : list
        List of files to become read, sorted by its slice position
    """
    # Setup a list of slices with their position
    slices = np.zeros((len(files), 2))
    for i,f in enumerate(files):
        try:
            dcm = dicom.read_file(f, force=True)
        except:
            print("Failure reading '{}'".format(f))
            continue
        try:
            slices[i, 0] = i
            slices[i, 1] = list(map(float, dcm.InstanceNumber))
        except AttributeError:
            print("'{}' has not InstanceNumber attribute!".format(f))
            continue
    # Sort the slices
    sorted_slices = slices[slices[:, 1].argsort()]
    sorted_files = [files[int(i)] for i in sorted_slices[:, 0]]
    return sorted_files


def __get_data(files):
    """Read the files with PyDICOM, and return the spacing. PyDICOM is the most
    reliable library to make this work.

    Parameters
    ----------
    files : list
        List of files to become read

    Returns
    -------
    dims : np.array
        Dimensions in pixels
    spacing : np.array
        Spacing between pixels [m]
    sorted_files : list
        List of files to become read, sorted by its slice position
    slice_axis : int
        Slicing axis. 0 if the slices are distributed along x axis, 1 if they
        are distributed along y, 2 if they are distributed along z.
    """
    # Select the most convenient series
    files = __filter_by_series(files)

    # Read the the reference file (the first one with the attributes Rows and
    # Columns)
    ref_dcm = None
    dims = np.zeros(3, dtype=int)
    for i,f in enumerate(files):
        dcm = dicom.read_file(f, force=True)
        try:
            dims = np.asarray((int(dcm.Rows), int(dcm.Columns), len(files)),
                              dtype=int)
        except:
            continue
        ref_dcm = dcm
        files = files[i:]
        break

    if ref_dcm is None:
        return dims, np.zeros(3, dtype=float), files, 2

    # Check that the minimum data is available
    if not hasattr(ref_dcm, 'PixelSpacing'):
        return dims, np.zeros(3, dtype=float), files, 2

    if not hasattr(ref_dcm, 'ImagePositionPatient') and \
       not hasattr(ref_dcm, 'SliceLocation') and \
       not hasattr(ref_dcm, 'SliceThickness'):
        return dims, np.zeros(3, dtype=float), files, 2

    # ImagePositionPatient is much more reliable than SliceThickness
    if hasattr(ref_dcm, 'ImagePositionPatient'):
        sorted_files, thickness, slice_axis = __sort_by_position(files)
    elif hasattr(ref_dcm, 'SliceLocation'):
        sorted_files, thickness, slice_axis = __sort_by_location(files)
    elif hasattr(ref_dcm, 'InstanceNumber'):
        sorted_files = __sort_by_instance(files)
        thickness = float(ref_dcm.SliceThickness)
        slice_axis = 2
    else:
        sorted_files = files
        thickness = float(ref_dcm.SliceThickness)
        slice_axis = 2

    # Compute the spacing (in meters)
    spacing = np.asarray(list(map(float, ref_dcm.PixelSpacing)), dtype=float)
    spacing = np.insert(spacing, slice_axis, thickness) * 1E-3

    return dims, spacing, sorted_files, slice_axis


def __clean_icons(files):
    """DICOM disposes the TAG 0x0088,0x0200 to define image icon. However, such
    TAG may be wrongly defined, resulting in a program crash.

    Such TAG is useless for our purposes, so we can just remove it, just in case

    Parameters
    ----------
    files : list
        List of files to become manipulated
    """
    for f in files:
        r = gdcm.Reader()
        r.SetFileName(f)
        r.Read()
        manipulator = gdcm.Anonymizer()
        manipulator.SetFile( r.GetFile() )
        manipulator.Remove( gdcm.Tag(0x0088,0x0200) )
        w = gdcm.Writer()
        w.SetFile( manipulator.GetFile() )
        w.SetFileName(f)
        w.Write()


def __load_dicom(folder, output_file):
    """Load a DICOM provided its folder.

    The DICOM data is loaded using vtkGDCMImageReader (see
    http://www.vtk.org/Wiki/VTK/FAQ#How_can_I_read_DICOM_files_.3F).

    However such reader may fail at the time of evaluating the pixel spacing, so
    we are relying in PyDICOM to recognize valid DICOM files and read such
    metadata. This is relatively common in some old machines.

    Parameters
    ----------
    dicom_path : str
        Folder containing the DICOM files. The DICOM files should have the
        extension *.dcm
    output_file : str
        Save the readed data as an VTK Image file (the user is responsible of
        setting the *.vti extension). None if the loaded DICOM data should not
        be saved as VTI

    Returns
    -------
    shape : np.array
        Dimensions in pixels
    spacing : np.array
        Spacing between pixels [m]
    img : vtk.vtkImageData
        Loaded DICOM as VTK image
    """
    # List the available files
    files = []
    for filename in sorted(os.listdir(folder)):
        if not filename.lower().endswith(".dcm"):
            continue
        files.append(os.path.join(folder, filename))
    if not files:
        raise IOError("Can't find *.dcm files in path '{}'".format(folder))

    # Use PyDICOM to get the relevant metadata
    shape, spacing, sorted_files, slice_axis = __get_data(files)

    # Clean DICOM icon image, which may crash the program and is useless anyway
    __clean_icons(sorted_files)

    # Read the DICOM with vtkGDCMImageReader
    files_vtk = vtk.vtkStringArray()
    for f in sorted_files:
        files_vtk.InsertNextValue(f)
    reader = vtkgdcm.vtkGDCMImageReader()
    reader.SetFileNames(files_vtk)
    reader.FileLowerLeftOn()

    # Eventually correct the orientation and spacing
    mat = vtk.vtkMatrix4x4()
    mat.DeepCopy(reader.GetDirectionCosines())
    if slice_axis != 2 and \
       [mat.GetElement(i, i) for i in range(3)] == [1, 1, 1]:
        mat.SetElement(2, 2, 0)
        mat.SetElement(slice_axis, slice_axis, 0)
        mat.SetElement(slice_axis, 2, 1)
        mat.SetElement(2, slice_axis, -1)
        spacing[slice_axis], spacing[2] = spacing[2], spacing[slice_axis]
    image_modifier = vtk.vtkImageChangeInformation()
    image_modifier.SetInputConnection(reader.GetOutputPort())
    image_modifier.SetOutputSpacing(spacing[0],
                                    spacing[1],
                                    spacing[2])
    # For float precission reasons, it is better to stick close to 0,0,0
    image_modifier.SetOutputOrigin(0,0,0)
    image_modifier.Update()
    image_reslice = vtk.vtkImageReslice()
    image_reslice.SetInputConnection(image_modifier.GetOutputPort())
    mat.Invert()
    image_reslice.SetResliceAxes(mat)
    image_reslice.Update()
    img = image_reslice.GetOutput()

    # Save the data if the user queried for that
    if output_file is not None:
        writer = vtk.vtkXMLImageDataWriter()
        writer.SetFileName(output_file)
        writer.SetInputConnection(image_reslice.GetOutputPort());
        writer.SetDataModeToBinary()
        writer.Write()

    return shape, spacing, img


def __load_vti(filepath, output_file):
    """Load a VTI file.

    Parameters
    ----------
    filepath : str
        Path of the VTI file
    output_file : str
        Save a copy of the read VTK Image file (the user is responsible of
        setting the *.vti extension). None if the a copy should not be saved

    Returns
    -------
    shape : np.array
        Dimensions in pixels
    spacing : np.array
        Spacing between pixels [m]
    img : vtk.vtkImageData
        Loaded DICOM as VTK image
    """
    # Load the data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(filepath)
    reader.Update()
    img = reader.GetOutput()
    shape = np.asarray(img.GetDimensions(), dtype=int)
    spacing = np.asarray(img.GetSpacing(), dtype=float)

    # Save the data if the user queried for that
    if output_file is not None:
        writer = vtk.vtkXMLImageDataWriter()
        writer.SetFileName(output_file)
        writer.SetInputConnection(reader.GetOutputPort());
        writer.SetDataModeToBinary()
        writer.Write()

    return shape, spacing, img


def load(dicom_path, output_file=None):
    """Load a DICOM or a VTI file.

    Parameters
    ----------
    dicom_path : str
        Folder containing the DICOM files, or path of a VTI file
    output_file : str
        Save the readed data as an VTK Image file (the user is responsible of
        setting the *.vti extension). None if the data loaded DICOM should not
        be saved as VTI

    Returns
    -------
    shape : np.array
        Dimensions in pixels
    spacing : np.array
        Spacing between pixels [m]
    img : vtk.vtkImageData
        Loaded DICOM as VTK image
    """
    # Discriminate between DICOM folder of VTI file
    assert(os.path.exists(dicom_path))
    if os.path.isdir(dicom_path):
        return __load_dicom(dicom_path, output_file)
    else:
        return __load_vti(dicom_path, output_file)
