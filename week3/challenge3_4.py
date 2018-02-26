import sys
import re
from datetime import datetime


def open_parser(filename):
	try:
		with open(filename) as logfile:
			pattern = (r''
					   '(\d+.\d+.\d+.\d+)\s-\s-\s'
					   '\[(.+)\]\s'
					   '"GET\s(.+)\s\w+/.+"\s'
					   '(\d+)\s'
					   '(\d+)\s'
					   '"(.+)"\s'
					   '"(.+)"')
			parsers = re.findall(pattern, logfile.read())
			return parsers
	except:
		print("Parameter Error")
		sys.exit(-1)

def main():
	logs = open_parser('/home/shiyanlou/Code/nginx.log')
	visit_dict = {}
	req_dict = {}
	for log in logs:
		if log[3] == '404':
			if req_dict.get(log[2]) is None:
				req_dict[log[2]] = 0
			req_dict[log[2]] += 1
		if '11/Jan/2017' not in log[1]:
			continue
		if visit_dict.get(log[0]) is None:
			visit_dict[log[0]] = 0
		visit_dict[log[0]] += 1		

	ip = max(visit_dict, key = visit_dict.get)
	ip_dict = {ip : visit_dict[ip]}
	url = max(req_dict, key = req_dict.get)
	url_dict = {url:  req_dict[url]}


	return ip_dict, url_dict

if __name__ == '__main__':
	ip_dict, url_dict = main()
	print(ip_dict, url_dict)
