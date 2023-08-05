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
import pyopencl as cl
from . import helpers


def __setup_cl():
    """Create an OpenCL context to start working
 
    By default, the first available GPU will be chosen. If a valid GPU cannot
    be found, the first available accelerated device will be applied.

    Returns
    -------
    dev : cl.Device
        The selected OpenCL device
    ctx : cl.Context
        The OpenCL context
    queue : cl.CommandQueue
        The OpenCL commands queue associated with the device dev
    """
    __platforms = cl.get_platforms()
    if not __platforms:
        print("No available OpenCL platforms! Cone Beam system will not work")
        return None, None, None
    __devices = __platforms[0].get_devices(device_type=cl.device_type.GPU)
    if not __devices:
        __devices = __platforms[0].get_devices(device_type=cl.device_type.ALL)
    if not __devices:
        print("No available OpenCL devices! Cone Beam system will not work")
        return None, None, None
    devs = (__devices[0],)
    ctx = cl.Context(devices=__devices)
    queue = cl.CommandQueue(ctx)
    return devs[0], ctx, queue


def _gaussian(img, size=3, mode='both'):
    """Compute a some sort of Gaussian blur, where a Laplacian edge detection
    is used to exclude the main features of the image from the filtering
    carried out later.

    Parameters
    ----------
    img : ndarray
        The image slice which center value should be convoluted
    size : float
        Standard deviation of the Gaussian function
    mode : {'lap', 'grad', 'both'}
        Select the edge detection algorithm used to discard the areas to become
        smoothed

    Returns
    -------
    value : float
        Filtered image
    """
    # Renormalize the image to work with it
    renormalized, _, _ = helpers.renormalize(img)

    # Compute the smoothing factor
    grad = np.zeros(img.shape)
    lap = np.zeros(img.shape)
    if mode == 'grad' or mode == 'both':
        grad = ndimage.gaussian_gradient_magnitude(renormalized, size)
        grad /= np.max(grad)
    if mode == 'lap' or mode == 'both':
        lap = np.abs(ndimage.gaussian_laplace(renormalized, 1))
        # Smooth a bit the border
        lap = ndimage.gaussian_filter(lap, size)
        lap /= np.max(lap)
    # Drop the noise truncating the values and rescaling
    f = grad + lap
    f /= np.max(f)
    f -= 0.05
    f[f < 0] = 0
    f /= np.max(f)
    # Saturate the edges image
    f = f**(1.0 / 4.0)

    # Gaussian smooth of the original image
    smoothed = ndimage.gaussian_filter(img, size)

    # Return a weighted average image
    return f * img + (1.0 - f) * smoothed


def __bilateral_point(img, sigma_color_f, g, c):
    """Compute a single point of the bilateral filter. See
    https://en.wikipedia.org/wiki/Bilateral_filter
    In this case, the Gaussian spatial kernel is precomputed, so we just need
    to compute the radiosity differences, make the convolution, and renormalize
 
    Parameters
    ----------
    img : ndarray
        The image slice which center value should be convoluted
    sigma_color_f : float
        Standard deviation for grayvalue distance (radiometric similarity)
        factor. It is computed as 1 / (2 * sigma_color**2)
    g : ndarray
        Precomputed Gaussian kernel to carry out the spatial convolution.
    c : list
        Precomputed center of the array
 
    Returns
    -------
    value : float
        Bilateral filter convoluted value
    """
    # Conveniently reshape the image slice
    img = img.reshape(g.shape)
    # Compute the radiosity differences kernel
    I = img[c]
    f = np.exp(- sigma_color_f * (img - I)**2 )
    
    # Perform the convolution
    w = f * g
    return np.sum(img * w) / np.sum(w)


