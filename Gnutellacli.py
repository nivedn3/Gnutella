
'''
Implementation of basic Gnutella protocol for accesssing the file from a single node'''

from socket import *
from thread import *
import os
class servent():
	contacts=[]
	def __init__(self):
		self.sock=socket()	
	def send(self,d,file_n,host_addr,path_n):
		if host_addr=='':
			print path_n
			os.chdir(path_n)
			f=open(file_n,'w+')
			#for i in self.contacts:
				#self.sock.connect(i)
			self.sock.send(d)
			l=self.sock.recv(1024)
			while l:
				print "receiving" + l
				f.write(l)
				l=self.sock.recv(1024)
			f.close()
		else:
			self.sock.connect(host_addr)
			self.sock.send(d)
			pong=self.sock.recv(1024)
			print pong 
	def beginServer(self,port):
		self.share()	
		def clientthread(c):
				while True:
					#c.send("connection established thread")
					while c.recv:
						k=c.recv(255555)
						print k
						if k:
							sp=k.split(',')
							des=sp[0][1:]
							data_len=len(sp[1])
							data=sp[1][2:data_len-2]
							if des == '1':
									c.sendall("PONG:")
									#c.shutdown(SHUT_WR)
									#c.shutdown(socket.SHUT_WR)
									#c.close()
							elif des=='2':
								os.chdir(self.path)
								list=os.listdir(self.path)
								if data in list:
									print "QueryHit:success"
									f=open(data,'rb+')
									l=f.read(1024)
									while l:
										c.sendall(l)
										print "sending"
										l=f.read(1024)
									c.shutdown(SHUT_WR)
									f.close()
								else:
									print data 
									c.sendall("QueryHit:Failed") 
									c.shutdown(SHUT_WR)
		host=raw_input("Enter the address (127.0.0.1 for local host':");
		#setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
		self.sock.bind((host,port))
		self.sock.listen(10)
		while True:
			c,addr=self.sock.accept()
			print "connection request from" , addr
			start_new_thread(clientthread,(c,))
	'''Query sends the requested file name to the other clients, 
	User enters the file_name and file path where it needs to be downloaded to'''
	def Query(self):
		file_n=raw_input("Enter file name :");
		path_n=raw_input("Enter the path to store the file");
		print path_n
		d=[2]
		d.append(file_n)
		d=str(d)
		self.send(d,file_n,'',path_n)
	def ping(self):
		host=input("Enter the (host_name,port) to ping in the mentioned format:")
		d=[1,'']
		d=str(d)
		self.send(d,'',host,'')
	'''In future Implementation where the number of nodes in the network is more, the contacts are stored.'''
	def peers(self):
		peer=input("Enter the (host_name,port) in this format:");
		self.contacts.append(peer)
	'''Selectig the directory which is to be shared with the other clients'''
	def share(self):
		path=raw_input("Enter the path of directory to share :");
		self.path=path

if __name__ == "__main__":
    n=servent()
    n.peers()
    n.ping()
    n.Query()