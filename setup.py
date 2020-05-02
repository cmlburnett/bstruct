#from distutils.core import setup
from setuptools import setup

majv = 1
minv = 0

setup(
	name = 'bstruct',
	version = "%d.%d" %(majv,minv),
	description = "Python module that overlays a custom struct onto binary data.",
	author = "Colin ML Burnett",
	author_email = "cmlburnett@gmail.com",
	url = "",
	packages = ['bstruct'],
	package_data = {'bstruct': ['bstruct/__init__.py']},
	classifiers = [
		'Programming Language :: Python :: 3.8'
	],
	test_suite="tests",
)
