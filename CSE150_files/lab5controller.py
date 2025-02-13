# Lab 5 Firewall Controller
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall(object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """

    def __init__(self, connection):
        # Store the connection to the switch
        self.connection = connection

        # Bind the PacketIn event listener
        connection.addListeners(self)

    def do_firewall(self, packet, packet_in):
        """
        Implements the firewall logic for each incoming packet.
        """

        ip_packet = packet.find('ipv4')  # Extract IP layer
        if ip_packet is None:
            return  # Ignore non-IP packets

        src = str(ip_packet.srcip)
        dst = str(ip_packet.dstip)

        # Extract protocol
        protocol = None
        if packet.find('tcp'):
            protocol = "TCP"
        elif packet.find('udp'):
            protocol = "UDP"
        elif packet.find('icmp'):
            protocol = "ICMP"
        elif packet.find('arp'):
            protocol = "ARP"

        # Firewall Rules Based on Table 2

        # Rule #1 & Rule #2: Allow ARP & ICMP (Must be implemented first)
        if protocol in ["ARP", "ICMP"]:
            self.accept(packet_in)
            return

        # Rule #3: Web Traffic (Allow TCP between Laptop <-> iPad)
        if protocol == "TCP" and (
            (src == "laptop" and dst == "iPad") or
            (src == "iPad" and dst == "laptop")
        ):
            self.accept(packet_in)
            return

        # Rule #4: IoT Traffic
        if protocol == "UDP" and (
            (src == "heater" and dst == "lights") or
            (src == "iPad" and dst in ["lights", "heater"])
        ):
            self.accept(packet_in)
            return

        if protocol == "TCP" and (
            (src == "iPad" and dst in ["lights", "heater"])
        ):
            self.accept(packet_in)
            return

        # Rule #5: Laptop/iPad General Management (Allow UDP between Laptop <-> iPad)
        if protocol == "UDP" and (
            (src == "laptop" and dst == "iPad") or
            (src == "iPad" and dst == "laptop")
        ):
            self.accept(packet_in)
            return

        # Default Deny Rule (Drop all other traffic)
        self.drop(packet_in)

    def accept(self, packet_in):
        """
        Allow the packet by installing a flow rule in the switch.
        """
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet_in)
        msg.idle_timeout = 60  # Rule expires if inactive for 60s
        msg.hard_timeout = 300  # Rule expires after 5 minutes
        msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))  # Forward normally
        self.connection.send(msg)
        log.info("Packet Accepted - Flow Installed")

    def drop(self, packet_in):
        """
        Drop the packet by installing a drop rule in the switch.
        """
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet_in)
        self.connection.send(msg)
        log.info("Packet Dropped - Flow Installed")

    def _handle_PacketIn(self, event):
        """
        Handles PacketIn events from the switch.
        """
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp
        self.do_firewall(packet, packet_in)


def launch():
    """
    Starts the firewall when POX is launched.
    """
    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Firewall(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

