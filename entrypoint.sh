#!/bin/bash

[[ -n $CLOUDFLARED_TOKEN ]] && cloudflared tunnel run --token $CLOUDFLARED_TOKEN &
gunicorn --bind 0.0.0.0:5000 web:app &
python bot.py