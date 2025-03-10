#!/bin/sh

# parameters
MIRRORDIR=/home/iscb/wolfson/doririmon/home/order/ubinet/pesto/C_structured/PeSToIntegration/assets/data/pesto/data/all_biounits
#MIRRORDIR=all_biounits_cif
LOGFILE=/home/iscb/wolfson/doririmon/home/order/ubinet/pesto/C_structured/PeSToIntegration/assets/data/pesto/data/pdb_download_logs.txt
SERVER=rsync.ebi.ac.uk::pub/databases/rcsb/pdb-remediated
PORT=873
FTPPATH=/data/biounit/PDB/divided/
#FTPPATH=/data/biounit/mmCIF/divided/

# download
rsync -rlpt -v -z --delete --port=$PORT ${SERVER}${FTPPATH} $MIRRORDIR > $LOGFILE 2>/dev/null
