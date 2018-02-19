# -*- coding:utf-8 -*-
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class File(db.Model):
	__tablename__ = 'file'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))
	content = db.Column(db.Text)

	def __init__(self, id, title, created_time, category, content):
		self.id = id
		self.title = title
		self.created_time = created_time
		self.category = category
		self.content = content

	def __repr__(self):
		return '<File %r>' % self.title

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __init__(self, id, name):
		self.id = id
		self.name = name

	def __repr__(self):
		return '<Category %r>' % self.name


@app.route('/')
def index():
	engine = create_engine('mysql://root:@localhost/shiyanlou')
	files = engine.execute('select * from file').fetchall()

	return render_template('index.html', files=files)



@app.route('/files/<file_id>')
def file(file_id):
	engine = create_engine('mysql://root:@localhost/shiyanlou')
	Session = sessionmaker(bind=engine)
	session = Session()
	file = session.query(File).filter(File.id==file_id).one_or_none()
	if file == None:
		return render_template('404.html'), 404

	article = {}
	article['content'] = file.content
	article['created_time'] = file.created_time
	article['category'] = file.category.name

	return render_template('file.html', article=article) 
	

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

