# SDN-Based Traffic Filtering using POX Controller

##  Project Overview
This project demonstrates Software Defined Networking (SDN) using Mininet and the POX OpenFlow controller. It focuses on implementing traffic filtering using controller-based logic.

The controller applies a drop rule to block traffic from host h1 to host h2, showcasing centralized control in SDN.

---

##  Objectives
- Understand SDN architecture
- Implement controller-switch interaction
- Apply match–action flow rules
- Demonstrate traffic filtering
- Observe packet loss behavior

---

##  Network Topology

h1 (10.0.0.1) ----\
                    [ s1 Switch ] ---- POX Controller
h2 (10.0.0.2) ----/

- 2 Hosts: h1, h2
- 1 Switch: s1
- Remote Controller: POX

---

##  Technologies Used
- Mininet
- POX Controller
- OpenFlow Protocol
- Ubuntu (Linux)

---

##  SDN Behavior Demonstrated

| Behavior        | Description                          |
|----------------|--------------------------------------|
| Packet Drop    | h1 → h2 traffic is blocked           |
| Flow Matching  | Based on source & destination IP     |
| Packet Loss    | 100% loss observed                   |
| Controller     | Handles PacketIn events              |

---

##  Controller Logic

The controller:
1. Listens for PacketIn events
2. Extracts IP information
3. Applies rules:

- If traffic is from **h1 → h2** → DROP
- Otherwise → FORWARD (flood)

---

##  Setup & Installation

### Step 1: Install Mininet
```bash
sudo apt update
sudo apt install mininet -y
Step 2: Clone POX
git clone https://github.com/noxrepo/pox.git
cd pox
 How to Run
Terminal 1: Start Controller
cd ~/pox
python3 pox.py controller
Terminal 2: Start Mininet
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6633
 Test Commands
h1 ping -c 5 h2
h2 ping -c 5 h1
pingall
 Results
 Ping from h1 to h2
100% packet loss
Traffic successfully blocked
 Pingall Output
100% dropped (0/2 received)
 Screenshots
1. Controller Running

Shows POX controller active and switch connected
 screenshots/controller_running.png

2. Packet Drop Log

Controller log showing:

IP 10.0.0.1 -> 10.0.0.2
DROP h1 -> h2

 screenshots/drop_log.png

3. Mininet Topology

Command:

net

 screenshots/topology.png

4. Ping Test (h1 → h2)
100% packet loss

 screenshots/ping_test.png

5. Pingall Result
*** Results: 100% dropped (0/2 received)

 screenshots/pingall.png

6. ARP Table

Shows MAC resolution working
 screenshots/arp_table.png

 Analysis
The drop rule successfully blocks traffic from h1 to h2
Packet loss confirms enforcement of controller logic
Reverse traffic is also affected due to simplified forwarding logic
 Limitations
Reverse communication (h2 → h1) may fail
Basic flooding logic used instead of optimized routing
 Conclusion

This project successfully demonstrates SDN concepts using the POX controller. Traffic filtering is implemented using flow rules, and the effect is observed through packet loss.

It highlights how SDN enables centralized control over network behavior.

 Project Structure
project/
├── controller.py
├── README.md
└── screenshots/
    ├── controller_running.png
    ├── drop_log.png
    ├── topology.png
    ├── ping_test.png
    ├── pingall.png
    └── arp_table.png
