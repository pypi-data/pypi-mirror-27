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

import numpy as np
from scipy import ndimage
from scipy.ndimage.filters import gaussian_filter
import vtk
from . import helpers


def __marching_cubes(img, decimate_factor):
    """Reconstruct a surface from a voxelization using marching cubes. See
    https://en.wikipedia.org/wiki/Marching_cubes

    Parameters
    ----------
    img : vtk.vtkImageData
        Voxelization to become reconstructed.
    decimate_factor : scalar
        Polygons decimation rate. See vtkDecimatePro.SetTargetReduction
        documentation

    Returns
    -------
    pdn : vtk.vtkPolyDataNormals
        Reconstructed surface algorithm. To get the actual surface (i.e.
        vtk.vtkPolyData), you may call pdn.GetOutput().
    """
    dmc = vtk.vtkDiscreteMarchingCubes()
    if vtk.VTK_MAJOR_VERSION <= 5:
        dmc.SetInput(img)
    else:
        dmc.SetInputData(img)
    dmc.GenerateValues(1, 1, 1)
    dmc.ComputeNormalsOff()
    dmc.ComputeScalarsOff()
    dmc.Update()
    # Remove duplicated
    cpd = vtk.vtkCleanPolyData()
    cpd.SetInputConnection(dmc.GetOutputPort())
    # cpd.SetTolerance(1E-6)
    cpd.PointMergingOn()
    cpd.Update()
    # Decimate
    if decimate_factor < 1:
        dp = vtk.vtkDecimatePro()
        dp.SetInputConnection(cpd.GetOutputPort())
        dp.SetTargetReduction(decimate_factor)
        dp.Update()
    else:
        dp = cpd
    # Compute the normals
    pdn = vtk.vtkPolyDataNormals()
    pdn.SetInputConnection(dp.GetOutputPort())
    pdn.AutoOrientNormalsOn()
    pdn.ComputePointNormalsOn()
    pdn.ComputeCellNormalsOn()
    pdn.SplittingOff()
    pdn.Update()
    return pdn


def __smooth(obj, feature_angle=None, iterations=15, pass_band=0.001):
    """Smooth a surface. See vtkWindowedSincPolyDataFilter documentation

    Parameters
    ----------
    obj : vtk.vtkAlgorithm
        Surface to smooth
    feature_angle : scalar
        Angle to consider edges as features. If None, the algorithm will not
        look for feature angles, and everything will become smoothed
    iterations: int
        Smoothing iterations
    pass_band: float
        Spacing window length. Details lower than this value will be skiped

    Returns
    -------
    pdn : vtk.vtkPolyDataNormals
        Smoothed surface algorithm. To get the actual surface (i.e.
        vtk.vtkPolyData), you may call pdn.GetOutput().
    """
    spd = vtk.vtkWindowedSincPolyDataFilter()
    spd.SetInputConnection(obj.GetOutputPort())
    spd.SetNumberOfIterations(iterations)
    spd.SetPassBand(pass_band)
    spd.BoundarySmoothingOn()
    if feature_angle is None:
        spd.FeatureEdgeSmoothingOn()
        spd.SetFeatureAngle(120.0)        
    else:
        spd.SetFeatureAngle(feature_angle)
        spd.FeatureEdgeSmoothingOff()
    spd.NonManifoldSmoothingOn()
    spd.NormalizeCoordinatesOn()
    spd.Update()

    # Clip the data by the minimum and maximum z coordinates
    bds = obj.GetOutput().GetBounds()
    zmin, zmax = bds[4], bds[5]
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, zmin)
    plane.SetNormal(0, 0, 1)
    zmin = vtk.vtkClipPolyData()
    zmin.SetClipFunction(plane)
    zmin.SetInputConnection(spd.GetOutputPort())
    zmin.Update()
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, zmax)
    plane.SetNormal(0, 0, -1)
    zmax = vtk.vtkClipPolyData()
    zmax.SetClipFunction(plane)
    zmax.SetInputConnection(zmin.GetOutputPort())
    zmax.Update()

    pdn = vtk.vtkPolyDataNormals()
    pdn.SetInputConnection(zmax.GetOutputPort())
    pdn.ComputePointNormalsOn()
    pdn.ComputeCellNormalsOn()
    pdn.Update()

    return pdn


