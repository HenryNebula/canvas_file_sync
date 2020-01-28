#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_dir=$( cat config.json | jq -r .base_path )
src_dir=$DIR
src_dir+="/${base_dir}"

cd $DIR
py=$( cat config.json | jq -r .python )
dest_dir=$( cat config.json | jq -r .dest_path )

eval $py canvas_sync.py
/usr/bin/rclone sync $src_dir $dest_dir --delete-before -v
echo "ALL FINISH"
