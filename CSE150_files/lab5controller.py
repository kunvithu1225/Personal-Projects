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

        # Step 1: Allow ALL ARP (Fixes Packet Loss)
        if packet.find('arp'):
            log.info("Allowing ARP Traffic")
            msg = of.ofp_packet_out()
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Flood ARP packets
            self.connection.send(msg)
            return  # Skip further processing

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

        #  Step 2: Allow ICMP (Ping)
        if protocol == "ICMP":
            log.info("Allowing ICMP Traffic (Ping)")
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet_in)
            msg.idle_timeout = 60
            msg.hard_timeout = 300
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))  # Forward ICMP packets
            self.connection.send(msg)
            return


        # Step 3: Web Traffic (Allow TCP between Laptop <-> iPad)
        if protocol == "TCP" and (
            (src == "10.1.1.2" and dst == "10.1.1.1") or  # Laptop → iPad
            (src == "10.1.1.1" and dst == "10.1.1.2")     # iPad → Laptop
        ):
            log.info("Allowing Web Traffic: Laptop <-> iPad (TCP)")
            self.accept(packet_in)
            return

        # Step 4: IoT Traffic (Allow UDP between Heater <-> Lights)
        if protocol == "UDP" and (
            (src == "10.1.20.2" and dst == "10.1.20.1") or  # Heater → Lights
            (src == "10.1.20.1" and dst == "10.1.20.2")     # Lights → Heater
        ):
            log.info(" Allowing IoT Traffic: Heater <-> Lights (UDP)")
            self.accept(packet_in)
            return

        #  Step 5: Allow TCP between iPad <-> IoT (Heater/Lights)
        if protocol == "TCP" and (
            (src == "10.1.1.1" and dst in ["10.1.20.1", "10.1.20.2"]) or  # iPad → IoT
            (src in ["10.1.20.1", "10.1.20.2"] and dst == "10.1.1.1")     # IoT → iPad
        ):
            log.info(" Allowing TCP Traffic: iPad <-> IoT")
            self.accept(packet_in)
            return

        #  Step 6: Laptop/iPad General Management (Allow UDP)
        if protocol == "UDP" and (
            (src == "10.1.1.2" and dst == "10.1.1.1") or  # Laptop → iPad
            (src == "10.1.1.1" and dst == "10.1.1.2")     # iPad → Laptop
        ):
            log.info(" Allowing UDP Traffic: Laptop <-> iPad")
            self.accept(packet_in)
            return

        #  Default Deny Rule (Drop all other traffic)
        log.warning(" Dropping Packet: %s -> %s (%s)" % (src, dst, protocol))
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
        log.info(" Packet Accepted - Flow Installed")

    def drop(self, packet_in):
        """
        Drop the packet by installing a drop rule in the switch.
        """
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet_in)
        self.connection.send(msg)
        log.info(" Packet Dropped - Flow Installed")

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
