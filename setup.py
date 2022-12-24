from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np

sourcefiles = ['get_data_c.pyx']

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("get_data_c", sourcefiles, include_dirs=[np.get_include()])],
)