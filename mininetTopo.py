from vTBTopo import *
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, UserSwitch

class CustomTopo(Topo):
		def build(self, topology):
			for elem in topology['switches']:
				switch = self.addSwitch(elem)
			#creamos los hosts llamados hX donde X es su numero de host. Tambien creamos y asignamos los enlaces que interconectan los hosts con el switch
			for node in topology['nodes']:				
				host = self.addHost(node)

			for link in topology['links']:
				if(len(link)==2):
					self.addLink(link[0],link[1])
				if(len(link)==3):
					self.addLink(link[0],link[1],bw=link[2])
				if(len(link)==4):
					self.addLink(link[0],link[1],bw=link[2],delay=link[3])
class mininetTopo(vTBTopo.vTBTopo):
	
	
	def __init__(self,topology):

		self.topology=topology
		topo = CustomTopo(topology)
		self.net = Mininet(topo=topo,link=TCLink)
		#una vez creada la red arrancamos la emulacion
		net.start()
		#mostramos las conexiones
		print "Las conexiones son:"
		dumpNodeConnections(net.hosts)

	      
	      
		#print "Probando conectividad con ping"
		#Ejecutamos ping entre todos los hosts
		#net.pingAll()
		#La funcion CLI nos crea una linea de comandos de mininet para introducir comandos. Para automatizar este script se puede comentar esta linea
		#CLI(net)
	       	return net


	def stopScenarioMininet():
		net.stop()
