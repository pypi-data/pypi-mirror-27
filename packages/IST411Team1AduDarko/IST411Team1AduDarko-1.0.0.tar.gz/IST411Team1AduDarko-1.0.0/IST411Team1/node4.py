#Project: Project Diamond, node4
#Purpose Details: This node receives a JSON payload via a Pyro4 Proxy to a remote object's (node3) URI, receives a checksum for the payload
#from the same Proxy, validates the checksum against a self generated checksum on the received payload, encrypts the payload with AES
#encryption, sends the payload to a RabbitMQ consumer (node1) after
#declaring a channel and queue on which to communicate, and logs every activity using node5's Node5 class log method. Point to point
#payload time from this node to the start of the next node is calculated using Team 1's p2p module.
#Author: Shawn Conway
#Date Developed: 11/21/2017
#Last Date Changed: 11/26/2017
#Rev: 1.2.9

import Pyro4, sys, subprocess, pika, zlib, serpent, time, p2p
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from node5 import Node5

beginTime = p2p.start()
class node4:

	def __init__(self,name):
		self.json = None
		self.name = name
		self.payloadHash = None
		self.cipherText = None

	def receiveJSON(self,argv):
		try:
			print(self.name + " is pulling in the remote object's URI.")
			self.uri = argv
			log = {"Node":self.name,"URI Received from Node 3":str(self.uri)}
			Node5.log(log)
			print(self.name + " is creating a remote object with the URI.")
			json_getter = Pyro4.Proxy(self.uri)
			print(self.name + " is getting the JSON from the remote object's get_json().")
			compJson = json_getter.get_json()
			print("Decompressing received payload...")
			self.json = zlib.decompress(serpent.tobytes(compJson))
			checksum = json_getter.getChecksum()
			try:
				json_getter.shutDown()
			except:
				pass
			log = {"Node":self.name,"JSON Received via Pyro4":str(self.json),"Checksum received via Pyro4":str(checksum)}
			Node5.log(log)
			print(self.name," JSON received: ", self.json)
			print(self.name," Verifying data integrity with checksum match...")
			genChecksum = zlib.crc32(self.json)
			if checksum == genChecksum:
				print(self.name,": checksum match indicates that received data is intact.")
				log = {"Node":self.name,"Checksum received via Pyro4 matches":"True","Checksum received via Pyro4":str(checksum),"Checksum generated for matching":str(genChecksum)}
				Node5.log(log)
				return self.json
			else:
				print(self.name,": checksum non-match indicates that received data has been compromised.")

		except Exception as e:
			print(e)

	def sendJSON(self):
		sent = False
		try:
			print(self.name," connecting to localhost")
			connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
			channel = connection.channel()
			channel.queue_declare('node4to1')
			print(self.name," channel connected.")
			#self.aesEncrypt()
			channel.basic_publish(exchange='',routing_key='node4to1',body=self.cipherText)
			log = {"Node":self.name,"AES Encrypted message sent":"True"}
			Node5.log(log)
			sent = True
			return sent
			connection.close()
		except Exception as e:
			Sent = False
			print(e)
			return sent 

	def aesEncrypt(self):
		try:
			pad = b' '
			key = 'This is a key123'
			obj = AES.new(key,AES.MODE_CBC,'This is an IV456')
			payload = self.json
			length = 16 - (len(payload)%16)
			payload += length*pad
			print(self.name," is encrypting the JSON with AES")
			self.cipherText = obj.encrypt(payload)
			print(self.name,"'s encrypted payload: ",self.cipherText)
			log = {"Node":self.name,"AES Encrypted Payload":str(self.cipherText)}
			Node5.log(log)
			return self.cipherText
		except Exception as e:
			print(e)
if __name__ == "__main__":
	print("Starting Node 4...")
	node4 = node4("Node 4")
	node4.receiveJSON(sys.argv[1])
	node4.aesEncrypt()
	p2pTime = p2p.end(beginTime)
	Node5.log({"Node":node4.name,"P2P payload time in seconds":p2pTime})
	print(node4.name," to Node 1 payload time: ",p2pTime," seconds")
	node4.sendJSON()






