#!/usr/bin/env python

from setuptools import setup
try:
    import vtk
except ImportError:
    raise ImportError('VTK cannot be automatically installed by this tool. ' \
                      'Please, install it manually. In Debian systems you ' \
                      'can type \'apt-get install python-vtk\'')
try:
    import vtkgdcm
except ImportError:
    raise ImportError('VTK-GDCM cannot be automatically installed by this ' \
                      'tool. Please, install it manually. In Debian systems '\
                      'you can type \'apt-get install python-vtk\'')


setup(name='nasalgeom',
      version='1.0.0',
      author='Jose Luis Cercos-Pita',
      author_email='jlcercos@gmail.com',
      url='http://www.nasalsystems.com',
      description='A free 3D upper respiratory tract geometry reconstruction ' \
                  'software',
      long_description='NASAL-Geom is a 3D upper respiratory tract geometry ' \
                       'reconstruction software developed by NASAL Systems, ' \
                       'and released as free software under the Affero-GPL ' \
                       'v3 license. With this software you can load ' \
                       'Computerized Tomography (CT) DICOM files and ' \
                       'generate the associated 3D surfaces',
      download_url='https://gitlab.com/sanguinariojoe/nasal-geom.git',
      license='Affero-GPL v3',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='tomography nasal cavity',
      packages=['nasalgeom'],
      scripts=['nasal-geom'],
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pydicom',
          'scikit-image',
          'pyopencl',
          'trimesh',
          'pyopengl'
      ],
     )
