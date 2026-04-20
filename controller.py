from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class PacketDropController(object):

    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed

        if not packet.parsed:
            return

        # Check if it's an IP packet
        ip_packet = packet.find('ipv4')

        if ip_packet:
            src_ip = str(ip_packet.srcip)
            dst_ip = str(ip_packet.dstip)

            log.info(f"Packet from {src_ip} to {dst_ip}")

            # Drop rule: block h1 → h2
            if src_ip == "10.0.0.1" and dst_ip == "10.0.0.2":
                log.info("Dropping packet (h1 -> h2)")
                return  # No action → packet dropped

        # Allow all other traffic
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)


def launch():
    def start_switch(event):
        log.info("Controller connected")
        PacketDropController(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
