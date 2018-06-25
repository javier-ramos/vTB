import docker
import time
import ovsWrapper
import ipaddress
import dockerpty
from vTBTopo import *
class dockerTopo(vTBTopo):
	
	def __init__(self,topology):
		#cli = Client(base_url='unix://var/run/docker.sock')
		self.net=None;	
		self.APICli = docker.APIClient(base_url='unix://var/run/docker.sock')
		self.cli= docker.from_env()
		self.ovsW=ovsWrapper.OVSWrapper()
		self.nIP=1
		self.net=ipaddress.ip_network(u'%s/%s' %(topology['net'],topology['mask']))
		self.topology=topology
	
		self.node={}

		for elem in topology['switches']:
			if self.ovsW.createSwitch(elem)==True:
				print ('Switch %s created' % elem)


	
		for elem in topology['nodes']:

			try:	
				container=self.cli.containers.get(elem)
				print container
				print 'Reusing container '+elem
				container.restart()
				print(container.exec_run('/sbin/ifconfig eth0 down',privileged=True))
			except Exception as ex:
				print 'Creating container '+elem

			 	container = self.APICli.create_container('ubuntu:latest',name=elem,tty=True,stdin_open = True,command='/bin/bash')
				container=self.cli.containers.get(elem)
				container.start()
				#print(container.exec_run('apt -yqq update'))
		 		#print(container.exec_run('apt -yqq install iputils-ping'))
				#print(container.exec_run('apt -yqq install net-tools'))
				print(container.exec_run('/sbin/ifconfig eth0 down',privileged=True))
	
		
		for link in topology['links']:
			print 'Adding Link '+str(link)
			if(len(link)==2):
				self.ovsW.connectContainer(link[0],link[1],'%s/%s' %(self.net[self.nIP],topology['mask']))
			if(len(link)==3):
				self.ovsW.connectContainer(link[0],link[1],'%s/%s' %(self.net[self.nIP],topology['mask']))
			self.nIP+=1
	#			self.addLink(link[0],link[1],bw=link[2])
	#		if(len(link)==4):
	#			self.addLink(link[0],link[1],bw=link[2],delay=link[3])
		
			#print(container.exec_run('/sbin/ifconfig'))
	
		for elem in topology['nodes']:
				container=self.cli.containers.get(elem)
				#print(container.exec_run('/sbin/ifconfig'))
				#print(container.exec_run('/bin/ping %s -c 3' %(self.net[1])))
	
		#container.stop()
	

	def stop(self):
		print 'Stopping topology'
		for link in self.topology['links']:
			print 'Adding Link '+str(link)
			if(len(link)==2):
				self.ovsW.disconnectContainer(link[0],link[1])
			if(len(link)==3):
				self.ovsW.disconnectContainer(link[0],link[1])

		for elem in self.topology['switches']:
			if self.ovsW.deleteSwitch(elem)==True:
				print ('Switch %s deleted' % elem)



