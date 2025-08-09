# Import required libraries/modules
from mininet.net import Mininet  # Mininet library for creating network topologies
from mininet.topo import Topo  # Mininet library for defining network topologies
from mininet.node import RemoteController  # Mininet library for adding remote controllers
from mininet.log import setLogLevel, info  # Mininet library for logging
from mininet.cli import CLI  # Mininet library for command-line interface
from ryu.base import app_manager  # Ryu library for managing Ryu applications
from ryu.controller import ofp_event  # Ryu library for handling OpenFlow events
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER  # Ryu library for event handling
from ryu.controller.handler import set_ev_cls  # Ryu library for event decorator
from ryu.ofproto import ofproto_v1_3  # Ryu library for defining OpenFlow protocol version 1.3
from ryu.lib.packet import ethernet, packet  # Ryu library for packet parsing
from ryu.lib.packet import ipv4, tcp  # Ryu library for IP and TCP packet parsing
from ryu.lib import mac  # Ryu library for MAC address operations
from ryu.lib import hub  # Ryu library for cooperative multitasking
import logging  # Python logging library

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Define Ryu application for round-robin load balancing
class RoundRobinBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RoundRobinBalancer, self).__init__(*args, **kwargs)
        self.mac_to_port = {}  # Dictionary to store MAC addresses to ports mapping
        self.servers = {}  # Dictionary to store server host info
        self.hosts = []  # List to store Mininet host objects
        self.current_index = 0  # Index to track current server for round-robin

    # Method to add Mininet hosts to the network
    def add_hosts(self, num_hosts):
        for i in range(num_hosts):
            host_name = 'h{}'.format(i + 1)
            host = self.net.addHost(host_name)
            self.hosts.append(host)

    # Method to start Mininet network
    def start_mininet(self):
        self.net = Mininet(topo=None, build=False)
        self.add_hosts(num_hosts=3)  # Add 3 hosts
        self.net.build()
        self.net.start()

    # Method to handle incoming packets and perform round-robin load balancing
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            ip = pkt.get_protocol(ipv4.ipv4)
            tcp_pkt = pkt.get_protocol(tcp.tcp)
            if ip and tcp_pkt:
                server = self.get_next_server()  # Get next server in round-robin
                out_port = self.mac_to_port[server.mac]
                actions = [parser.OFPActionOutput(out_port)]
                data = None
                if msg.buffer_id == ofp.OFP_NO_BUFFER:
                    data = msg.data
                out = parser.OFPPacketOut(
                    datapath=dp, buffer_id=msg.buffer_id, in_port=msg.match['in_port'],
                    actions=actions, data=data)
                dp.send_msg(out)

    # Method to get next server in round-robin sequence
    def get_next_server(self):
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server

# Main function
def main():
    net = Mininet(controller=None)  # Create Mininet network without default controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=7000)  # Add remote controller c0
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=7001)  # Add remote controller c1
    s1 = net.addSwitch('s1')  # Add switch s1

    h1 = net.addHost('h1')  # Add host h1
    h2 = net.addHost('h2')  # Add host h2
    h3 = net.addHost('h3')  # Add host h3

    net.addLink(h1, s1)  # Add link between h1 and s1
    net.addLink(h2, s1)  # Add link between h2 and s1
    net.addLink(h3, s1)  # Add link between h3 and s1

    net.start()  # Start Mininet network
    s1.start([c0, c1])  # Start switch s1 with controllers c0 and c1

    rr_balancer = RoundRobinBalancer()  # Instantiate round-robin load balancer
    rr_balancer.start_mininet()  # Start Mininet network for the balancer
    hub.spawn(rr_balancer.start)  # Spawn a green thread to start the balancer

    CLI(net)  # Start Mininet CLI
    net.stop()  # Stop Mininet network

# Entry point of the script
if __name__ == '__main__':
    main()
