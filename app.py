from flask import Flask, render_template, request, url_for
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

import os
import json
import sys

load_dotenv()
app = Flask( __name__ )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
heroku = Heroku(app)
db = SQLAlchemy(app)

class Dataentry(db.Model):
    __tablename__ = "dataentry"
    id = db.Column(db.Integer, primary_key=True)
    mydata = db.Column(db.Text())

    def __init__ (self, mydata):
        self.mydata = mydata

@app.route("/submit", methods=["POST"])
def post_to_db():
    indata = Dataentry(request.form['mydata'])
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry.\n")
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))

@app.route("/")
def enter_data(): 
    return render_template("dataentry.html")

if __name__ == ' __main__':
    app.run()
