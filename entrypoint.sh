#!/bin/bash

#cloudflared tunnel run --token $TOKEN &
gunicorn --conf gunicorn_conf.py --bind 0.0.0.0:5000 web:app &
python bot.py