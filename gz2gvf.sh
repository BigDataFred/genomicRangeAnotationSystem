#!/bin/bash


####################
# F.Roux, July 2019
##
# use as: sh gz2gvf.sh 

p2gz=$1
echo ${p2gz}
f=$( ls ${p2gz}*.gz )
for i in ${f}
do 
echo ${i} 
#echo "gunzip ${i}"
gunzip ${i}
done
