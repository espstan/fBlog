#!/bin/bash

cd blog/
virtualenv -p python3 ./venv	
source ./venv/bin/activate
#установка компонентов
pip install -r requirements.txt
python app.py
