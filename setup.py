#!/usr/bin/env python3

from setuptools import setup, find_packages
import os.path

setup(
	name='alcf',
	version='1.0.0-beta.1',
	description='Automatic Lidar and Ceilometer Framework (ALCF)',
	author='Peter Kuma, Adrian J. McDonald, Olaf Morgenstern, Richard Querel, Israel Silber, Connor J. Flynn',
	author_email='peter@peterkuma.net',
	license='MIT',
	scripts=['bin/alcf', 'bin/cosp_alcf'],
	packages=find_packages(),
	zip_safe=False,
	package_data={'alcf': [
		os.path.join('..',p,f)
		for p,_,fs in os.walk('alcf/opt')
		for f in fs
	]},
	install_requires=[
		'numpy',
		'scipy',
		'matplotlib',
		'netCDF4>=1.2.9',
		'cl2nc',
	],
	keywords=['alc', 'ceilometer', 'lidar', 'atmosphere', 'model', 'simulator', 'nwp', 'gcm', 'cosp', 'actsim', 'vaisala', 'cl51', 'cl31', 'lufft', 'chm-15k', 'minimpl', 'amps', 'merra-2', 'um'],
	url='https://alcf-lidar.github.io',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 3',
		'Programming Language :: Fortran',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
		'Topic :: Scientific/Engineering :: Physics',
		'Topic :: Scientific/Engineering :: Visualization',
	]
)
