from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()
	requirements = [x.rstrip() for x in requirements]

long_description = """
SalmonEuAdmix: a machine learning-based library for estimating European admixture proportions in Atlantic salmon. 

TODO - Add a detailed description here.
"""


setup(
	name = 'SalmonEuAdmix',
	version = '1.0.0',
	author = 'Cam Nugent',
	author_email = 'Cameron.Nugent@dfo-mpo.gc.ca',
	url = 'https://github.com/CNuge/SalmonEuAdmix',
	description = 'Estimating European admixture proportions in Atlantic salmon',
	long_description = long_description,
	license= 'LICENSE.md',
	packages = find_packages(),
	package_data={'SalmonEuAdmix': ['data/*']},
	entry_points = {
	'console_scripts':[
	'SalmonEuAdmix = SalmonEuAdmix.cli:main']
	},
	python_requires='>=3.9.7',
	install_requires = requirements,

	)


"""
create the release:
python setup.py sdist
install the release:
python3 setup.py install

#then check from home dir if the package works with
SalmonEuAdmix -h

#can check to see if functions available with:
from SalmonEuAdmix.encode import encode_ped
?encode_ped
"""