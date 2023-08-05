#! /usr/bin/env python
from setuptools import find_packages, setup

version = '0.1.0'

setup(
	name='django-tinycolorpicker',
	packages=find_packages(),
	include_package_data=True,
	version=version,
	license='MIT',
	url='https://www.github.com/perdixsw/django-tinycolorpicker',
	download_url='https://www.github.com/perdixsw/django-tinycolorpicker/archive/%s.tar.gz' % version,
	author='Perdix Software',
	author_email='ssmith@perdixsw.com',
	description='Django Field and Widget implementation of wieringen/tinycolorpicker',
	long_description='Django Field and Widget implementation of wieringen/tinycolorpicker',
	keywords=['django', 'color', 'field', 'colorpicker', 'tinycolorpicker',],
	zip_safe=False,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
