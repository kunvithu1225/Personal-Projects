#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
   
                    # ADDING HOSTS #

    # laptop1 = self.addHost('Laptop1', ip='200.20.2.8/24',defaultRoute="Laptop1-eth1")
    # MAC address: subnet identfier ->(XX) , Last octet ->(YY)

    # University Data Center /24
    examServer = self.addHost('examServer', ip='169.233.2.1/24', mac="00:00:00:00:10:01")
    webServer = self.addHost('webServer', ip='169.233.2.2/24', mac="00:00:00:00:10:01")
    dnsServer = self.addHost('dnsServer', ip='169.233.2.3/24', mac="00:00:00:00:10:03")

    # IT Department LAN
    itWS = self.addHost('itWS', ip='169.233.1.10/24', mac="00:00:00:00:02:01")
    itBackup = self.addHost('itBackup', ip='169.233.1.30/24', mac="00:00:00:00:02:02")
    itPC = self.addHost('itPC', ip='169.233.1.20', mac="00:00:00:00:2:03")

    # faculty LAN /24
    facultyWS = self.addHost('facultyWS', ip='169.233.3.10/24', mac="00:00:00:00:01:01")
    printer = self.addHost('printer', ip='169.233.3.30/24', mac="00:00:00:00:01:02")
    facultyPC = self.addHost('facultyPC', ip='169.233.3.30/24', mac="00:00:00:00:01:03")

    # student housing LAN /24
    studentPC1 = self.addHost('studentPC1', ip='169.233.4.1/24', mac="00:00:00:00:03:01")
    studentPC2 = self.addHost('studentPC2', ip='169.233.4.2/24', mac="00:00:00:00:03:02")
    labWS = self.addHost('labWS', ip='169.233.4.2/24', mac="00:00:00:00:03:03")

    # Internet
    # No subnet mask in the pdf? /24 or /32
    trustedPC1 = self.addHost('trustedPC1', ip='212.26.59.102', mac="00:00:00:00:04:01")
    trustedPC2 = self.addHost('trustedPC2', ip='10.100.198.6', mac="00:00:00:00:04:02")
    guest = self.addHost('guest', ip='10.100.198.10', mac="00:00:00:00:05:01")

    
                    # ADDING SWITCHES #
    
    # switch1 = self.addSwitch('s1') 
    s1 = self.addSwitch('s1'); # -> Faculty LAN
    s2 = self.addSwitch('s2'); # -> Student Housing LAN
    s3 = self.addSwitch('s3'); # -> IT Department LAN
    s4 = self.addSwitch('s4'); # -> University Data Center
    s5 = self.addSwitch('s5'); # -> Core Switch

    # self.addLink(laptop1, switch1, port1=1, port2=2)



if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
