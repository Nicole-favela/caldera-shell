#!/bin/bash

#configuration
Caldera_dir="$HOME/caldera"
log_file="$Caldera_dir/caldera.log"
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip3 install -r $Caldera_dir/requirements.txt
echo "starting caldera"

docker run -p 8888:8888 caldera > "$log_file" 2>&1 &

