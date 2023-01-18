#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def exeption(e):
    """ Teardown session """
    storage.close()


@app.route('/cities_by_states')
def statesList():
    """ Handle route """
    state = storage.all("State")
    return render_template('8-cities_by_states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
