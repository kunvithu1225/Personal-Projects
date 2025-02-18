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

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # Your code here
    pass


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)


    # Extracting IP
    if packet.find('ipv4'):
      src_ip = str(packet.find('ipv4').srcip)
      dst_ip = str(packet.find('ipv4').dstcip)


    # Define protocol
    protocol = None
    if packet.find('icmp'):
        protocol = "ICMP"
    elif packet.find('tcp'):
        protocol = "TCP"
    elif packet.find('udp'):
        protocol = "UDP"



    # Firewall Rules



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
        if src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_icmp or (dst_subnet, src_subnet):
            log.info(f"Allowing ICMP Traffic {src_ip} -> {dst_ip}")
            self.forward_packet(event, self.get_out_port(event, dst_ip))
        else:
            log.warning(f"Blocking ICMP {src_ip} -> {dst_ip}")




    # Rule 2: TCP Traffic Restrictions
    if protocol == "TCP":
        # Extract source and destination subnets
        src_subnet = ".".join(src_ip.split(".")[:3])
        dst_subnet = ".".join(dst_ip.split(".")[:3])

        allowed_tcp = [
            ("169.233.2", "169.233.1"),  # University Data Center ↔ IT
            ("169.233.2", "169.233.3"),  # University Data Center ↔ Faculty
            ("169.233.2", "169.233.4"),  # University Data Center ↔ Student Housing
            ("169.233.5", "169.233.5"),  # TrustedPCs ↔ Guest
        ]

        # Faculty LAN is the only group allowed to access Exam Server
        if dst_ip == "169.233.2.1" and src_subnet != "169.233.3":
            log.warning(f"Blocking TCP access to Exam Server from {src_ip}")
            return

        # Allow TCP only if it meets defined criteria
        if src_subnet == dst_subnet or (src_subnet, dst_subnet) in allowed_tcp or (dst_subnet, src_subnet) in allowed_tcp:
            log.info(f"Allowing TCP {src_ip} -> {dst_ip}")
            self.forward_packet(event, out_port)
        else:
            log.warning(f"Blocking TCP {src_ip} -> {dst_ip}")
        return

    # Rule 3: UDP Traffic Restrictions
    # Rule 4: Guest Can Use the Printer
    # Rule 5: Default Deny (Drop All Other Traffic)






def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