def __bilateral_cpu(img, win_size=None, sigma=2, sigma_color=0.05, output=None,
                    mode='constant', cval=0.0):
    """Denoise the image using a Bilateral filter. See
    https://en.wikipedia.org/wiki/Bilateral_filter

    Bilateral filter may return similar results to Perona-Malik, by a fraction
    of its cost. As a drawback, it needs a significantly bigger interpolation
    window, and therefore larger memory requirements.

    Parameters
    ----------
    img : ndarray
        Image to filter
    win_size : int
        Window size for filtering. If win_size is not specified, it is
        calculated as ceil(3 * sigma), which is enough for normal sigma values.
    sigma : float
        Standard deviation for range distance. A larger value results in
        averaging of pixels with larger spatial differences.
    sigma_color : float
        Standard deviation for grayvalue distance (radiometric similarity). A
        larger value results in averaging of pixels with larger radiometric
        differences. Note, that the image will be renormalized and thus the
        standard deviation is in respect to the range [0, 1].
    output : ndarray
        The output parameter passes an array in which to store the filter
        output.
    mode : {'reflect', 'constant', 'nearest', 'mirror', 'wrap'}
        The mode parameter determines how the array borders are handled, where
        cval is the value when mode is equal to 'constant'. Valid options are
        'reflect', 'constant', 'nearest', 'mirror', 'wrap'
    cval : scalar
        Value to fill past edges of input if mode is 'constant'. Note, that the
        image will be renormalized and thus the standard deviation is in respect
        to the range [0, 1].

    Returns
    -------
    output : ndarray
        Filtered image
    """
    # Renormalize the image
    dtype = img.dtype
    img, cmin, cmax = helpers.renormalize(img, only_positive=True)

    # Get the window size, if it is not provided
    if win_size is None:
        win_size = np.int32(2 * np.ceil(3 * sigma) + 1)
    # Even values are not alowed
    if not np.mod(win_size, 2):
        win_size += 1

    # Setup the Gaussian function footprint
    g = np.zeros([win_size] * img.ndim, dtype=np.float)
    c = [slice(np.int(np.floor(d / 2.)),
               np.int(np.ceil(d / 2.))) for d in g.shape]
    g[c] = 1.0
    g = ndimage.gaussian_filter(g, sigma)
    g /= np.sum(g)

    # Filter the image
    sigma_color_f = 0.5 / sigma_color**2
    output = ndimage.filters.generic_filter(img,
                                            function=__bilateral_point,
                                            size=win_size,
                                            output=output,
                                            mode=mode,
                                            cval=cval,
                                            extra_arguments=(sigma_color_f,
                                                             g,
                                                             c))

    # Denormalize the image
    return (output * (cmax - cmin) + cmin).astype(dtype=dtype)


