import socket
import sys

def check_connect():
	args = sys.argv[1:]
	try:
		index1 = args.index('--host')
		index2 = args.index('--port')
		host = args[index1 + 1]
		port = args[index2 + 1].split('-')
		port = [ int(i) for i in port]
	except:
		print('Parameter Error')
		sys.exit(-1)

	if len(host.split('.')) != 4:
		print('Parameter Error')
		sys.exit(-1)

	if len(port) == 1:
		start = port[0]
		end = port[0]
	else:
		start = port[0]
		end = port[1]

	while start <= end:
		s = socket.socket()
		s.settimeout(0.1)
		try:
			s.connect((host, start))
			print(str(start) + ' open')
		except:
			print(str(start) + ' closed')
		start+=1


if __name__ == '__main__':
	check_connect()