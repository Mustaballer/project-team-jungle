#!/bin/bash
echo "My nigga"
pkill -f tmux

cd project-team-jungle/
git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip3 install -r requirements.txt	

# create tmux session
tmux new -d -s my_session 'flask run --host=0.0.0.0'


