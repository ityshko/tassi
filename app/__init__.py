import os

from flask import Flask
app = Flask(__name__)
app.config.from_json("config.json", silent=False)

# def create_app():
#   # create and configure app
#   app = Flask(__name__, instance_relative_config=True)
#   app.config.from_json("config.py", silent=False)
#

from app import views
