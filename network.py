import socket
import pickle
import main


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
        #self.id = self.connect()
        #print(self.id)

    def connect(self):
        """
        Connects to the game server        
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        """
        Sends data to the game server
        """
        try:
            data_stream = pickle.dumps(data)
            self.client.send(data_stream)
            return self.client.recv(2048)
        except socket.error as e:
            print(e)
