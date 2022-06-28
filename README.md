# SalmonEuAdmix
## A machine learning-based library for estimating European admixture proportions in Atlantic salmon

### detailed description here, copy into setup.py

## Installation
TODO - fill


## Usage 
### Command line interface
TODO - fill


## TODO
- add documentation to all functions
- add unit tests to cover the functions
- add description of how to install and use the model
- verbose documents for the argument parser.
- test the install and execution
    - make sure requirements work as expected
- add travis.ci to display the unit tests.
- run install test and make sure the predictions are what is expected.
    ^pull lines from the paper results corresponding to the fish in the example file, make sure the predictions match.
- make a shrunken version of the DNN
    -convert the DNN to tflite to make it smaller
    -make sure the tflite and regular agree (TODO)
    -sub out the requirements and try to eliminate the tensorflow dependency
        ^go back to paper repo, and sub in the finished product. (see desktop for starting code)
        - keep just one or the other
- silence any tf command line warnings
-cleanup / eliminate the main sections of module files (these are start of unit tests)