# from Lab5 Skeleton

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

class Routing (object):
    def __init__ (self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection
        # This binds our PacketIn event listener
        connection.addListeners(self)
        self.mac_to_port = {}


    def get_out_port(self, event, dst_mac):
    # Determining output port based on MAC address
        return self.mac_to_port.get(dst_mac, of.OFPP_FLOOD)  # Default to flooding


    def forward_packet(self, event, out_port):
        # Forward packet using flow rule
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)
        pass

    def do_routing (self, packet, packet_in, port_on_switch, switch_id):
        # port_on_swtich - the port on which this packet was received
        # switch_id - the switch which received this packet
        log.info(f"Routing packet {packet} received on switch {switch_id} port {port_on_switch}")
        # Your code here


    def _handle_PacketIn (self, event):
        # Handles packet in messages from the switch
        packet = event.parsed # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

    src_ip = dst_ip = None

    if packet.find('ipv4'):
            src_ip = str(packet.find('ipv4').srcip)
            dst_ip = str(packet.find('ipv4').dstip)


    # Define protocol
    protocol = None
    # Extracting IP
    if packet.find('ipv4'):
      src_ip = str(packet.find('ipv4').srcip)
      dst_ip = str(packet.find('ipv4').dstip)
      
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
    # Note, shorthand IP for referencing department !!
    allowed_icmp = [
        ("169.233.1", "169.233.3"), # From IT to Faculty
        ("169.233.1", "169.233.4"), # From IT to Student Housing
      ]
    
    # Devices on same subnet
    # Covering all base cases (same, src+dst, = allowed, dst+src, or = allowedicmp)
    if protocol == "ICMP":
        if src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_icmp or (dst_subnet, src_subnet) in allowed_icmp:
            log.info(f"Allowing ICMP Traffic {src_ip} -> {dst_ip}")
            self.forward_packet(event, self.get_out_port(event, dst_ip))
        else:
            log.warning(f"Blocking ICMP {src_ip} -> {dst_ip}")




    # Rule 2: TCP Traffic Restrictions
        allowed_tcp = [
            ("169.233.2", "169.233.1"),  # University Data Center ↔ IT
            ("169.233.2", "169.233.3"),  # University Data Center ↔ Faculty
            ("169.233.2", "169.233.4"),  # University Data Center ↔ Student Housing
            ("169.233.5", "169.233.5"),  # TrustedPCs ↔ Guest
        ]

        # Faculty LAN is the only group allowed to access Exam Server
        if protocol == "TCP":
            if dst_ip == "169.233.2.1" and src_subnet != "169.233.3":
                log.warning(f"Blocking TCP access to Exam Server from {src_ip}")
            # Allow TCP only if it meets defined criteria
            elif src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_tcp or (dst_subnet, src_subnet) in allowed_tcp:
                log.info(f"Allowing TCP {src_ip} -> {dst_ip}")
                self.forward_packet(event, self.get_out_port(event, dst_ip))
            else:
                log.warning(f"Blocking TCP {src_ip} -> {dst_ip}")




    # Rule 3: UDP Traffic Restrictions
    allowed_udp = [
        ("169.233.2", "169.233.1"),  # University Data Center ↔ IT
        ("169.233.2", "169.233.3"),  # University Data Center ↔ Faculty
        ("169.233.2", "169.233.4"),  # University Data Center ↔ Student Housing
    ]

    if protocol == "UDP":
       if src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_udp or (dst_subnet, src_subnet) in allowed_udp:
        log.info(f"Allowing UDP {src_ip} -> {dst_ip}")
        self.forward_packet(event, self.get_out_port(event, dst_ip))
    else:
        log.warning(f"Blocking UDP {src_ip} -> {dst_ip}")




    # Rule 4: Guest Can Use the Printer
    if src_subnet == "169.233.5" and dst_ip == "169.233.3.30":
        log.info(f"Allowing Guest to Access Printer: {src_ip} -> {dst_ip}")
        self.forward_packet(event, self.get_out_port(event, dst_ip))
        return




    # Rule 5: Default Deny (Drop All Other Traffic)
    log.warning(f"Blocking Unauthorized Traffic: {src_ip} -> {dst_ip} ({protocol})")
    return


def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
