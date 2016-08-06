#!/bin/bash
rsync -av -e "ssh -Cv" *.db btech@localhost:/home/btech/IPT400S/local/db | tee rsync.log