def __bilateral(img, win_size=None, sigma=2, sigma_color=0.05):
    """Denoise the image using a Bilateral filter. See
    https://en.wikipedia.org/wiki/Bilateral_filter

    Bilateral filter may return similar results to Perona-Malik, by a fraction
    of its cost. As a drawback, it needs a significantly bigger interpolation
    window, and therefore larger memory requirements.

    Parameters
    ----------
    img : ndarray
        Image to filter
    win_size : int
        Window size for filtering. If win_size is not specified, it is
        calculated as ceil(3 * sigma), which is enough for normal sigma values.
    sigma : float
        Standard deviation for range distance. A larger value results in
        averaging of pixels with larger spatial differences.
    sigma_color : float
        Standard deviation for grayvalue distance (radiometric similarity). A
        larger value results in averaging of pixels with larger radiometric
        differences. Note, that the image will be renormalized and thus the
        standard deviation is in respect to the range [0, 1].

    Returns
    -------
    output : ndarray
        Filtered image, None if errors are detected
    """
    dev, ctx, queue = __setup_cl()
    if dev is None or ctx is None or queue is None:
        print("ERROR: No valid OpenCL context found")
        return None

    # Renormalize the image
    dtype = img.dtype
    I_orig, cmin, cmax = helpers.renormalize(img, only_positive=True)
    I_orig = I_orig.astype(dtype=np.float32)
    Nx, Ny, Nz = np.int32(img.shape)
    I_host = I_orig.ravel()

    # Compute the win_size (at least 3 standard deviations). see
    # https://github.com/scikit-image/scikit-image/issues/1955
    if win_size is None:
        win_size = np.int32(2 * np.ceil(3 * sigma) + 1)

    # Correct the data types for OpenCL (we are also conveneintly computing
    # sigma factors as they are used in the equation)
    win_radius = np.int32((win_size - 1) / 2)
    sigma = np.float32(0.5 / sigma**2)
    sigma_color = np.float32(0.5 / sigma_color**2)

    # Check and allocate memory (conveniently spliting the work by pieces)
    mem = dev.get_info(cl.device_info.GLOBAL_MEM_SIZE)
    # We need at least 3 aid memory objects, and we want to ensure memory
    # enough will be available (0.25 safety factor)
    mem_per_obj = mem / (3 * 4)
    # However, we cannot tolerate more than 256MB of contiguous memory (0.5
    # safety factor)
    if mem_per_obj > 128 * 1024 * 1024:
        mem_per_obj = 128 * 1024 * 1024
    # Also, due to the intensive work load, we should not accept the computation
    # of more than 2^19 interactions per thread
    if mem_per_obj * (win_radius**img.ndim) / I_host.dtype.itemsize > 1<<19:
        mem_per_obj = (1<<19) / (win_radius**img.ndim) * I_host.dtype.itemsize

    bytes_per_obj = I_host.nbytes
    slices = [1, 1, 1]
    while bytes_per_obj > mem_per_obj:
        # Compute the next less intrusive divisor
        candidates = []
        for i in range(3):
            if slices[i] == img.shape[i]:
                candidates.append(np.iinfo(np.int32).max)
                continue
            candidate = slices[i] + 1
            while img.shape[i] % candidate:
                candidate += 1
            candidates.append(candidate)
        i = np.argmin([candidates[i] - slices[i] for i in range(3)])
        slices[i] = candidates[i]
        bytes_per_obj = I_host.nbytes / np.prod(slices)
    nx = np.int32(Nx / slices[0])
    ny = np.int32(Ny / slices[1])
    nz = np.int32(Nz / slices[2])
    # Allocate the main memory object. We need win_radius additional layers of
    # elements per bound
    bytes_per_obj = (nx + 2 * win_radius) * \
                    (ny + 2 * win_radius) * \
                    (nz + 2 * win_radius) * I_host.dtype.itemsize
    I = cl.Buffer(ctx, cl.mem_flags.READ_ONLY, bytes_per_obj)
    bytes_per_obj = nx * ny * nz * I_host.dtype.itemsize
    I_out = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)
    shepard = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)

    # Load the program
    f = open(os.path.join(os.path.dirname(__file__), 'bilateral.cl'), 'r')
    src = f.read()
    f.close()
    del f
    prg = cl.Program(ctx, src).build()
    del src

    # Start the process by packages
    # Create a conveniently expanded version of the image to can read "out of
    # bounds"
    I_expanded = np.lib.pad(I_orig, win_radius, mode='wrap')
    pbar = helpers.ProgressBar()
    for i in range(slices[0]):
        for j in range(slices[1]):
            for k in range(slices[2]):
                slice_id = 1 + k + j * slices[2] + i * slices[2] * slices[1]
                pbar.update(float(slice_id) / np.prod(slices))

                # Get the slice of the image
                i0 = np.int32(i * nx)
                j0 = np.int32(j * ny)
                k0 = np.int32(k * nz)
                I_slice = I_expanded[i0:i0 + nx + 2 * win_radius,
                                     j0:j0 + ny + 2 * win_radius,
                                     k0:k0 + nz + 2 * win_radius].flatten()
                # Send the data to the buffer
                # cl.enqueue_write_buffer(queue, I, I_slice).wait()
                cl.enqueue_copy(queue, I, I_slice).wait()
                # Execute the task
                prg.interpolate(queue, (int(nx), int(ny), int(nz)), None,
                                I, I_out, shepard, nx, ny, nz,
                                sigma, sigma_color, win_radius)
                prg.renormalize(queue, (int(nx), int(ny), int(nz)), None,
                                I_out, shepard, nx, ny, nz)
                # Write the output on the original image
                I_slice = np.zeros(nx * ny * nz, dtype=np.float32)
                queue.finish()
                # cl.enqueue_read_buffer(queue, I_out, I_slice).wait()
                cl.enqueue_copy(queue, I_slice, I_out).wait()

                I_slice = I_slice.reshape(nx, ny, nz)
                I_orig[i0:i0 + nx, j0:j0 + ny, k0:k0 + nz] = \
                    np.copy(I_slice)

    # Denormalize the image
    return (I_orig * (cmax - cmin) + cmin).astype(dtype=dtype)


