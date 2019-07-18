#!/bin/bash

####################
# F.Roux, July 2019
##
# use as: sh optimizeQueries.sh 

# measure duration of query before optimized
START=$(date +%s.%N)
echo "SELECT variant_id FROM GRCh37_variant_call_gvf WHERE outer_start >= 15000 AND outer_end <=350000;" | sqlite3 snvDB.db
END=$(date +%s.%N)
DIFF1=$(echo "$END - $START" | bc)

# create index for optim queries
echo "CREATE INDEX optimGenomRange ON GRCh37_variant_call_gvf (outer_start,outer_start);" | sqlite3 snvDB.db

# check that query has been optim
echo "EXPLAIN QUERY PLAN SELECT * FROM GRCh37_variant_call_gvf WHERE outer_start >= 15000 AND outer_start <=350000;" | sqlite3 snvDB.db

# measure duration of query after optim
START=$(date +%s.%N)
echo "SELECT variant_id FROM GRCh37_variant_call_gvf WHERE outer_start >= 15000 AND outer_end <=350000;" | sqlite3 snvDB.db
END=$(date +%s.%N)
DIFF2=$(echo "$END - $START" | bc)


echo $DIFF1
echo $DIFF2


