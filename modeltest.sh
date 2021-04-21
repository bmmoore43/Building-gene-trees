#!/bin/bash

## untar modeltest
tar -xzf modeltest_install.tar.gz
## run modeltest
modeltest_install/modeltest/bin/modeltest-ng-static -i $1 -t ml -d aa -p 16 
