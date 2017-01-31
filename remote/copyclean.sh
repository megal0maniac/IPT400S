#!/bin/sh
# This script copies databases from the temporary storage (RAM) into long-term storage (SD card)
# Databases in RAM older than 7 days are deleted
# It is called by cron. Please see remote/sys/crontab
# Michael Rodger 213085208
TMPDB="/tmp/db"
LTSDB="/data/db"

sleep 5
cp $TMPDB/currentdb $LTSDB
rsync -av $TMPDB/*.db $LTSDB
find $TMPDB/ -type f -mtime +7 -exec rm -f {} +
