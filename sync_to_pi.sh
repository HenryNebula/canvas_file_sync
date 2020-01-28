#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
rsync $DIR pi@192.168.0.59:/home/pi/Documents -v -r