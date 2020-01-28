#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

base_dir=$( cat config.json | jq -r .base_path )
src_dir=$DIR/${base_dir}
py=$( cat config.json | jq -r .python )
dest_dir=$( cat config.json | jq -r .dest_path )

$py canvas_sync.py
echo "from $src_dir to $dest_dir"
/usr/bin/rclone sync $src_dir $dest_dir --delete-before -v
echo "ALL FINISH"
