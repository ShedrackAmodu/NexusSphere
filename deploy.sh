#!/bin/bash
mkvirtualenv --python=/usr/bin/python3.10 nexussphere
workon nexussphere
git clone https://github.com/ShedrackAmodu/NexusSphere.git
cd NexusSphere
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
