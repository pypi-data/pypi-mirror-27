# encoding=utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='yekit',
	version='0.1.3',
	description='a useful toolkit',
	long_description=long_description,
	classifiers=[
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python :: 2.7',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
	],
	keywords='tool kit',
	author='ye',
	url='http://www.xuye.site',
	author_email='wmxy123@yeah.net',
	license='BSD',
	packages=find_packages(exclude=['']),  # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
	include_package_data=False,
	zip_safe=True,
	install_requires=[],
)
