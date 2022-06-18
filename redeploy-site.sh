#!/bin/bash

tmux kill-session -t portfolio_site
cd project-flask-ferrets
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -d -s portfolio_site
tmux send-keys -t "portfolio_site" "source python3-virtualenv/bin/activate" Enter
tmux send-keys -t "portfolio_site" "flask run --host=0.0.0.0" Enter