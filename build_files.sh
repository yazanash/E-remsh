#!/bin/bash
python3.9 -m venv venv
source /vercel/path0/venv/bin/activate
chmod 664 db.sqlite3
chmod 775 /vercel/path0/rmsh
if ! command -v pip &> /dev/null; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
fi

pip install -r requirements.txt

python3.9 manage.py collectstatic --noinput