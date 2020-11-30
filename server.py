#!/usr/bin/env python3
import socket
import pickle
import threading
import sys
import os
import network

server = None
clients = []

def start_server_thread():
	ret = threading.Thread(target=start_server)
	ret.start()
	#ret = network.Network("127.0.0.1",port)
	return ret

def start_server(server_ip,port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((server_ip, port))
	except socket.error as e:
		str(e)

	server.listen(2) # Limited to 2 connections
	print("Waiting for a connection, Server Started")
	while True:
		conn, addr = server.accept()
		threading.Thread(target=threaded_client,args=(conn)).start()

def stop_server():
		server.close()

def threaded_client(conn):
	conn.send(str.encode("Connected"))
	
	clients.append(conn)

	while True:
		try:
			data = conn.recv(2048)
			data_variable = pickle.loads(data)

			if not data:
				break
			for c in clients:
				if not conn is c:
					try:
						c.sendall(data_variable)
					except:
						break
		except:
			break

	conn.close()
	clients.remove(conn)


