import ovs
from subprocess import call, check_call, check_output,Popen, PIPE, STDOUT,CalledProcessError

class OVSWrapper():
        def __init__(self):
		print ('Creating OVSWrapper')

	def createSwitch(self,name):
		ret=''
		try:
			ret=check_output(['ovs-vsctl','add-br',name])
		except CalledProcessError as ex:
			print ('Switch %s not created '%name)
			print(ex)
			return False
		try:
			ret=check_call(['ovs-vsctl','br-exists',name])
			return True
		except CalledProcessError as ex:
			print ('Switch %s not created '%name)
			return False
			
	def deleteSwitch(self,name):
		check_output(['ovs-vsctl','del-br',name])
		
	def connectContainer(self,containerName,switchName,IP):
		ret=''
		print('Connecting container %s to switch %s'%(containerName,switchName))
		try:
			ret=check_output(['ovs-docker','add-port',switchName,'%s-eth0'%(containerName),containerName,'--ipaddress=%s'%IP])	
			print 'Ret '+ret
			return True
		except CalledProcessError as ex:
			print(ex)
			return False

	def disconnectContainer(self,containerName,switchName):
		ret=''
		print('Disconnecting container %s from switch %s'%(containerName,switchName))
		try:
			ret=check_output(['ovs-docker','del-port',switchName,'%s-eth0'%(containerName),containerName])	
			print 'Ret '+ret
			return True
		except CalledProcessError as ex:
			print(ex)
			return False

