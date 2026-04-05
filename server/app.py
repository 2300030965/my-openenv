# server/app.py

from fastapi import FastAPI
from app.main import app as main_app

app = main_app