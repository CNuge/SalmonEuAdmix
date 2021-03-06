from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()
	requirements = [x.rstrip() for x in requirements]

long_description = """
SalmonEuAdmix: a machine learning-based library for estimating European admixture proportions in Atlantic salmon. 

SalmonEuAdmix is a program designed to streamline the admixture estimation process, 
and allow for European admixture proporions to be accurately estimated from a 
parsimonious set of SNP markers. Relying exlusively on the genotypes for the set 
of SNPs as input, SalmonEuAdmix can predict admixture proporions for novel samples. 
The program utilizes a machine-learning model trained on pairs of genotypes and 
admixture proportions for 5812 individuals encompassing a mixture of wild and 
aquaculture fish of European, North American, and mixed ancestry. The model has 
been experimentally show to predict admixture proportions that conform to the 
estimations provided by a complete admixture analysis with greater than 98 percent accuracy.
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