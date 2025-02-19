# from Lab5 Skeleton

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

class Routing(object):
    def __init__(self, connection):
        # Keep track of the connection to the switch
        self.connection = connection
        # This binds our PacketIn event listener
        connection.addListeners(self)
        self.mac_to_port = {}

    def get_out_port(self, dst_mac):
        """Determining output port based on MAC address."""
        return self.mac_to_port.get(dst_mac, of.OFPP_FLOOD)  # Default to flooding

    def forward_packet(self, event, out_port):
        """Forward packet using a flow rule."""
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)

    def do_routing(self, packet, packet_in, port_on_switch, switch_id):
        """Routing logic."""
        log.info(f"Routing packet {packet} received on switch {switch_id} port {port_on_switch}")

    def _handle_PacketIn(self, event):
        """Handles packet in messages from the switch."""
        packet = event.parsed  # Parsed packet data
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp  # OpenFlow packet message
        self.do_routing(packet, packet_in, event.port, event.dpid)


        # Allowing ARP Traffic to Fix Packet Losses
        if packet.find('arp'):
            log.info("Allowing ARP Traffic")
            self.forward_packet(event, of.OFFP_FLOOD)
            return 


        # Extract IPv4 addresses
        ip_packet = packet.find('ipv4')
        if ip_packet is None:
            return  # Ignore non-IP packets

        src_ip = str(ip_packet.srcip)
        dst_ip = str(ip_packet.dstip)

        # Define protocol type
        protocol = None
        if packet.find('icmp'):
            protocol = "ICMP"
        elif packet.find('tcp'):
            protocol = "TCP"
        elif packet.find('udp'):
            protocol = "UDP"

        # Extracting source and destination subnets
        src_subnet = ".".join(src_ip.split(".")[:3])
        dst_subnet = ".".join(dst_ip.split(".")[:3])

        # RULE 1: ICMP Traffic Restrictions
        allowed_icmp = [
            ("169.233.1", "169.233.3"),  # IT to Faculty
            ("169.233.1", "169.233.4"),  # IT to Student Housing
        ]

        if protocol == "ICMP":
            if src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_icmp or (dst_subnet, src_subnet) in allowed_icmp:
                log.info(f"Allowing ICMP Traffic {src_ip} -> {dst_ip}")
                self.forward_packet(event, self.get_out_port(dst_ip))
            else:
                log.warning(f"Blocking ICMP {src_ip} -> {dst_ip}")

        # RULE 2: TCP Traffic Restrictions
        allowed_tcp = [
            ("169.233.2", "169.233.1"),  # Data Center to IT
            ("169.233.2", "169.233.3"),  # Data Center to Faculty
            ("169.233.2", "169.233.4"),  # Data Center to Student Housing
            ("169.233.5", "169.233.5"),  # TrustedPCs to Guest
        ]

        if protocol == "TCP":
            if dst_ip == "169.233.2.1" and src_subnet != "169.233.3":
                log.warning(f"Blocking TCP access to Exam Server from {src_ip}")
            elif src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_tcp or (dst_subnet, src_subnet) in allowed_tcp:
                log.info(f"Allowing TCP {src_ip} -> {dst_ip}")
                self.forward_packet(event, self.get_out_port(dst_ip))
            else:
                log.warning(f"Blocking TCP {src_ip} -> {dst_ip}")

        # RULE 3: UDP Traffic Restrictions
        allowed_udp = [
            ("169.233.2", "169.233.1"),  # Data Center to IT
            ("169.233.2", "169.233.3"),  # Data Center to Faculty
            ("169.233.2", "169.233.4"),  # Data Center to Student Housing
        ]

        if protocol == "UDP":
            if src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_udp or (dst_subnet, src_subnet) in allowed_udp:
                log.info(f"Allowing UDP {src_ip} -> {dst_ip}")
                self.forward_packet(event, self.get_out_port(dst_ip))
            else:
                log.warning(f"Blocking UDP {src_ip} -> {dst_ip}")

        # RULE 4: Guest Can Use the Printer
        if src_subnet == "169.233.5" and dst_ip == "169.233.3.30":
            log.info(f"Allowing Guest to Access Printer: {src_ip} -> {dst_ip}")
            self.forward_packet(event, self.get_out_port(dst_ip))
            return

        # RULE 5: Default Deny (Drop All Other Traffic)
        log.warning(f"Blocking Unauthorized Traffic: {src_ip} -> {dst_ip} ({protocol})")
        return


def launch():
    """Starts the POX controller."""
    def start_switch(event):
        log.debug(f"Controlling {event.connection}")
        Routing(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