def __sample(obj, img):
    """Sample the image data into a surface. To do that, the image data is
    previously smoothed, and then it is sampled into the surface using a
    trilinear filter (see https://en.wikipedia.org/wiki/Trilinear_interpolation)

    The sampled data, named 'voxel_data', will be set as the active array

    Parameters
    ----------
    obj : vtk.vtkAlgorithm
        Surface where the data should be sampled
    img : vtk.vtkImageData
        Image data to be sampled on obj

    Returns
    -------
    obj : vtk.vtkPolyData
        The surface object with the sampled data inside
    """
    np_img = helpers.vtkImageToNumPy(img).astype(np.float)
    spacing = np.asarray(img.GetSpacing())
    orig = np.asarray(img.GetOrigin())
    # Smooth the image and pad it to make easier and better the sampling process
    # np_img = ndimage.binary_dilation(np_img).astype(np_img.dtype)
    np_img = gaussian_filter(np_img, sigma=1)
    np_img = np.pad(np_img, ((5, 5), (5, 5), (5, 5)), 'edge')

    # Resample the data in the geometry
    out = obj.GetOutput()
    points = out.GetPoints()
    npoints = out.GetNumberOfPoints()
    scalars = vtk.vtkFloatArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName('voxel_data')
    for i in range(npoints):
        # Trilinear filtering. See
        # https://en.wikipedia.org/wiki/Trilinear_interpolation
        p = np.asarray(points.GetPoint(i)) - orig
        p /= spacing
        pimg = p.astype(np.int)
        f = p - pimg
        pimg += (5, 5, 5)

        c00 = np_img[pimg[0], pimg[1], pimg[2]] * (1 - f[0]) + \
              np_img[pimg[0] + 1, pimg[1], pimg[2]] * f[0]
        c01 = np_img[pimg[0], pimg[1], pimg[2] + 1] * (1 - f[0]) + \
              np_img[pimg[0] + 1, pimg[1], pimg[2] + 1] * f[0]
        c10 = np_img[pimg[0], pimg[1] + 1, pimg[2]] * (1 - f[0]) + \
              np_img[pimg[0] + 1, pimg[1] + 1, pimg[2]] * f[0]
        c11 = np_img[pimg[0], pimg[1] + 1, pimg[2] + 1] * (1 - f[0]) + \
              np_img[pimg[0] + 1, pimg[1] + 1, pimg[2] + 1] * f[0]
        c0 = c00 * (1 - f[1]) + c10 * f[1]
        c1 = c01 * (1 - f[1]) + c11 * f[1]
        c = c0 * (1 - f[2]) + c1 * f[2]
        if vtk.VTK_MAJOR_VERSION <= 6:
            scalars.InsertNextTupleValue([float(c)])
        else:
            scalars.InsertNextTypedTuple([float(c)])
    out.GetPointData().AddArray(scalars)
    out.GetPointData().SetActiveScalars('voxel_data')

    return out


def __split(surface, value=0.5):
    """Split the image using the sampled data in performed by __sample method.

    Parameters
    ----------
    surface : vtk.vtkPolyData
        Surface where the data should be sampled
    value : scalar
        Scalar to consider the surface should be split

    Returns
    -------
    cutter : vtk.vtkPolyData
        The cutted surface
    complementary : vtk.vtkPolyData
        The complementary surface
    """
    cutter = vtk.vtkClipPolyData()
    if vtk.VTK_MAJOR_VERSION <= 5:
        cutter.SetInput(surface)
    else:
        cutter.SetInputData(surface)
    cutter.GenerateClipScalarsOff()
    cutter.SetValue(0.001)
    cutter.InsideOutOff()
    cutter.GenerateClippedOutputOn()
    cutter.Update()
    return cutter.GetOutput(), cutter.GetClippedOutput()


def surface(cavity, bck, args):
    """Reconstruct the surfaces of the cavity and the background

    Parameters
    ----------
    cavity : vtk.vtkImageData
        VTK image of the cavity
    bck : vtk.vtkImageData
        VTK image of the background
    args : dict
        Program arguments

    Returns
    -------
    wall : vtk.vtkPolyData
        Cavity surface
    face : vtk.vtkPolyData
        face surface
    """
    print('3D reconstruction...')
    # Create a joined data of the whole air domain
    joined = vtk.vtkImageData()
    joined.DeepCopy(cavity)
    np_img = helpers.vtkImageToNumPy(cavity) + helpers.vtkImageToNumPy(bck)
    np_img[np_img > 1] = 1
    helpers.numPyTovtkImage(joined, np_img)
    # Reconstruct the 3D geometry
    obj = __marching_cubes(joined, 1.0 - args.surface_decimation)
    if args.debug:
        helpers.save_surface(obj, 'DBG_006_marching_cubes.vtk')
    # Smooth the geometry
    obj = __smooth(obj,
                   iterations=args.surface_smooth_iters,
                   pass_band=args.surface_smooth_size,
                   feature_angle=None)
    if args.debug:
        helpers.save_surface(obj, 'DBG_007_smooth.vtk')

    # Sample the cavity voxels data in the surface
    mix = vtk.vtkImageData()
    mix.DeepCopy(cavity)
    np_mix = helpers.vtkImageToNumPy(cavity) - helpers.vtkImageToNumPy(bck)
    helpers.numPyTovtkImage(mix, np_mix)
    surface = __sample(obj, mix)
    if args.debug:
        writer = vtk.vtkXMLImageDataWriter()
        writer.SetFileName('DBG_008_sample.vti')
        if vtk.VTK_MAJOR_VERSION <= 5:
            writer.SetInput(mix)
        else:
            writer.SetInputData(mix)
        writer.SetDataModeToBinary()
        writer.Write()
        helpers.save_surface(surface, 'DBG_008_sample.vtk')
    # And use such data to split the objects
    wall, face = __split(surface)
    if args.debug:
        helpers.save_surface(wall, 'DBG_009_wall.vtk')
        helpers.save_surface(face, 'DBG_009_face.vtk')

    return wall, face
