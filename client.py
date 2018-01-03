import socket, time

HOST = ''
PORT = 32222
MAXCONN = 10
TIMEOUT = 1
BUFFRECV = 1
BUFFSIZE = 1024
ENCODING = 'utf-8'

class ClientTcp(object):
	"""docstring for ClientTcp"""
	def __init__(self):
		super(ClientTcp, self).__init__()

	def __connect(self):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.connect((HOST,PORT))

	def recvall(self, sock, count):
		buf = b''
		while count:
			newbuf = sock.recv(BUFFRECV)
			if not newbuf: return None
			buf+= newbuf
			count -= len(newbuf)
		return buf

	def send(self):
		msg = input('z=> ')
		msg = msg.encode(ENCODING)
		self.__send(msg)

	def __send(self, data):
		for i in range(1):
			self.__connect()
			echo = self.recvall(self.serverSocket, 4)
			if echo:
				print(echo.decode(ENCODING))
				self.serverSocket.send(str(len(data)).encode(ENCODING))
				response = self.recvall(self.serverSocket, 3)
				if response:
					print(response.decode(ENCODING))
					self.serverSocket.send(data)
			self.serverSocket.close()

	def test(self):
		count = 1
		for i in range(100):
			self.__send(('TEST '+str(count)).encode(ENCODING))
			count +=1
			time.sleep(.01)

if __name__ == '__main__':
	client = ClientTcp()
	client.test()
