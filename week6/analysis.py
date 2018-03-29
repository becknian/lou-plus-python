import json
import pandas as pd 

def analysis(file, user_id):
	times = 0
	minutes = 0

	data = pd.read_json(file)


	user_data = data[data['user_id'] == user_id]
	times = len(user_data)
	minutes = 0

	for index in range(len(user_data)):
		minutes += user_data.iloc[index]['minutes']
	# print(times, minutes)

	return times, minutes
