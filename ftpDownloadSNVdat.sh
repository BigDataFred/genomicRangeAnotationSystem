#!/bin/bash


####################
# F.Roux, July 2019
##
# use as: sh ftpDownloadSNVdat.sh "/path/to/save/data/"

savepath=$1
echo ${savepath}

ftp="ftp://ftp.ncbi.nlm.nih.gov/pub/dbVar/data/Homo_sapiens/by_assembly/"
l=$( curl -l ${ftp} )

for tmp in ${l}
do 
ext="/gvf/*"
l2=$(curl -l ${ftp}${tmp}${ext}) 
for tmp2 in ${l2}
do
echo ${tmp2} >> listOfDownloadedFiles.txt
ext="/gvf/"
url=${ftp}${tmp}${ext}${tmp2}
ext="/"
saveName=${savepath}${ext}${tmp2}
#echo "curl ${url} -o ${saveName}" >> ftpDownloadCMD.txt
curl ${url} -o ${saveName} 
done
done

