import socket, logging, time
from queue import Empty
from multiprocessing import Process, log_to_stderr
from socket import error as Error

HOST = ''
PORT = 32222
MAXCONN = 10
TIMEOUT = 2
BUFFRECV = 1
BUFFSIZE = 1024
ENCODING = 'utf-8'
logg = log_to_stderr(logging.DEBUG)

class ServerTcp(object):
	"""docstring for ServerTcp"""
	def __init__(self):
		super(ServerTcp, self).__init__()
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((HOST,PORT))
		self.serverSocket.listen(MAXCONN)
		self.serverSocket.settimeout(TIMEOUT)

	def recvall(self, sock, count):
		buf = b''
		while count:
			newbuf = sock.recv(BUFFRECV)
			if not newbuf: return None
			buf+= newbuf
			count -= len(newbuf)
		return buf

	def worker(self,socket):
		while True:
			try:
				client, address = socket.accept()
				logg.debug("{u} connected".format(u=address))
				client.send("ECHO".encode(ENCODING))
				size = client.recv(BUFFSIZE).decode(ENCODING)
				if int(size) >0:
					client.send("OK.".encode(ENCODING))
					data = self.recvall(client,int(size))
					if int(size) == len(data):
						logging.debug(data.decode(ENCODING))
				client.close()
				logg.debug("{u} desconnected".format(u=address))
			except Error:
				time.sleep(0.1)

if __name__ == '__main__':
	server = ServerTcp()

	num_workers = 8
	workers = [Process(target=server.worker, args=(server.serverSocket,)) for i in 
			range(num_workers)]
	for p in workers:
		p.daemon = True
		p.start()

	while True:
		cm = input('z=> ')
		if cm == 'q':
			for p in workers:
				p.terminate()
			for p in workers:
				p.join()
			server.serverSocket.close()
			break

