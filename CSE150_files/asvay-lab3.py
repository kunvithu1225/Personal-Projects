#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink


class MyTopology(Topo):
    # topology based on figure 1
    def __init__(self):
        Topo.__init__(self)

        # ✅ Adding switches (inside __init__)
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        # ✅ Add hosts with IP addresses
        laptop = self.addHost('h1', ip='10.1.1.2')
        ipad = self.addHost('h2', ip='10.1.1.1')
        lights = self.addHost('h3', ip='10.1.20.1')
        heater = self.addHost('h4', ip='10.1.20.2')

        # ✅ Adding links between devices and switches
        self.addLink(laptop, switch1, bw=750)
        self.addLink(ipad, switch1, bw=750)
        self.addLink(lights, switch2, bw=750)
        self.addLink(heater, switch2, bw=750)

        # ✅ Linking the two switches
        self.addLink(switch1, switch2, bw=750)


if __name__ == '__main__':
    topo = MyTopology()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    # Display connections and IP addresses
    print("\n-- Displaying connections --")
    print(net.links)

    print("\n-- Displaying IP Addresses --")
    for host in net.hosts:
        print(f"{host.name}: {host.IP()}")

    CLI(net)
    net.stop()
