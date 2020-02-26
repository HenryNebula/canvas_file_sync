# canvas_file_sync

A simple tool for downloading course files from Canvas and syncing them to your own web drive. For now the syncing script only supports Unix-like systems and Python version higher than 3.6, and the tool has only been tested on Ubuntu 16.04 for now. The python file [canvas_sync.py]("canvas_sync.py") can be run alone, but without the feature for syncing the download contents to a web drive.

# How to use
1. Get a access token from your canvas site, following the tutorial [here](https://community.canvaslms.com/docs/DOC-10806-4214724194). 
2. (Optional) Install [rlone](https://rclone.org/downloads/) at /usr/bin/rclone
3. Install required packages from the [requirements.txt](./requirements.txt) using `pip install -r requirements.txt`
4. Copy [config.template](./config.template) to a new file named [config.json], and fill in all necessary configurations based on your runtime system. Those optional fields can be omitted if you are just using the python script for downloading.
5. Run `./gdrive_sync.sh` to start the syncing or just run `python canvas_sync.py -h` to see input arguments for running the python script by itself.
