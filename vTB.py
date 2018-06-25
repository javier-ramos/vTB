#!/bin/python

import sys
import json
import getopt
import subprocess
from vTBTopo import *
from shell import *
topology={}
application={}
model={}
verbose = False







def usage():
	print('python vTB.py -t topoFile -a appFile -m modelFile -v -h')

def createTopology():
	topo=vTBTopo(topology)
	print type(topo)
	return topo	
	
	

def readConfig(tFile,aFile,mFile):
	global topology,application,model
	try:
		js = open(tFile).read()
		topology = json.loads(js)
	except Exception as err:
		print ('Error reading file %s: '%tFile+str(err))
		sys.exit(-2)
	try:
		js = open(aFile).read()
		application = json.loads(js)
	
	except Exception as err:
		print ('Error reading file %s: '%aFile+str(err))
		sys.exit(-2)
	try:
		js = open(mFile).read()
		model= json.loads(js)
	except Exception as err:
		print ('Error reading file %s: '%mFile+str(err))
		sys.exit(-2)
	if verbose==True:
		print ('Configuration loaded')
	
	


def main():

	try:
		opts, args = getopt.getopt(sys.argv[1:], "ht:a:m:v", ["help", "topology=","application=","model="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	topologyFile = None
	appFile = None
	modelFile = None
	
	for o, a in opts:
		if o == "-v":
		    verbose = True
		elif o in ("-h", "--help"):
		    usage()
		    sys.exit()
		elif o in ("-t", "--topology"):
		    topologyFile = a
		elif o in ("-a", "--application"):
		    appFile = a
		elif o in ("-m", "--model"):
		    modelFile = a

		else:
		    assert False, "unhandled option"
		
	if topologyFile==None or appFile == None or modelFile== None:
		usage()
		sys.exit(2)

	readConfig(topologyFile,appFile,modelFile)
	topo=createTopology()

	s=shell(topo)
	topo.stop()



if __name__ == "__main__":
	main()
		
