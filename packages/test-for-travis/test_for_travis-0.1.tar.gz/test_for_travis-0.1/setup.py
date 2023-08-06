#!/usr/bin/env python
#coding: utf-8

from setuptools import setup

setup(
	name = 'test_for_travis',
	version = '0.1',
	author = 'wph',
	author_email = 'wangpenghui@gene.ac',
	url = 'https://testupload.test',
	description = 'test how to submit a project to pypi and test how to use the travis',
	packages = ['test_for_travis'],
	install_requires = [],
	entry_points = {
		'console_scripts':[
			'uploadpy = test_for_travis:uploadpy',
			'pypy = test_for_travis:pypy'
		]
	}
)
