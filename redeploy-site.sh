#!/bin/bash

cd project-team-jungle/
git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip3 install -r requirements.txt	

# restart myportfolio service
systemctl daemon-reload
systemctl restart myportfolio