def __maiseli_step(queue, I, Ix, Iy, Iz, c, dIdt, nx, ny, nz, prg, ht,
                   beta, lamb):
    """Performs a single time step of the Maiseli filter for a single working
    package.

    Parameters
    ----------
    I : ndarray
        Image to become smoothed
    Ix : ndarray
        Partial derivative in x direction
    Iy : ndarray
        Partial derivative in y direction
    Iz : ndarray
        Partial derivative in z direction
    c : ndarray
        Conductivity factor (depending on gradient, to preserve edges)
    dIdt : ndarray
        Time derivative of the image
    nx : int
        Size of the package in x direction
    ny : int
        Size of the package in y direction
    nz : int
        Size of the package in z direction
    prg : cl-Program
        OpenCL program to become executed
    ht : float
        Time step
    beta : float
        Beta factor
    lamb : float
        Lambda regularization factor
    """
    # Compute the gradient of the image, (Ix, Iy, Iz)
    prg.grad(queue, (nx + 2, ny + 2, nz + 2), None,
             I, Ix, Iy, Iz, nx, ny, nz)
    # Compute the conductivity factor
    prg.c(queue, (nx + 2, ny + 2, nz + 2), None,
          Ix, Iy, Iz, c, nx, ny, nz, beta)
    shape = (int(nx), int(ny), int(nz))  # Conversion error fix
    # Compute the time derivative
    prg.dIdt_stage1(queue, shape, None,
                    Ix, Iy, Iz, c, dIdt, nx, ny, nz)
    prg.dIdt_stage2(queue, shape, None,
                    Ix, Iy, Iz, c, dIdt, nx, ny, nz)
    # Integrate in time
    prg.time_step(queue, shape, None,
                  dIdt, I, nx, ny, nz, ht)    


