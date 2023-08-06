#Project Diamond, p2p.py
#Purpose Details: This module provides functionality for P2P payload time calculation; it allows for capturing of a start time, an end time, the time difference between those two as
#the P2P payload time, the ability to clear the p2pTime.txt file for reuse, and calculation of the sum of all nodes' P2P payload times.
#Author: Justin Grant
#Date Developed: 11/25/2017
#Last Date Changed: 11/26/2017
#Rev: 1.0.9
import sys, time

def start():
	startTime = time.clock()
	return startTime

def end(startTime):
	endTime = time.clock()
	p2pTime = endTime - startTime
	try:
		with open('p2pTime.txt','a') as outFile:
			outFile.write(str(p2pTime))
			outFile.write("\n")
	except Exception as e:
		print(e)
	return p2pTime

def clear():
	with open('p2pTime.txt', 'w'):
		pass

def calcTotal():
	total = 0
	with open('p2pTime.txt') as inFile:
		contentList = inFile.read().splitlines()
		for line in contentList:
			total += float(line)
		inFile.close()
	return total
