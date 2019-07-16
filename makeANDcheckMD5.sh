#!/bin/bash


####################
# F.Roux, June 2019
##
# use as: sh makeANDcheckMD5.sh "/Volumes/Toshiba3Tb/"

p2gz=$1
echo ${p2gz}
f=$( ls ${p2gz}*.gz )
for i in ${f}
do 
echo ${i} 
cs1=$( md5 ${i} ) 
echo ${cs1} >> checksumListGZ1.txt
cs2=$(cat ${i}".md5")
echo ${cs2} >> checksumListGZ2.txt
done

cs1=$( cat checksumListGZ1.txt | awk -F '=' '{print $2}' ) 
cs2=$( cat checksumListGZ2.txt | awk -F ' ' '{print $1}' )

rm "checksumListGZ1.txt"
rm "checksumListGZ2.txt"

for i in ${cs1}
do 
echo ${i} >> checksumListGZ1.txt
done

for i in ${cs2}
do 
echo ${i} >> checksumListGZ2.txt
done


chck=$( diff checksumListGZ1.txt checksumListGZ2.txt | wc -c )

echo ${chck}" differences were found between checksumListGZ1.txt & checksumListGZ2.txt"