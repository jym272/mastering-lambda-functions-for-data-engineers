#!/usr/bin/zsh
# go to layer dir or exit with error message
cd layer || { echo "layer dir not found"; exit 1; }
# create a venv
rm -rf venv
python3.9 -m venv venv
# activate venv
source venv/bin/activate
# pip install requests, numpy into the python folder
pip install requests
pip install pandas
pip install numpy --upgrade
# deactivate venv
deactivate
