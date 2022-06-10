set fileformat=unix
#!/bin/bash

sudo apt-get update
sudo apt-get install python3
python3 -m venv venv_for_run
source venv_for_run/bin/activate
sudo apt-get install build-essential python3-dev libpq-dev
sudo apt-get install python3-pip
sudo apt-get install build-dep python-psycopg2
pip3 install psycopg2
python3 -m pip install flask
pip install -r ./flask_files/requirements.txt
python ./flask_files/app.py