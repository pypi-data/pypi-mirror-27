from flask import Flask, jsonify, redirect, render_template, url_for

from .db import DB


app = Flask(__name__)
db = DB()


@app.route('/')
def index():
    items = db.get_unread()
    return render_template('index.html', items=items)


@app.route('/read/<id>/')
def read(id):
    db.mark_read(id)
    return redirect(url_for('index'))
