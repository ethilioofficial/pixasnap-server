#!/usr/bin/env bash

apt-get update
apt-get install -y python3.10 python3.10-venv python3.10-dev

python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
