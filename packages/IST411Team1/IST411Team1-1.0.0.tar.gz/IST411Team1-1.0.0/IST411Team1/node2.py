"""Project: Project Diamond, node2
Purpose Details: to use SSL socket to receive json payload from node1, and will log the payload once payload is received. After this process, the genCheckSum method
generates a checksum for the payload using SHA256. After this, via SFTP, the json payload and checksum are sent to a remote directory, and logged with Node5. The json payload is also 
sent via email, using SMTP, and logged with Node5. The P2P payload time from this node to node3 is calculated as well in this node. 
Course: IST 411
Author: Jimmy Hopf
Date Developed: 11/20/17
Last date changed: 11/26/17
Rev: 1.3.7"""
import socket, ssl, json, sys, smtplib, hashlib, time, pysftp, subprocess, p2p
from node5 import Node5
from email.mime.text import MIMEText
"""calls clock() to track time"""
beginTime = time.clock()
class Node2:

	def __init__(self,name):
		self.name = name
		self.payload = None
		self.checksum = None

	def receivePayload(self): 
		"""receive json payload from node1
		   :return: the json payload
		   :rtype: bytes object """
		payload = None
		try:
			print(self.name," creating an INET, STREAMing socket using SSL")
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
			ssl_sock = ssl.wrap_socket(s, server_side=True,certfile="server.crt", keyfile="server.key")
			print(self.name," binding the socket to a public host, and a well-known port 8080")
			ssl_sock.bind(('localhost', 8080))
			ssl_sock.listen(5)
			while True:
				if payload != None:
					break
				print("accept connections from outside")
				(clientsocket, address) = ssl_sock.accept()
				payload = clientsocket.recv(2048)
		except Exception as e:
			print(e)
			ssl_sock.close()
		log = {"Node":self.name,"Payload received via SSL Socket":str(payload)}
		print(type(payload))
		return payload

	def genChecksum(self,payload):
		"""generates a checksum with hashlib
		   :return: checksum
		   :rtype: str """
		print(self.name," generating a checksum of the payload to send")
		checksum = hashlib.sha256(payload).hexdigest()
		log = {"Node":self.name,"Checksum generated":str(checksum)}
		Node5.log(log)
		return checksum

	def sendSFTP(self,payload,checksum,runSub):
		"""sending payload through SFTP
		:return: sent
		:rtype: boolean"""

		sent = False
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None
		with open('Team1SFTPpayload.json','w') as outFile:
			outFile.write(json.dumps(payload.decode()))
			outFile.close()
		with open('Team1SFTPchecksum.txt','w') as outFile:
			outFile.write(checksum)
			outFile.close()

		cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux-fa17-411', 'username':'ftpuser', 'password':'test1234', 'port':101}
		try:
			with pysftp.Connection(**cinfo) as sftp:
				print("Connection made")
				try:
					print(self.name," is sending JSON file to remote directory via SFTP")
					sftp.put('Team1SFTPpayload.json','/home/ftpuser/Team1SFTPpayload.json')
					print(self.name," is sending JSON's checksum to remote directory via SFTP")
					sftp.put('Team1SFTPchecksum.txt','/home/ftpuser/Team1SFTPchecksum.txt')
					sent = True
					log = {"Node":self.name,"JSON file Sent via SFTP":"Team1SFTPpayload.json","Checksum file sent via SFTP":"Team1SFTPchecksum.txt"}
					Node5.log(log)
					if runSub == True:
						subprocess.Popen(['python3','node3.py'])
				except:
					print("Log exception 1: ", sys.exc_info()[0])
				return sent
		except Exception as e:
			print(e)

	def sendSMTP(self,payload):
		"""sending payload as email
		:return: sent
		:rtype:boolean"""
		sent = False
		fromAddress = 'sjc54599@gmail.com'
		toAddress = 'sjc5459@psu.edu'
		subject = 'Node 2 Payload Email'
		msg = MIMEText(str(payload))
		msg['Subject'] = subject
		msg['From'] = fromAddress
		msg['to'] = toAddress
		try:
			s = smtplib.SMTP('smtp.psu.edu')
			s.sendmail(fromAddress,[toAddress],msg.as_string())
			sent = True
			log = {"Node":self.name,"Email with payload sent to":toAddress,"Send from":fromAddress}
			Node5.log(log)
		except Exception as e:
			print(e)

		finally:
			s.quit()
			return sent


def main():
	print("Starting Node 2...")
	node2 = Node2("Node 2")
	node2.payload = node2.receivePayload()
	node2.checksum = node2.genChecksum(node2.payload)
	print("Payload: ", node2.payload)
	print("Checksum: ",node2.checksum)
	p2pTime = p2p.end(beginTime)
	print(node2.name," to Node 3 payload time: ",p2pTime," seconds")
	Node5.log({"Node":node2.name,"P2P payload time in seconds":p2pTime})
	node2.sendSFTP(node2.payload,node2.checksum,True)
	node2.sendSMTP(node2.payload)

if __name__ == '__main__':
	main()
