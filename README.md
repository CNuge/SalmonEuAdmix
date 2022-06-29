# SalmonEuAdmix
## A machine learning-based library for estimating European admixture proportions in Atlantic salmon

### detailed description here, copy into setup.py

### what is it doing? (A bunch of backgroud detail abstracted away into that one command):

1. reads the ped and map files
	-if there are more SNPs than the panel, it subsets just the required SNPs
2. Encodes the SNPs for the machine learning model
	- i.e. `AA AT TT` -> `0 1 2`
	- is uses a stored data structure so that the Major and Minor encoding is consistent with previous
3. Loads a Deep neural network trained to predict European Admixture % (its been shown to be about 99% accurate relative to running a complete from scratch ).
4. Applies scalers to interface with the neural network, runs the DNN to make predictions
5. Spits the data to an output file ready for excel/R/human inspection.



## Installation

```
create the release:
python setup.py sdist
install the release:
python3 setup.py install

#then check from home dir if the package works with
SalmonEuAdmix -h
```

## Usage 
### Command line interface

Get the help menu:
```
SalmonEuAdmix -h
```

Run the neural network to predict european admixture for a series of genotyped individuals.
Example inputs can be found in the subfolder SalmonEuAdmix/data/
The following will read in the panel_513_data .ped and .map files, run the admixture prediction pipeline and then output the predicted european admixture proportions for each individual in the file `example_output.tsv`

```
SalmonEuAdmix -p panel_513_data.ped -m panel_513_data.map -o example_output.tsv

```

Where the ped and the map file are obtained from [plink](https://www.cog-genomics.org/plink/). Note you'll probably want to do some pre-filtering for gentype quality. The 513 SNPs of the panel must all be present in the file, additional marker columns are allowed, and these will simply be filtered out prior to the encoding

To see the list of required SNPs, you can look in the example .map file:
`SalmonEuAdmix/data/panel_513_data.map`

or from within python run:
```
from SalmonEuAdmix import panel_snps
panel_snps    # this is a list of the 513 markers in the panel used by the predictive model. All must be present.
```

SalmonEuAdmix can handle low levels





## TODO
- add documentation to all functions
    - need to fill in the docstrings
    - verbose typing of outputs?
- add a license
- make sure unit tests cover all the functions
- verbose documents for the argument parser.
- add a header == true or false line to the PED parser
- add travis.ci to display the unit tests.
- I've killed the tflite, it complicates the code far too much for the few mb size savings
    - [x] make a shrunken version of the DNN
        -[x] convert the DNN to tflite to make it smaller
        -make sure the tflite and regular agree (TODO)
        -sub out the requirements and try to eliminate the tensorflow dependency
            ^go back to paper repo, and sub in the finished product. (see desktop for starting code)
            - keep just one or the other
                - If using the tflite, need to add an iterative predict function. It won't bulk predict on a matrix of multiple inputs
- silence any tf command line warnings
- cleanup / eliminate the main sections of module files (these are start of unit tests)
- *IMPORTANT ADD*
    - add the mode values to the SNP_major_minor_info.pkl?
        - want the imputation based on the training data, not based off of the new data
            - could have a param added to enable either.
- make it pip installable?
- lint the code to get you spacing and formatting pretty and proper