import docker
import time
import ovsWrapper
import ipaddress




class vTBTopo(object):
	def __new__(cls, topology):
		print 'NEw'
		if cls is vTBTopo and topology['virt'] == 'mininet':
			from mininetTopo import mininetTopo
			return object.__new__(mininetTopo, topology)
		elif cls is vTBTopo and topology['virt'] == 'docker':
			from dockerTopo import dockerTopo
			return object.__new__(dockerTopo, topology)
		else:
		    return object.__new__(cls, topology)
	def __init__(self,topology):
		self.topology=topology
	def stop(self):
        	raise NotImplementedError('users must define stop to use this base class')
	def getCMD(self,node):
        	raise NotImplementedError('users must define getCMD to use this base class')

