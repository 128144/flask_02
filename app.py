#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import os, json
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

'''
jsons_name = os.listdir("/home/shiyanlou/files")
with open(os.path.join("/home/shiyanlou/files",jsons_name[0]), 'r') as f:
    world = json.loads(f.read())
with open(os.path.join("/home/shiyanlou/files",jsons_name[1]), 'r') as f:
    shiyanlou = json.loads(f.read())
'''

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    cteated_time = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('files', lazy='dynamic'))

    def __init__(self, title, created_time, category, content):
        self.title = title
        if created_time is None:
            created_time = datetime.utcnow()
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

f = db.session.query(File).all()

c = db.session.query(Category).all()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@app.route('/')
def index():
    return render_template('index.html',file = f )

@app.route('/files/<file_id>')
def file(file_id):  
     return render_template('file.html',file_id = file_id, file = f, category = c, )
   
