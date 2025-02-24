#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSController

class MyTopology(Topo):
    def __init__(self):
        Topo.__init__(self)

        # ADDING SWITCHES  #
        s1 = self.addSwitch('s1')  # University Data Center
        s2 = self.addSwitch('s2')  # IT Department LAN
        s3 = self.addSwitch('s3')  # Faculty LAN
        s4 = self.addSwitch('s4')  # Student Housing LAN
        s5 = self.addSwitch('s5')  # Internet  
        s6 = self.addSwitch('s6')  # Core Router Switch

        # ADDING ROUTER HOST
        router = self.addHost('r1', ip='169.233.1.254/24')

        # CONNECT ROUTER TO ALL NETWORK SWITCHES
        self.addLink(router, s1)
        self.addLink(router, s2)
        self.addLink(router, s3)
        self.addLink(router, s4)
        self.addLink(router, s5)
        self.addLink(router, s6)

        # CONNECT SWITCHES TO THE CORE ROUTER SWITCH
        self.addLink(s1, s6)
        self.addLink(s2, s6)
        self.addLink(s3, s6)
        self.addLink(s4, s6)
        self.addLink(s5, s6)

        # ADDING HOSTS WITH CORRECT DEFAULT GATEWAY (r1)
        # University Data Center /24
        examServer = self.addHost('examServer', ip='169.233.2.1/24', mac="00:00:00:00:10:01", defaultRoute="via 169.233.1.254")
        webServer = self.addHost('webServer', ip='169.233.2.2/24', mac="00:00:00:00:10:02", defaultRoute="via 169.233.1.254")
        dnsServer = self.addHost('dnsServer', ip='169.233.2.3/24', mac="00:00:00:00:10:03", defaultRoute="via 169.233.1.254")

        # IT Department LAN /24
        itWS = self.addHost('itWS', ip='169.233.1.10/24', mac="00:00:00:00:02:01", defaultRoute="via 169.233.1.254")
        itBackup = self.addHost('itBackup', ip='169.233.1.30/24', mac="00:00:00:00:02:02", defaultRoute="via 169.233.1.254")
        itPC = self.addHost('itPC', ip='169.233.1.20/24', mac="00:00:00:00:02:03", defaultRoute="via 169.233.1.254")

        # Faculty LAN /24
        facultyWS = self.addHost('facultyWS', ip='169.233.3.10/24', mac="00:00:00:00:01:01", defaultRoute="via 169.233.1.254")
        printer = self.addHost('printer', ip='169.233.3.30/24', mac="00:00:00:00:01:02", defaultRoute="via 169.233.1.254")
        facultyPC = self.addHost('facultyPC', ip='169.233.3.40/24', mac="00:00:00:00:01:03", defaultRoute="via 169.233.1.254")

        # Student Housing LAN /24
        studentPC1 = self.addHost('studentPC1', ip='169.233.4.1/24', mac="00:00:00:00:03:01", defaultRoute="via 169.233.1.254")
        studentPC2 = self.addHost('studentPC2', ip='169.233.4.2/24', mac="00:00:00:00:03:02", defaultRoute="via 169.233.1.254")
        labWS = self.addHost('labWS', ip='169.233.4.3/24', mac="00:00:00:00:03:03", defaultRoute="via 169.233.1.254")

        # Internet Hosts
        trustedPC1 = self.addHost('trustedPC1', ip='212.26.59.102/24', mac="00:00:00:00:04:01", defaultRoute="via 169.233.1.254")
        trustedPC2 = self.addHost('trustedPC2', ip='10.100.198.6/24', mac="00:00:00:00:04:02", defaultRoute="via 169.233.1.254")
        guest = self.addHost('guest', ip='10.100.198.10/24', mac="00:00:00:00:05:01", defaultRoute="via 169.233.1.254")

        # CONNECTING HOSTS TO THEIR RESPECTIVE SWITCHES
        self.addLink(examServer, s1)
        self.addLink(webServer, s1)
        self.addLink(dnsServer, s1)
        self.addLink(itWS, s2)
        self.addLink(itBackup, s2)
        self.addLink(itPC, s2)
        self.addLink(facultyWS, s3)
        self.addLink(printer, s3)
        self.addLink(facultyPC, s3)
        self.addLink(studentPC1, s4)
        self.addLink(studentPC2, s4)
        self.addLink(labWS, s4)
        self.addLink(trustedPC1, s5)
        self.addLink(trustedPC2, s5)
        self.addLink(guest, s5)

if __name__ == '__main__':
    topo = MyTopology()
    net = Mininet(topo=topo, controller=OVSController, autoSetMacs=True)
    
    # ADDING CONTROLLER
    c0 = net.addController(name='c0', controller=OVSController)
    
    # START NETWORK
    net.start()

    # ENABLE IP FORWARDING ON THE ROUTER (r1)
    net.get('r1').cmd('sysctl -w net.ipv4.ip_forward=1')

    # TEST CONNECTIVITY
    print("Testing network connectivity...")
    net.pingAll()
    print("Testing complete. Entering CLI mode.")

    # ENTER CLI
    CLI(net)
    
    # STOP NETWORK
    net.stop()
