#!/bin/bash


alembic revision --autogenerate -m 'init'
alembic upgrade head

python bot.py