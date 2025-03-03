#!/bin/bash
python3.9 -m venv venv
source venv/bin/activate

if ! command -v pip &> /dev/null; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
fi

pip install -r requirements.txt

python3.9 manage.py collectstatic --noinput