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
    """ close session """
    storage.close()


@app.route('/states')
@app.route('/states/<id>')
def StatesAndcitiesByState(id=None):
    """ Handle route """
    state = storage.all("State")
    if id is None:
        return render_template('9-states.html', state=state)
    else:
        for x in state.values():
            if x.id == id:
                return render_template("9-states.html", state=x)
    return render_template("9-states.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
