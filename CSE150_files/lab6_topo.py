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
    webServer = self.addHost('webServer', ip='169.233.2.2/24', mac="00:00:00:00:10:02")
    dnsServer = self.addHost('dnsServer', ip='169.233.2.3/24', mac="00:00:00:00:10:03")

    # IT Department LAN
    itWS = self.addHost('itWS', ip='169.233.1.10/24', mac="00:00:00:00:02:01", defaultRoute="itWS-eth0")
    itBackup = self.addHost('itBackup', ip='169.233.1.30/24', mac="00:00:00:00:02:02", defaultRoute="itBackup-eth0")
    itPC = self.addHost('itPC', ip='169.233.1.20', mac="00:00:00:00:02:03", defaultRoute="itPC-eth0")

    # faculty LAN /24
    facultyWS = self.addHost('facultyWS', ip='169.233.3.10/24', mac="00:00:00:00:01:01")
    printer = self.addHost('printer', ip='169.233.3.30/24', mac="00:00:00:00:01:02", defaultRoute="printer-eth0")
    facultyPC = self.addHost('facultyPC', ip='169.233.3.40/24', mac="00:00:00:00:01:03", defaultRoute="facultyPC-eth0")

    # student housing LAN /24
    studentPC1 = self.addHost('studentPC1', ip='169.233.4.1/24', mac="00:00:00:00:03:01")
    studentPC2 = self.addHost('studentPC2', ip='169.233.4.2/24', mac="00:00:00:00:03:02")
    labWS = self.addHost('labWS', ip='169.233.4.3/24', mac="00:00:00:00:03:03")

    # Internet
    # No subnet mask in the pdf? /24 or /32
    trustedPC1 = self.addHost('trustedPC1', ip='212.26.59.102/24', mac="00:00:00:00:04:01", defaultRoute="trustedPC1-eth0")
    trustedPC2 = self.addHost('trustedPC2', ip='10.100.198.6/24', mac="00:00:00:00:04:02", defaultRoute="trustedPC2-eth0")
    guest = self.addHost('guest', ip='10.100.198.10/24', mac="00:00:00:00:05:01", defaultRoute="guest-eth0")

    
                    # ADDING SWITCHES #
    
    # switch1 = self.addSwitch('s1') 
    s1 = self.addSwitch('s1'); # -> Univeristy Data Center
    s2 = self.addSwitch('s2'); # -> IT Department LAN
    s3 = self.addSwitch('s3'); # -> Faculty LAN
    s4 = self.addSwitch('s4'); # -> Student Housing LAN
    s5 = self.addSwitch('s5'); # -> Internet   



                # CONNECTING HOSTS TO SWITCHES
    # self.addLink(laptop1, switch1, port1=1, port2=2)

    # University Data Center (switch 1)
    self.addLink(examServer, s1)
    self.addLink(webServer, s1)
    self.addLink(dnsServer, s1)

    # IT Department Hosts (switch 2)
    self.addLink(itWS, s2)
    self.addLink(itBackup, s2)
    self.addLink(itPC, s2)

    # Faculty LAN Hosts (switch 3)
    self.addLink(facultyWS, s3)
    self.addLink(printer, s3)
    self.addLink(facultyPC, s3)

    # Student Housing Hosts (switch 4)
    self.addLink(studentPC1, s4)
    self.addLink(studentPC2, s4)
    self.addLink(labWS, s4)

    # Internet Hosts (switch 5)
    self.addLink(trustedPC1, s5)
    self.addLink(trustedPC2, s5)
    self.addLink(guest, s5)




if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
