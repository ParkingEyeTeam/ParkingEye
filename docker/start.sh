#!/bin/bash

source /venv/bin/activate
exec uvicorn --host 0.0.0.0 server.main:app &
exec python telegram_bot/main.py