def __maiseli(img, nstep=20):
    """Denoise the image using a Maiseli filter. See
    https://en.wikipedia.org/wiki/Anisotropic_diffusion

    An improved version of the Perona-Malik filter, which may significantly
    improve the noise suppression and edge preserving features, such that it
    make a difference with in extremely noisy images.

    Parameters
    ----------
    img : ndarray
        Image to filter
    nstep : int
        The maximum number of time steps to carry out (It may stop before
        depending on the convergence).

    Returns
    -------
    output : ndarray
        Filtered image, None if errors are detected
    """
    dev, ctx, queue = __setup_cl()
    if dev is None or ctx is None or queue is None:
        print("ERROR: No valid OpenCL context found")
        return None

    # Renormalize the image
    dtype = img.dtype
    I_orig, cmin, cmax = helpers.renormalize(img, only_positive=True)
    I_orig = I_orig.astype(dtype=np.float32)
    Nx, Ny, Nz = np.int32(img.shape)
    I_host = I_orig.ravel()

    # Get the time step
    ht = np.float32(0.5 / img.ndim**2)

    # Parameters. beta should be bigger than
    # np.float32(2.0 / (1.0 + np.sqrt(5.0))) * grad(u), where grad(u) is the
    # maximum gradient expectable (theoretically around 0.5)
    beta = np.float32(0.01)
    lamb = np.float32(0.0)

    # Check and allocate memory (conveniently spliting the work by pieces)
    mem = dev.get_info(cl.device_info.GLOBAL_MEM_SIZE)
    # We need at least 6 aid memory objects, and we want to ensure memory
    # enough will be available (0.25 safety factor)
    mem_per_obj = mem / (6 * 4)
    # However, we cannot tolerate more than 256MB of contiguous memory (0.5
    # safety factor)
    if mem_per_obj > 128 * 1024 * 1024:
        mem_per_obj = 128 * 1024 * 1024
    # Also, due to the intensive work load, better to impose a limit on the
    # number of threads per wave
    if mem_per_obj / I_host.dtype.itemsize > 1<<15:
        mem_per_obj = I_host.dtype.itemsize * 1<<15

    bytes_per_obj = I_host.nbytes
    slices = [1, 1, 1]
    while bytes_per_obj > mem_per_obj:
        # Compute the next less intrusive divisor
        candidates = []
        for i in range(3):
            if slices[i] == img.shape[i]:
                candidates.append(np.iinfo(np.int32).max)
                continue
            candidate = slices[i] + 1
            while img.shape[i] % candidate:
                candidate += 1
            candidates.append(candidate)
        i = np.argmin([candidates[i] - slices[i] for i in range(3)])
        slices[i] = candidates[i]
        bytes_per_obj = I_host.nbytes / np.prod(slices)
    nx = np.int32(Nx / slices[0])
    ny = np.int32(Ny / slices[1])
    nz = np.int32(Nz / slices[2])

    # Allocate the main memory object. We need two additional layers of
    # elements per bound
    bytes_per_obj = (nx + 4) * (ny + 4) * (nz + 4) * I_host.dtype.itemsize
    I = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)
    # Allocate the transitional memory objects. We need one additional
    # element per bound in the memory objects which its gradient is required
    # later
    bytes_per_obj = (nx + 2) * (ny + 2) * (nz + 2) * I_host.dtype.itemsize
    Ix = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)
    Iy = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)
    Iz = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)
    c = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)
    bytes_per_obj = nx * ny * nz * I_host.dtype.itemsize
    dIdt = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, bytes_per_obj)

    # Load the program
    f = open(os.path.join(os.path.dirname(__file__), 'maiseli.cl'), 'r')
    src = f.read()
    f.close()
    del f
    prg = cl.Program(ctx, src).build()
    del src

    # Start the process by packages
    pbar = helpers.ProgressBar()
    for s in range(nstep):
        # Create a conveniently expanded version of the image to can read "out of
        # bounds"
        I_expanded = np.lib.pad(I_orig, 2, mode='wrap')
        error = 0.0
        for i in range(slices[0]):
            for j in range(slices[1]):
                for k in range(slices[2]):
                    slice_id = 1 + k + j * slices[2] + i * slices[2] * slices[1]
                    pbar.update((s + float(slice_id) / np.prod(slices)) / nstep)
                    # Get the slice of the image
                    i0 = np.int32(i * nx)
                    j0 = np.int32(j * ny)
                    k0 = np.int32(k * nz)
                    I_slice = I_expanded[i0:i0 + nx + 4,
                                         j0:j0 + ny + 4,
                                         k0:k0 + nz + 4].flatten()
                    # Send the data to the buffer
                    cl.enqueue_write_buffer(queue, I, I_slice)
                    # Execute the task
                    __maiseli_step(queue, I, Ix, Iy, Iz, c, dIdt,
                                   nx, ny, nz, prg, ht, beta, lamb)
                    # Write the output on the original image
                    cl.enqueue_read_buffer(queue, I, I_slice).wait()
                    I_slice = I_slice.reshape(nx + 4, ny + 4, nz + 4)
                    I_orig[i0:i0 + nx, j0:j0 + ny, k0:k0 + nz] = \
                        I_slice[2:nx + 2, 2:ny + 2, 2:nz + 2]
                    # Get the error
                    e = np.max(np.abs(I_slice - I_expanded[i0:i0 + nx + 4,
                                                           j0:j0 + ny + 4,
                                                           k0:k0 + nz + 4]))
                    error = np.max((error, e))
                    # print(error)
        if error < 0.5E-3:
            break
    pbar.update(1.0)

    # Recover the image in the original initial colourfield
    return (I_orig * (cmax - cmin) + cmin).astype(dtype=dtype)


