# file: __init__.py
# pwd : /project/app/__init__.py

from flask import Flask

app = Flask(__name__)

from app.main.index import main as main
from app.main.test import bp 

app.register_blueprint(main)
app.register_blueprint(bp)
