# SalmonEuAdmix
## A machine learning-based library for estimating European admixture proportions in Atlantic salmon

Despite never being approved for commercial use in Canada, there is growing evidence of genetic information from European Atlantic salmon entering into  North American aquaculture stocks, with aquaculture escapees subsequently introducing this information into wild populations.  Understanding the extent of European genetic introgression and the impacts it has on wild salmon populations relies on the characterization of European admixture proportions. Obtaining this information using large SNP panels or microsatellite markers can be expensive, analytically intensive, and relies on the inclusion of numerous North American and European individuals to serve as baselines for subsequent analyses.

`SalmonEuAdmix` is a program designed to streamline the admixture estimation process. It allows for European admixture proportions  to be accurately estimated from a parsimonious set of SNP markers. Relying exclusively on the genotypes for the set of SNPs used as input, `SalmonEuAdmix` can predict admixture proportions for novel samples. The program utilizes a machine-learning model trained on pairs of genotypes and admixture proportions for 5812 individuals encompassing a mixture of wild and aquaculture fish of European, North American, and mixed ancestry. The model has been experimentally shown to predict admixture proportions that conform to the estimations provided by a complete admixture analysis with greater than 98% accuracy.


### How does SalmonEuAdmix work?

A run of `SalmonEuAdmix` is invoked via a command line interface. The following workflow takes place to process and analyze the inputs:

1. The program reads a ped and map file.
    - These data files are standard Plink file formats for storing SNP genotype information. More information on them can be found [on the Plink website](https://www.cog-genomics.org/plink/1.9/formats#ped).
	- Your input is permitted to include more SNPs than those required by the model. If there are more SNPs than the selected panel (301-SNP panel is default, larger 513-SNP can be optionally employed), the program subsets just the required SNPs and ignores the others.
2. The program encodes the SNPs for the machine learning model in dosage format.
	- i.e. `AA AT TT` -> `0 1 2`
	- To do this, it uses a stored data structure to ensure the major and minor allele encoding are consistent with the data that were used in training.
3. A Deep neural network trained to predict European Admixture percentage is loaded and used to make predictions. (The models have been shown to be about 99% accurate relative to running a complete admixture run with the same SNPs for ~7000 baseline individuals, you get to skip that part!) 
5. The predictions are output to a tab separated file that is ready for excel/R/human inspection.


## Installation

`SalmonEuAdmix` is a Python3 program, to use it you will need to have [Python3](https://www.python.org/downloads/) installed on your computer. 

### A note on your programming environment
It is recommended, though not required, that you use a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) to install and run `SalmonEuAdmix`. Using a virtual environment allows you to avoid installing Python packages globally which could break system tools or other projects. 

Setting up a virtual environment on Linux or macOS:
```
# you can install virtualenv using pip
pip install virtualenv

# from the command line, make a virtual environment named 'Env'
python3 -m venv Env

# activate the environment
source Env/bin/activate

# now you can install and run SalmonEuAdmix without affecting other projects

# when you're done, deactivate the environment with the command
deactivate
```

Setting up a virtual environment on Windows:
```
# you can install virtualenv using pip
py -m pip install --user virtualenv

# from PowerShell, make a virtual environment named 'Env'
py -m venv Env
#activate the environment 
.\Env\Scripts\activate

# now you can install and run SalmonEuAdmix without affecting other projects

# when you're done, deactivate the environment with the command
deactivate
```

### Linux and macOS - Install via pip

SalmonEuAdmix is available on [pypi](https://pypi.org/project/SalmonEuAdmix/) and can be installed from the terminal using Python's package installer pip.
```
# from terminal, run the command:
pip install SalmonEuAdmix
# check that the installation was successful by calling the help menu
SalmonEuAdmix -h 

```

### Windows - Install via pip

Installing on windows requires a slightly different syntax. The following commands will let you install `SalmonEuAdmix` using PowerShell.
```
# from PowerShell, run the command:
py -m pip install SalmonEuAdmix

# check that the installation was successful by calling the help menu
SalmonEuAdmix -h
```

### Install development version from GitHub

To set up and install `SalmonEuAdmix` from Github, clone this repository (alternatively, you can download and unzip it). 
```
git clone https://github.com/CNuge/SalmonEuAdmix.git
#or if you have your github ssh setup
#git clone git@github.com:CNuge/SalmonEuAdmix.git
```

Then from within the SalmonEuAdmix repository run: 
```
pip install -e .
```
This shoud install the python package and make the command line tool available on your system. You can check the package works by calling the help menu.
```
SalmonEuAdmix -h 
```
From that command you should get an output listing the program's options. From there you're good to start using SalmonEuAdmix!

## Usage 
### Command line interface

Example input files can be found in the subfolder `SalmonEuAdmix/data/`. You can make a copy of these to test the package.

The following command will read in the files `panel_301_data.ped` and `panel_301_data.map` (from your current working directory), run the admixture prediction pipeline, and then output the predicted European admixture proportions for each individual in a file named `example_output.tsv`. If not in your working directory, you can specify the path for the inputs or desired output file location.

```
SalmonEuAdmix -p panel_301_data.ped -m panel_301_data.map -o example_output.tsv

```

The ped (`-p`) and map files (`-m`) are obtained from [plink](https://www.cog-genomics.org/plink/). Note you will more than likely want to use plink or some associated methods to do some pre-processing: filtering for genotype quality, missing data, *etc.*. The 301 SNPs of the panel must all be present in the file, additional marker columns are allowed, and these will simply be filtered out prior to the encoding step.

To see the list of required SNPs, you can look in the example .map file:
`SalmonEuAdmix/data/panel_301_data.map`

You can also view the list of markers from within an interactive Python environment by running the following:
```
from SalmonEuAdmix import panel_snps
panel_snps    # this is a list of the 301 markers in the panel used by the predictive model. All must be present in the input.
```

SalmonEuAdmix can handle low levels of missing information, the modal genotype from the training data will be imputed to fill in missing data. You should explore your data to get a sense of the amount of missing values.

### Alternative model selection
`SalmonEuAdmix` gives you a choice of an additional, larger, neural network for admixture prediction. By default, the 301-SNP model is used, by changing the `--neuralnetwork` flag, you can select between the `301_model` and the `513_model`. The 513_model uses a larger panel of SNPs (all 301 markers are in the 513-SNP panel). If individuals were genotyped for all 513 markers, then the `513_model` will be marginally more accurate in its predictions. 

You can view the list of the larger 513-SNP markers from by running the following from within Python:

```
from SalmonEuAdmix import reduced_panel_snps
reduced_panel_snps    # this is the list of the 513 markers in the reduced panel used by the 513-SNP predictive model.
# All 513 SNPs must be present in the input PED file.
```

Below is an example call using the larger 513-SNP model (files can be found in the subfolder `SalmonEuAdmix/data/`).
```
SalmonEuAdmix -p panel_513_data.ped -m panel_513_data.map -o 513_model_predictions.tsv -n 513_model
```

