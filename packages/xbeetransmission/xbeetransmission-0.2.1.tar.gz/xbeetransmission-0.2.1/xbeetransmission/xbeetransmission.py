#!/usr/bin/env python

import serial
import datetime	
import os
import time
import sys	
import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

##############################################################
# This functions is designed the securely and reliably send messages over xbee as serial
# data= the contents of a file or data you want to send
# ser = the serial interface for your xbee module
# symkey = the key you want to be used for AES encryption 
#############################################################
def xbeesend(data, ser, symkey):

    #Symmetric Keys must have a length that is a multiple of 16. Append x's until a multiple of 16
    while len(symkey) % 16 != 0:
        symkey += "x"

    #Decryption Key
    encryption_suite = AES.new(symkey, AES.MODE_CBC, 'This is an IV456')

    #Set data segment size to 8- bytes
    chunkSize = 80

    #get the length of the data, ie size of the input file in bytes
    bytes = len(data)

    #calculate the number of chunks to be created
    noOfChunks = bytes/80
    if(bytes%chunkSize):
        noOfChunks += 1
  
    #busy wait until it receives a message that the receiver is ready
    incoming = ser.readline().strip()
    while(incoming != "ACK0"):
        incoming = ser.readline().strip()

    ackNumber = 1
    chunkNames = []
    for i in range(0, bytes+1, chunkSize):
	#if the number of bytes left in the packet then is the last packet and you should break
        if(bytes - i < 80):
	        break
	#Send chunk over xbee
	hash =  hashlib.sha1(data[i:i+ chunkSize]).hexdigest()
	plainTextData = data[i:i+ chunkSize]
	#Encrypting data
	cipher_text = encryption_suite.encrypt(plainTextData)
	#Write data
	ser.write(cipher_text + hash[:10] + str(ackNumber).zfill(10))
	incoming = ser.readline().strip()
	#get time
	start = time.time()
	#busy wait until ack received for chunk sent
	while(incoming != "ACK" + str(ackNumber)):
	        incoming = ser.readline().strip()
	        #if it has been 90 sec since last ACK resend
	        if((time.time() - start) > 1):
	            ser.flush()
	            ser.write(data[i:i+ chunkSize] + hash[:10] + str(ackNumber).zfill(10))
	            #reset time
	            start = time.time()
        #increment acknowldgement number
        ackNumber += 1
    #tell receiver you are done sending packets
    ser.write(data[i:i+ chunkSize] + hash[:10] + "FIN".zfill(10))
    ser.close()


##############################################################
# This functions is designed the securely and reliably receive messages over xbee as serial
# ser = the serial interface for your xbee module
# symkey = the key you want to be used for AES encryption 
# filename = the name of the file you want to output to
#############################################################   
def xbeereceive(ser, symkey, filename):

    #Symmetric Keys must have a length that is a multiple of 16. Append x's until a multiple of 16
    while len(symkey) % 16 != 0:
        symkey += "x"

    #Decryption Key
    decryption_suite = AES.new(symkey, AES.MODE_CBC, 'This is an IV456')

    #get date and time for file name
    dt= str(datetime.datetime.now())

    #open new file
    k = open(filename, 'a')
    ackNumber = 0
    while True:
	print ackNumber	
	#read in 100 bytes (xbee max length)
	incoming = ser.read(100)
	#print incoming
	#if incoming is FIN exit
	if incoming[len(incoming)-3:] == "FIN":
		#Write the data that isn't the checksum or sequence number
		k.write(incoming[:-20])
        	k.close()
		ser.close()
		sys.exit(0)
	#busy wait until incoming changes
        elif incoming != "":
		#first 80 bytes is the encrypted data
		cipher_text = incoming[0:80]
		#Decrypt the data
                data = decryption_suite.decrypt(cipher_text)
		#Take sha1 hash the data
		hash = hashlib.sha1(data).hexdigest()
		#checksum of packet
		checksum = incoming[80:90]
		#Sequence number is equal to acknowledgement number then add leading zeros
		seqNum = str(ackNumber + 1).zfill(10)
		#checking integrity of file by checking sequence number of checksum
                if((hash[:10] == checksum) and seqNum == incoming[len(incoming)-10:]):
			#append to file incoming bytes
                	k.write(data)
                	ackNumber += 1
		else:
			ser.flush()
	#send ack with packet number
	ser.write("ACK" + str(ackNumber) + "\r\n")
