from pox.core import core
import pox.openflow.libopenflow_01 as of
log = core.getLogger()


# This function is called whenever a switch sends a PacketIn message
def _handle_PacketIn(event):

    # Extract the packet from the event,if not parsed,ignore it
    packet = event.parsed
    if not packet.parsed:
        return

    # Always allow ARP packets (needed for MAC address resolution)
    if packet.type == packet.ARP_TYPE:

        # Create a packet_out message to send packet from controller to switch
        msg = of.ofp_packet_out()
        msg.data = event.ofp

        # Action: Flood packet to all ports (so hosts can discover each other)
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

        # Send message to switch
        event.connection.send(msg)
        return

    # Check if the packet is an IPv4 packet
    ip = packet.find('ipv4')

    if ip:
        # Extract source IP address
        src = str(ip.srcip)

        # Extract destination IP address
        dst = str(ip.dstip)

        # Print packet info in controller terminal
        log.info("IP Packet %s -> %s", src, dst)


        # -------------------- DROP RULE --------------------

        # If traffic is from h1 (10.0.0.1) to h2 (10.0.0.2)
        if src == "10.0.0.1" and dst == "10.0.0.2":

            # Log drop action
            log.info("DROP h1 -> h2")

            # Do nothing → packet is dropped
            return


    # -------------------- FORWARDING --------------------

    # Create packet_out message for forwarding
    msg = of.ofp_packet_out()

    # Attach original packet data
    msg.data = event.ofp

    # Action: Flood packet to all ports (basic forwarding)
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

    # Send packet to switch
    event.connection.send(msg)


# -------------------- CONTROLLER START --------------------

def launch():

    # Register PacketIn event to our handler function
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

    # Print message when controller starts
    log.info("CONTROLLER FULLY ACTIVE")
