#!/bin/bash

## untar modeltest
tar -xzf modeltest_install.tar.gz
## run modeltest
modeltest_install/modeltest/bin/modeltest-ng-static -i CYP75A_MAr05_monocot_OG0000074.fa_filter.fa.aln -t ml -d aa -p 16 
