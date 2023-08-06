"""Project: Project Diamond, node3
Purpose Details: This node receives a JSON payload from a remote directory via SFTP, receives the payload's checksum via SFTP, verifies the checksum matches a self generated
checksum on the received payload using SHA-256 hashing, compresses the received payload using crc32 compression, and activates a Pyro4 request broker so node4 can access the
method to receive the JSON via a generated URI.  All activities are logged to a MongoDB in this node, and P2P payload time is calculated as well.
Authors: Arnold Adu-Darko & Shawn Conway
Date Developed: 11/21/2017
Last Date Changed: 11/26/2017
Rev: 1.3.1"""

import Pyro4, subprocess, zlib, time, pysftp, json, hashlib, p2p
from node5 import Node5

bool = False
beginTime = time.clock()
@Pyro4.expose
class node3:
	def __init__(self,name,daemon):
		self.name = name
		self.json = None
		self.daemon = daemon
		self.crcChecksum = None
		self.recSFTPChecksum = None

	"""Getting the json"""
	def get_json(self):
		compJson = self.compressPayload(self.json)
		print("Compressed message: ",compJson)
		bool = True
		return compJson

	"""Method to handle daemon shutdown"""
	def shutDown(self):
		shutDown = False
		try:
			self.daemon.shutdown()
			shutDown = True
		except Exception as e:
			print(e)
		return shutDown
	"""Compressing Payload"""
	def compressPayload(self,data):
		try:
			print(self.name, " is compressing payload...")
			payloadComp = zlib.compress(data)
			log = {"Node":self.name,"Compressed payload":str(payloadComp)}
			Node5.log(log)
			return payloadComp
		except Exception as e:
			print(e)

	"""Generating Checsum for Compressed Payload"""
	def genCrcChecksum(self,data):
		try:
			print(self.name," is generating checksum...")
			checksum = zlib.crc32(data)
			print(self.name," checksum: ",checksum)
			log = {"Node":self.name,"CRC Checksum":str(checksum)}
			Node5.log(log)
			return checksum
		except Exception as e:
			print(e)

	"""Getting the Checksum"""
	def getChecksum(self):
		return self.crcChecksum

	"""Receiving the payload vis SFTP"""
	def receiveSFTPPayload(self):
		try:
			print(self.name," is retrieving payload from remote directory via SFTP...")
			payload = None
			cnopts = pysftp.CnOpts()
			cnopts.hostkeys = None
			cinfo = {'cnopts':cnopts,'host':'oz-ist-linux-fa17-411','username':'ftpuser','password':'test1234','port':101}
			with pysftp.Connection(**cinfo) as sftp:
				sftp.get('/home/ftpuser/Team1SFTPpayload.json','Team1SFTPReceived.json')
			with open('Team1SFTPReceived.json','r') as inFile:
				payload = json.load(inFile)
			payload = payload.encode('utf-8')
			log = {"Name":self.name,"Payload received via SFTP":str(payload)}
			Node5.log(log)
			return payload
		except Exception as e:
			print(e)

	"""Receiving the Payload's Checksum via SFTP"""
	def receiveSFTPChecksum(self):
		try:
			print(self.name," is retrieving payload's checksum from remote directory via SFTP...")
			checksum = None
			cnopts = pysftp.CnOpts()
			cnopts.hostkeys = None
			cinfo = {'cnopts':cnopts,'host':'oz-ist-linux-fa17-411','username':'ftpuser','password':'test1234','port':101}
			with pysftp.Connection(**cinfo) as sftp:
				sftp.get('/home/ftpuser/Team1SFTPchecksum.txt','Team1ChecksumReceived.txt')
			with open('Team1ChecksumReceived.txt','r') as inFile:
				checksum = inFile.read()
			log = {"Node":self.name,"Checksum received via SFTP":str(checksum)}
			Node5.log(log)
			return checksum
		except Exception as e:
			print(e)

	"Authenticating Payload by Checking to see if Checksums match"""
	def verifySFTPChecksum(self,checksum,payload):
		verifyPerformed = False
		try:
			checksumOfPayload = hashlib.sha256(payload).hexdigest()
			print(checksumOfPayload)
			print(checksum)
			if checksumOfPayload == checksum:
				print("Checksum of payload received from Node 2 via SFTP verifed.")
				log = {"Node":self.name,"Checksum received via SFTP is verified":"True","Checksum Received":str(checksum),"Checksum Generated for matching":str(checksumOfPayload)}
				Node5.log(log)

			else:
				print("Payload received from Node 2 via SFTP has been compromised.")
			verifyPerformed = True
		except Exception as e:
			print(e)
		return verifyPerformed


if __name__ == '__main__':

	print("Starting Node 3...")
	daemon = Pyro4.Daemon()
	node3 = node3("Node 3",daemon)
	node3.json = node3.receiveSFTPPayload()
	node3.recSFTPChecksum = node3.receiveSFTPChecksum()
	node3.verifySFTPChecksum(node3.recSFTPChecksum,node3.json)
	node3.crcChecksum = node3.genCrcChecksum(node3.json)
	uri = node3.daemon.register(node3)
	print(node3.name + "'s uri: ",uri)
	print(node3.name," is ready for remote access via Pyro4.")
	p2pTime = p2p.end(beginTime)
	log = {"Node":node3.name,"P2P payload time in seconds":p2pTime}
	Node5.log(log)
	print(node3.name," to Node 4 payload time: ",p2pTime," seconds")
	subprocess.Popen(['python3','node4.py',str(uri)])
	node3.daemon.requestLoop()
