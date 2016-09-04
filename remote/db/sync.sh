#!/bin/sh
REMOTEUSER="btech"
REMOTEHOST="cloud.michaelrodger.co.za"
DBPATHLOCAL="/tmp/db"
BASEPATHREMOTE="/home/btech/IPT400S"

sleep 1
rsync -avc -e "ssh -v" $DBPATHLOCAL/$(cat $DBPATHLOCAL/currentdb) $REMOTEUSER@$REMOTEHOST:$BASEPATHREMOTE/local/db
