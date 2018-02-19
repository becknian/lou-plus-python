# -*- coding:utf-8 -*-
from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
	path = '../files'
	files = os.listdir(path)
	titles = []
	for file in files:
		f = open(path + '/' + file)
		iter_f = iter(f)
		print(iter_f)
		for line in f:
			cur_line = line.strip().split(':')
			if cur_line[0] == '"title"':
				titles.append(cur_line[1][2:-2])
	return render_template('index.html', titles=titles)



@app.route('/files/<filename>')
def file(filename):
	parts = filename.split('.')
	filename = parts[0] + '.json'
	path = '../files/' + filename
	if not os.path.exists(path):
		return render_template('404.html'), 404
	article = {}
	with open(path) as file:
		for line in file:
			if ':' in line:
				cur_line = line.strip().split(':')
				article[cur_line[0][1:-1]] = cur_line[1][2:-2]
	return render_template('file.html', article=article)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


