import socket
import pickle
import threading
import queue

class Network:
	"""Contains functions to connect and send data"""

	def __init__(self, server_ip: str, port: int):
		"""
		Initializes an object for a connection to a computer


		client -- The client socket file descriptor
		server -- The server internet protocol address
		port -- The port we are connecting too
		addr -- Comprised of server and port
		id -- The client id
		"""
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = server_ip
		self.port = port
		self.addr = (self.server, self.port)
		self.xqu = queue.Queue()
		self.active = False

	def listener(self):
		while self.active:
			rec = pickle.loads(self.client.recv(2048))
			self.xqu.put(rec)
	
	def stop(self):
		self.active = False

	def connect(self):
		"""
		Connects to the game server        
		"""
		try:
			self.client.connect(self.addr)
			if self.client.recv(2048).decode() == "Connected":
				self.active = True
				threading.Thread(target=Network.listener,args=(self)).start()
			else:
				self.client.shutdown()
		except:
			pass

	def receive(self):
		if self.xqu.empty:
			return None
		return self.xqu.get_nowait()

	def send(self, data):
		"""
		Sends data to the game server
		"""
		try:
			data_stream = pickle.dumps(data)
			self.client.sendall(data_stream)
			return self.client.recv(2048)
		except socket.error as e:
			print(e)
