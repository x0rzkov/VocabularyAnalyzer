"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__, static_url_path='/static')
app.secret_key = "493wtgZewc9un"
import Vocabanal.views