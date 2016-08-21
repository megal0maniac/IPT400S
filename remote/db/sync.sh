#!/bin/sh
REMOTEUSER="btech"
REMOTEHOST="cloud.michaelrodger.co.za"
BASEPATHLOCAL="/root/IPT400S"
BASEPATHREMOTE="/home/btech/IPT400S"

sleep 1
rsync -avc -e "ssh -v" $BASEPATHLOCAL/remote/db/*.db $REMOTEUSER@$REMOTEHOST:$BASEPATHREMOTE/local/db
