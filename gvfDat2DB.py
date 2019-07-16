 #!/usr/bin/env python
#################################################
import os
from SNV2db import loadGVFdb
#################################################
# F.Roux, June 2019
##

p2gvf = "/Volumes/Toshiba3Tb/"
x = os.listdir(p2gvf)
for tmp in x:
    if ( tmp.endswith('.gvf') ): 
        print(tmp)
        loadGVFdb(p2gvf,tmp,1)