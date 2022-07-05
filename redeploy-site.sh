#!/bin/bash

cd project-flask-ferrets
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build





#tmux kill-session -t portfolio_site
#source python3-virtualenv/bin/activate
#pip install -r requirements.txt
#systemctl daemon-reload
#systemctl restart myportfolio
#tmux new -d -s portfolio_site
#tmux send-keys -t "portfolio_site" "source python3-virtualenv/bin/activate" Enter
#tmux send-keys -t "portfolio_site" "flask run --host=0.0.0.0" Enter