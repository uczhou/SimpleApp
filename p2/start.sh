#! /bin/bash

pip install flask
pip install flask-login
pip install flask-sqlalchemy


if [ $# -gt 0 ]; then
    python views.py $1
else
    python views.py
fi