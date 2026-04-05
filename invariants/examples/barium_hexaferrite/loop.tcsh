#!/bin/tcsh
# Original script for reference — superseded by isoinv.py
# Variable naming and sed substitution approach used before this tool existed.

set irrep_labels = 'GM2- GM6- GM2+ GM6+ A1'

# edit input file
sed    "s/irrep_labels/$irrep_labels/g" iso_input > iso_input_test
sed -i "s/order/1 7/g" iso_input_test

# run isotropy to get invariant polynomial and prep for Mathematica input
iso < iso_input_test > iso_output_temp
sed -i "s/n1/(Pz)/g"   iso_output_temp
sed -i "s/n2/(Px)/g"   iso_output_temp
sed -i "s/n3/(Py)/g"   iso_output_temp
sed -i "s/n4/(Mz)/g"   iso_output_temp
sed -i "s/n5/(Mx)/g"   iso_output_temp
sed -i "s/n6/(My)/g"   iso_output_temp
sed -i "s/n7/(A1a)/g"  iso_output_temp
sed -i "s/n8/(A1b)/g"  iso_output_temp
tail -n +8 iso_output_temp | head -n -1 > iso_output_test
