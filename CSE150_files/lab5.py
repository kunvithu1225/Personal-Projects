from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def build(self):
        # Create switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Create hosts
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')

        # Link hosts to switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        # Link switches in a linear topology
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)

def run():
    # Create the network with a remote controller
    net = Mininet(topo=CustomTopo(), switch=OVSSwitch, controller=None)

    # Add the POX Controller (Ensure port matches POX settings)
    controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1',port=6633)

    net.start()
    print("\nNetwork is up and running. You can now run tests.\n")
    CLI(net)  # Start the Mininet CLI
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

