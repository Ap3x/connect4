#!/usr/bin/env python3
import main
import socket
import pickle
from threading
import sys
import os
import network

# hostname = socket.gethostname()  
# server = socket.gethostbyname(hostname) 
server = "0.0.0.0"
port = 5969

def start_server_thread():
	ret = threading.Thread(target=start_server)
	ret.start()
	#ret = network.Network("127.0.0.1",port)
	return ret

def start_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.bind((server, port))
	except socket.error as e:
		str(e)

	s.listen(3) # Limited to 3 connections
	print("Waiting for a connection, Server Started")
	while True:
		conn, addr = s.accept()
		#print("Connected to:", addr)
		threading.Thread(target=threaded_client,args=(conn)).start()

def threaded_client(conn):
	conn.send(str.encode("Connected"))
	# os.system("cls" if os.name == "nt" else "clear")
	# main.board.print_board()
	while True:
		try:
			data = conn.recv(2048)
			data_variable = pickle.loads(data)

			if not data:
				print("Disconnected")
				break
			else:
				print("Recieved Something")
				print(data_variable)
			
			conn.sendall(data_variable)
		except:
			break

	print("Lost connection")
	conn.close()


