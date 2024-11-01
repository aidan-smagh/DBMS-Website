from flask import Flask
dbtour_app = Flask(__name__)
from dbtour_dev import routes
