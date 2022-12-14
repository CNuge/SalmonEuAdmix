from setuptools import setup, find_packages

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
	version = '1.0.6',
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
	install_requires = ["numpy>=1.20.3",
						"pandas>=1.3.4",
						"tensorflow>=2.8.0",
						"scikit-learn>=0.24.2",
						"pytest==6.2.4"]

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


Systems I've tested the install and a small demo run on:
- Linux, Ubuntu 18.04.4, python 3.8.5 (in a virtual environment)
	- all model situations worked as expected.
- Compute Canada VM, Linux, python 3.8.10 (in a virtual environment)
	- all model situations worked as expected.
	- needed to install cython on compute canada, think this is a .whl nuance for them
- Windows 11, windows subsystem for linux
	- native environment for the package
- Windows 11, powershell
	- works, needed to change the model save from pkl to native tf format, but all is well now.

"""