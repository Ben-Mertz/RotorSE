#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
import platform


setup(
    name='RotorSE',
    version='0.1.0',
    description='Rotor Systems Engineering Model',
    author='S. Andrew Ning',
    author_email='andrew.ning@nrel.gov',
    install_requires=['commonse', 'ccblade', 'pbeam'],
    package_dir={'': 'src'},
    packages=['rotorse','rotorse.test','rotorse.5MW_AFFiles','rotorse.5MW_PreCompFiles'],
    license='Apache License, Version 2.0',
    dependency_links=['https://github.com/byuflowlab/CCBlade-1/tarball/master#egg=ccblade',
        'https://github.com/WISDEM/pBEAM/tarball/master#egg=pbeam',
        'https://github.com/WISDEM/CommonSE/tarball/openmdao1#egg=commonse'],
    zip_safe=False
)


from numpy.distutils.core import setup, Extension
setup(
    name='precomp',
    package_dir={'': 'src/rotorse'},
    ext_modules=[Extension('_precomp', ['src/rotorse/PreCompPy.f90'], extra_compile_args=['-O2'])],
)

if platform.system() == 'Windows':
		setup( 
		    name='curvefem', 
		    package_dir={'': 'src/rotorse'}, 
		    ext_modules=[Extension('_curvefem', ['src/rotorse/CurveFEMPy.f90'], 
		        extra_compile_args=['-O2'], 
		        include_dirs=[''], 
		        library_dirs=['C:/lapack'], 
		        libraries=['lapack'] 
		        )], 
		) 
elif platform.system() == 'Darwin':
    setup(
        name='curvefem',
        package_dir={'': 'src/rotorse'},
        ext_modules=[Extension('_curvefem', ['src/rotorse/CurveFEMPy.f90'], extra_compile_args=['-O2'])])
else:
    setup(
        name='curvefem',
        package_dir={'': 'src/rotorse'},
        ext_modules=[Extension('_curvefem', ['src/rotorse/CurveFEMPy.f90'], extra_compile_args=['-O2'],
                               libraries=['lapack'])])

