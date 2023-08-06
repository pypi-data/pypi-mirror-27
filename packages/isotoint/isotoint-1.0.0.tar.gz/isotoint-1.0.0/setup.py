#!/usr/bin/env python3

from os import path
from distutils.core import setup
from Cython.Build import cythonize

def read(relpath):
	with open(path.join(path.dirname(__file__), relpath)) as f:
		return f.read()

setup(
	name = 'isotoint',
	version = read('version.txt').strip(),
	description = 'Convert ISO 8601 string to integer in a microsecond.',
	long_description = read('README.md'),
	author = 'Radek Kysely',
	author_email = 'kyselyradek@gmail.com',
	url = 'https://github.com/kysely/isotoint',
	license = 'MIT',
	ext_modules = cythonize('isotoint/__init__.pyx'),
	keywords = ['iso', 'iso8601', 'integer', 'cython'],
	packages = [
		'isotoint'
	]
)