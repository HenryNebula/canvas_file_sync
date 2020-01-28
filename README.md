# canvas_file_sync

A simple tool for downloading course files from Canvas and syncing them to your own web drive. For now it only supports Unix-like systems and Python version higher than 3.6, and the tool has only been tested on Ubuntu 16.04 for now.

# How to use

1. Install [rlone](https://rclone.org/downloads/) at /usr/bin/rclone
2. Install required packages from the [requirements.txt](./requirements.txt) using `pip install -r requirements.txt`
3. Copy [config.template](./config.template) to a new file named [config.json], and fill in all necessary configurations based on your runtime system.
4. Run `./gdrive_sync.sh` to start the syncing.
