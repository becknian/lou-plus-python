import sys
from pymongo import MongoClient
from flask import Flask

getrank = Flask(__name__)

def get_rank(user_id):
	client = MongoClient('127.0.0.1', 27017)
	db = client.shiyanlou
	contests = db.contests
	users = db.ranks.find().sort([('score', -1), ('time', 1)])
	rank = 1
	for user in users:
		if user['user_id'] == user_id:
			score = user['score']
			submit_time = user['time']
			break
		rank += 1

	return rank, score, submit_time

def create_scores():
	client = MongoClient('127.0.0.1', 27017)
	db = client.shiyanlou
	ids = db.contests.distinct('user_id')
	for id in ids:
		score = 0
		time = 0
		for line in  db.contests.find({'user_id': id}):
			score += line['score']
			time += line['submit_time']
		user = {'user_id': id, 'score': score, 'time': time}
		db.ranks.insert_one(user)


if __name__ == '__main__':
	try:
		user_id = int(sys.argv[1])
	except:
		print("Parameter Error")
		sys.exit(-1)

	userdata = get_rank(user_id)
	print(userdata)