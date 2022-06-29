# SalmonEuAdmix
## A machine learning-based library for estimating European admixture proportions in Atlantic salmon

### detailed description here, copy into setup.py

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

get the help menu
```
SalmonEuAdmix -h
```



## TODO
- add documentation to all functions
- add liscence
- add unit tests to cover the functions
- add description of how to install and use the model
- verbose documents for the argument parser.
- add a header == true or false line to the PED parser
- add travis.ci to display the unit tests.
- run install test and make sure the predictions are what is expected.
    ^pull lines from the paper results corresponding to the fish in the example file, make sure the predictions match.

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
