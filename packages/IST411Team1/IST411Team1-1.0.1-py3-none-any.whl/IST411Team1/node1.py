"""Project: Project Diamond, node1
   Purpose Details: This node is responsible for getting a JSON payload using cURL,
                    then forwarding the JSON message to node2 using a Socket(SSL).
                    Additionally, node1 should write the JSON payload to a text file.
		    Also, node1 will receive an AES encrypted payload from the final 
		    node via RabbitMQ and decrypt it. Every activity is logged within
		    this node to a MongoDB using node5's Node5 log method. P2P payload 
		    time is calculated using Team 1's p2p module; the total P2P time
		    is also calculated in this node since it is the last node to receive
		    a payload. 
   Course: IST 411
   Author: Justin Grant
   Date Developed: 21 November 2017
   Last Date Changed: 26 November 2017
   Rev: 1.3.5
"""
import urllib.parse, urllib.request, pika, json, socket, ssl, subprocess, sys, time, p2p
from Crypto.Cipher import AES
from node5 import Node5 as mongo

p2p.clear()
startTime = p2p.start()

class Node1:
	"""Node1 is responsible for receiving a JSON payload, processing it, and forwarding to Node2"""
	def __init__(self,name):
		"""initialize a Node1 object
	   	   :param name: name of object
	   	   :rtype: None
		"""
		self.name = name
		self.p = None
		self.payload = None
		self.aesPayload = None	
		self.recDecrPayload = None



	def getCurlMessage(self):
		"""Get a cURL message
		   :return: the JSON payload
		   :rtype: bytes object
		"""
		# https://jsonplaceholder.typicode.com/posts/1
		url='https://jsonplaceholder.typicode.com'
		param='/posts/1'
		payload = None
		try:
			#parse is needed if there are special characters in the URL that need encoding
			#value=urllib.parse.urlencode(param)
			response=urllib.request.urlopen(url+param)
			payload=response.read()
		except: #Catch all exceptions
			e = sys.exc_info()[0]
			print("error: %s" % e)
		return payload
	
	def sslServerInitiate(self,payload,bValue):
		"""Initiate the SSL Server in Node2
		   :param payload: the JSON payload
		   :param bValue: boolean value for testing, will not call subprocess if value is False
		   :return: if bValue is True returns process, otherwise returns bValue
		"""
#		self.writePayloadFile(payload) #output payload to text file
		#initiate server using subprocess
#		print(self.name," is sending JSON to node 2.")
		if (bValue==True):
			process = subprocess.Popen(['python3', 'node2.py'])
#			time.sleep(1)
#			p2pTime = p2p.end(startTime)
#			mongo.log({"Node":self.name,"P2P payload time in seconds":p2pTime})
#			print(self.name," to Node 2 payload time: ",p2pTime," seconds")
#			self.sendSocket(payload)
#			process.terminate()
			return process
		else:
			return bValue

	def sendSocket(self,payload,bValue):
		"""Send the JSON payload to the SSL server via socket
		   :param: payload - The JSON payload to send
		   :return: payload
		"""
		try:
#			print(self.name," client connecting on port 8080 using SSL")
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			ssl_sock=ssl.wrap_socket(s,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
			ssl_sock.connect(('localhost', 8080))
			ssl_sock.sendall(payload)
#			log = {"Node":self.name,"Payload sent to Node 2":str(payload)}
#			mongo.log(log)
#			time.sleep(5)
			ssl_sock.shutdown(1)
			ssl_sock.close()
		except Exception as e:
			print(e)
			ssl_sock.shutdown(1)
			ssl_sock.close()
		finally:
			if(bValue==True):
				self.receiveJson(True)
			return payload

	def writePayloadFile(self,payload):
		"""write the payload to a file called payload.txt
		   :param: payload: the JSON payload
		   :return: the outFile
		"""
		with open('payload.txt', 'wb') as outFile:
			outFile.write(payload)
		return outFile

	def receiveJson(self, bValue):
		"""Receive the JSON payload from RabbitMQ
		   :return: payload
		"""
		try:
			print("Connecting to localhost to receive messages from Node4")
			connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
			channel = connection.channel()
			print("Connecting to channel")
			queue = channel.queue_declare(queue='node4to1', passive=True)
			print("Queue node4to1 created")
			#callback function that will receive the message
			def callback(ch, method, properties, body):
				self.aesPayload = body
				if(bValue==True):
					self.recDecrPayload = self.aesDecrypt()
				else:
					self.recDecrPayload = self.aesDecrypt(self)
				print(" [x] Decrypted message received %r" % self.recDecrPayload)
				channel.stop_consuming()
				return self.recDecrPayload
			channel.basic_consume(callback, queue='node4to1', no_ack=True)
			print(' [*] Waiting for messages. To exit press CTRL+C')
			channel.start_consuming()
			return self.recDecrPayload
		except Exception as e:
			print(e)

	def aesDecrypt(self):
		"""Decrypt the payload after it is received
		   :return: decrypted JSON payload
		"""
		try:
			obj = AES.new('This is a key123',AES.MODE_CBC,'This is an IV456')
			print(self.name," is decrypting the received payload using AES decryption")
			self.recDecrPayload = obj.decrypt(self.aesPayload)
			self.recDecrPayload = self.recDecrPayload.strip()
			log = {"Node":self.name,"AES Encrypted payload received from Node 4":str(self.aesPayload),"AES Decrypted JSON payload":str(self.recDecrPayload)}
			mongo.log(log)
			return self.recDecrPayload
		except Exception as e:
			print(e)

def main():
	mongo.log("Start Project Diamond")
	print("Starting Node 1...")
	node1 = Node1("Node 1")
	print(node1.name," is getting a JSON payload via CURL...")
	node1.payload = node1.getCurlMessage() #get original JSON payload using cURL
	log = {"Node":node1.name,"Payload Received through CURL":str(node1.payload)}
	mongo.log(log)
	node1.writePayloadFile(node1.payload) #output payload to text file
	mongo.log("Payload written to file: payload.txt")
	print(node1.name," is sending JSON to node 2.")
	node1.p = node1.sslServerInitiate(node1.payload, True)
	time.sleep(1)
	p2pTime = p2p.end(startTime)
	mongo.log({"Node":node1.name,"P2P payload time in seconds":p2pTime})
	print(node1.name," to Node 2 payload time: ",p2pTime," seconds")
	print(node1.name," client connecting on port 8080 using SSL")
	node1.payload = node1.sendSocket(node1.payload, True)
	log = {"Node":node1.name,"Payload sent to Node 2":str(node1.payload)}
	mongo.log(log)
	node1.p.terminate()
#	finalPayload = node1.receiveJson()
#	print("Final Payload = " , finalPayload)
	p2pTotalTime = p2p.calcTotal()
	print("Total P2P payload time: ",p2pTotalTime," seconds")
	mongo.log({"Total P2P payload time":p2pTotalTime})

if __name__ == '__main__':
	main()

