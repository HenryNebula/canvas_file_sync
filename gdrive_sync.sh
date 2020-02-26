#!/bin/bash
CONFIG="config.json"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

base_dir=$( cat "$CONFIG" | jq -r .base_path )
src_dir=$DIR/${base_dir}
py=$( cat "$CONFIG" | jq -r .python )
dest_dir=$( cat "$CONFIG" | jq -r .dest_path )

$py canvas_sync.py --config $CONFIG --course -2
echo "from $src_dir to $dest_dir"
/usr/bin/rclone sync $src_dir $dest_dir --delete-before -v
echo "ALL FINISH"
