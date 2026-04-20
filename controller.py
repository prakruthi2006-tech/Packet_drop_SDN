from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    # CRITICAL: ALWAYS allow ARP
    if packet.type == packet.ARP_TYPE:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    ip = packet.find('ipv4')

    if ip:
        src = str(ip.srcip)
        dst = str(ip.dstip)

        log.info("IP Packet %s -> %s", src, dst)

        # DROP ONLY h1 → h2
        if src == "10.0.0.1" and dst == "10.0.0.2":
            log.info("DROP h1 -> h2")
            return

    # ALWAYS forward everything else
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("CONTROLLER FULLY ACTIVE")