def denoise(vtk_img, args):
    """Performs the queried smoothing stages:

    * Median filter (https://en.wikipedia.org/wiki/Median_filter). This filter
      is pretty similar to a Gaussian filter, but has better edge preserving
      features. It is a little bit expensive in computational terms.
    * Gaussian blur (https://en.wikipedia.org/wiki/Gaussian_blur). In order to,
      add preserving edge capabilities, a Laplacian based edge detection is
      performed before to mask the areas which should not become affected by the
      filter. Good results can be obtained from the combination of this filter
      with the median one, with a relatively low computational cost
    * Bilateral filter (https://en.wikipedia.org/wiki/Bilateral_filter). Pretty
      similar to the Gaussian blur, this filter carry out a weighted
      interpolation where the weight is taken into account the distance but also
      color intensity differences.
    * Perona-Malik (https://en.wikipedia.org/wiki/Anisotropic_diffusion). The
      first filter built on top of a diffusion equation. This filter has good
      properties. However, due to the converging process it is very expensive.
      Probably you should consider the Maiseli filter instead.
    * Maiseli (http://www.sciencedirect.com/science/article/pii/S0923596515000363)
      This filter is an improvement of the Perona-Malik one, designed to improve
      the edge preserving features. It is as many costly as the Perona-Malik,
      but better results can be expected. You can consider this filter for
      extremely noisy images, like Cone-Beam tomography ones.

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
    img_orig = helpers.vtkImageToNumPy(vtk_img)
    img = np.copy(img_orig)
    # Clip extremely large and low values, which may dramatically decrease the
    # quality of the filtered images
    img[img < -3000] = -3000
    img[img > 7000] = 7000

    if args.smooth_median:
        print('Median filter...')
        img = ndimage.filters.median_filter(img, size=3)
        if args.debug:
            helpers.print_dicom(img,
                                'DBG_002a_median',
                                cmin=-1000.0,
                                cmax=1000.0)
    if args.smooth_gaussian:
        print('Gaussian filter...')
        img = _gaussian(img, size=3)
        if args.debug:
            helpers.print_dicom(img,
                                'DBG_002b_gaussian',
                                cmin=-1000.0,
                                cmax=1000.0)
    if args.smooth_bilateral:
        print('Bilateral filter...')
        img_out = __bilateral(img)
        if img_out is None:
            print('Falling back to CPU...')
            img_out = __bilateral_cpu(img)
        img = img_out
        if args.debug:
            helpers.print_dicom(img,
                                'DBG_002c_bilateral',
                                cmin=-1000.0,
                                cmax=1000.0)
    if args.smooth_maiseli:
        print('Maiseli filter...')
        img_out = __maiseli(img)
        # img_out = np.copy(img)
        if img_out is None:
            print('Ignoring this filter!')
        else:
            img = img_out
            if args.debug:
                helpers.print_dicom(img,
                                    'DBG_002e_maiseli',
                                    cmin=-1000.0,
                                    cmax=1000.0)

    img = args.smooth_factor * img + (1.0 - args.smooth_factor) * img_orig
    if args.debug:
        helpers.print_dicom(img,
                            'DBG_002_smoothed',
                            cmin=-1000.0,
                            cmax=1000.0)

    helpers.numPyTovtkImage(vtk_img, img)
    return vtk_img
