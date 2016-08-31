#!/bin/sh
TMPDB="/tmp/db"
LTSDB="/data/db"

sleep 5
cp $TMPDB/currentdb $LTSDB
rsync -av $TMPDB/*.db $LTSDB
find $TMPDB/ -type f -mtime +7 -exec rm -f {} +
