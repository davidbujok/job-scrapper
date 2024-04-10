#!/bin/bash

# START DOCKER AND DATABASE
tmux rename-window react-app-run
sudo systemctl start docker.socket
sudo systemctl start postgresql.service
# # PUT UP DOCKER CONTAINER
tmux send-keys 'docker compose up -d' C-m
# # START SSH SESSION INSIDE CONTAINER
tmux send-keys 'docker exec -it vite_docker sh' C-m
# # RUN SERVER ON THE CONTAINER
tmux send-keys 'npm run host' C-m

tmux new-window 
tmux rename-window flask-run
tmux send-keys 'cd ~/repos/job-scrapper/' C-m
tmux send-keys  'source venv/bin/activate' C-m
tmux send-keys  'flask --app app run' C-m

tmux new-window 
tmux rename-window js-code
tmux send-keys  'source venv/bin/activate' C-m
tmux send-keys  'swaymsg exec google-chrome-stable http://172.18.0.2:5173/' C-m
tmux send-keys 'cd ~/repos/job-scrapper/job-search' C-m
tmux send-keys 'clear' C-m

tmux new-window 
tmux rename-window scrapers
tmux send-keys 'cd ~/repos/job-scrapper/scrapers' C-m
tmux send-keys 'source ../venv/bin/activate' C-m
tmux send-keys 'clear' C-m
