    # Rule #1 & Rule #2: Allow ARP & ICMP (Implemented First)
    if protocol == "ARP" or protocol == "ICMP":
        accept_packet(event)
        return

    # Rule #3: Web Traffic (TCP between Laptop ↔ iPad)
    if ((src == "laptop" and dst == "iPad") or (src == "iPad" and dst == "laptop")) and protocol == "TCP":
        accept_packet(event)
        return

    # Rule #4: IoT Access
    if (src == "heater" and dst == "lights") and protocol == "UDP":
        accept_packet(event)
        return
    if (src == "iPad" and dst in ["lights", "heater"]) and protocol == "TCP":
        accept_packet(event)
        return
    if (src in ["lights", "heater"] and dst == "iPad") and protocol == "UDP":
        accept_packet(event)
        return

    # Rule #5: Laptop/iPad General Management (Allow UDP between laptop & iPad)
    if ((src == "laptop" and dst == "iPad") or (src == "iPad" and dst == "laptop")) and protocol == "UDP":
        accept_packet(event)
        return

    # Default Rule: Drop all other traffic
    drop_packet(event)
        return
