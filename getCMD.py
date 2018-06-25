import docker
import time
import ovsWrapper
import ipaddress
import dockerpty
import sys
def getCMD(node):
	print ('Getting CMD for node %s' %node)
	APICli = docker.APIClient(base_url='unix://var/run/docker.sock')
	dockerpty.start(APICli ,node)

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print 'Argument error: %s node_name' %(sys.argv[0])
	getCMD(sys.argv[1])
