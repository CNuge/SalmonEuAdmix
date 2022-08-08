# SalmonEuAdmix
## A machine learning-based library for estimating European admixture proportions in Atlantic salmon

Despite never being approved for commercial use in Canada, there is growing evidence of genetic information from European Atlantic salmon entering into both North American aquaculture stocks, with aquaculture escapees subsequently introducing this information into wild populations.  Understanding the extent of European genetic introgression and the impacts it has on wild salmon populations relies on the characterization of European admixture proportions. Obtaining this information using large SNP panels or microsatellite markers can be expensive, analytically intensive, and relies on the inclusion of numerous North American and European individuals to serve as baselines for subsequent analyses.

`SalmonEuAdmix` is a program designed to streamline the admixture estimation process. It allows for European admixture proporions to be accurately estimated from a parsimonious set of SNP markers. Relying exlusively on the genotypes for the set of SNPs used as input, `SalmonEuAdmix` can predict admixture proporions for novel samples. The program utilizes a machine-learning model trained on pairs of genotypes and admixture proportions for 5812 individuals encompassing a mixture of wild and aquaculture fish of European, North American, and mixed ancestry. The model has been experimentally shown to predict admixture proportions that conform to the estimations provided by a complete admixture analysis with greater than 98% accuracy.


### How does SalmonEuAdmix work?

A run of `SalmonEuAdmix` is invoked via a command line interface. The following workflow takes place to process and analyze the inputs:

1. The program reads a ped and map file.
    - These data files are standard Plink file formats for storing SNP genotype information. More information on them can be found [on the Plink website](https://www.cog-genomics.org/plink/1.9/formats#ped).
	- Your input is permitted to include more SNPs than those required by the model. If there are more SNPs than the panel, the program subsets just the required SNPs and ignores the others.
2. The program encodes the SNPs for the machine learning model in dosage format.
	- i.e. `AA AT TT` -> `0 1 2`
	- To do this, it uses a stored data structure to ensure the major and minor allele encoding are consistent with the data that were used in training.
3. A Deep neural network trained to predict European Admixture percentage (it has been shown to be about 99% accurate relative to running a complete from scratch) is loaded and used to make predictions.
5. The predictions are output to a tab separated file that is ready for excel/R/human inspection.



## Installation

To set up `SalmonEuAdmix`, clone this repository, and then from within the folder run the following commands:

```
# create the release:
python setup.py sdist
# install the release:
python3 setup.py install

# then check if the package works by calling the help menu
SalmonEuAdmix -h
```

## Usage 
### Command line interface

Example input files can be found in the subfolder `SalmonEuAdmix/data/`
The following command will read in the `panel_513_data.ped` and `panel_513_data.map` files, run the admixture prediction pipeline and then output the predicted european admixture proportions for each individual in a file named `example_output.tsv`.

```
SalmonEuAdmix -p panel_513_data.ped -m panel_513_data.map -o example_output.tsv

```

The ped (`-p`) and map files (`-m`) are obtained from [plink](https://www.cog-genomics.org/plink/). Note you will more than likely want to use plink or some associated methods to do some pre-processing, filtering for genoltype quality, missing data, *etc.*. The 513 SNPs of the panel must all be present in the file, additional marker columns are allowed, and these will simply be filtered out prior to the encoding step.

To see the list of required SNPs, you can look in the example .map file:
`SalmonEuAdmix/data/panel_513_data.map`

You can also view the list of markers from within python run the following:
```
from SalmonEuAdmix import panel_snps
panel_snps    # this is a list of the 513 markers in the panel used by the predictive model. All must be present in the input.
```

SalmonEuAdmix can handle low levels of missing information, the modal genotype from the training data will be imputed to fill in missing data.  


