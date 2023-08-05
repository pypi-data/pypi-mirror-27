#!/bin/bash

##########
# qordoba-string-extractor.sh
#
# Script that generates a csv file containing the location of all string literals in the given file or directory.
#
# Usage: qordoba-string-extractor.sh [options]
#
#   -d, --input directory <directory>
#                           input directory is a required argument
#   -i, --infile <file>      infile is a required argument
#   -o, --outfile <file>     outfile is a required argument
#   -v, --verbose            verbose is a flag
#   --help                   prints this usage text
#
##########

ARGS=$@

cd /string-extractor

# e.g.: sbt "run -d src/test/resources/python -o python-string-literals.csv"
sbt "run $ARGS"

