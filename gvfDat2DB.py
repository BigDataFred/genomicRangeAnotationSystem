 #!/usr/bin/env python
#################################################
import os
import sys
from SNV2db import loadGVFdb
#################################################
# F.Roux, July 2019
##

# use as python gvfDat2DB "/path/to/gvfData/" "/path/to/saveGVFdata/"
p2gvf = sys.argv[1]
savePath = sys.argv[2]

x = os.listdir(p2gvf)
for tmp in x:
    if ( tmp.endswith('.gvf') ): 
        loadGVFdb(p2gvf,tmp,savePath,1)
