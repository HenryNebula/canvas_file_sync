#!/bin/bash
CONFIG="config.json"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
echo "entering folder $DIR"

base_dir=$( python3 json_parser.py --config $CONFIG --key base_path )
src_dir=$DIR/${base_dir}
dest_dir=$( python3 json_parser.py --config $CONFIG --key dest_path )
echo "from $src_dir to $dest_dir"

py=$( python3 json_parser.py --config $CONFIG --key python )
rc=$( python3 json_parser.py --config $CONFIG --key rclone )
echo "runtime environment [python: $py, rclone: $rc]"
$py canvas_sync.py --config $CONFIG --course -2
$rc sync $src_dir $dest_dir --delete-before -v
echo "ALL FINISH"
