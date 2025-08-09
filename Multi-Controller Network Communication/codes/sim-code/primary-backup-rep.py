from mininet.net import Mininet  # Mininet library for creating network topologies
from mininet.topo import Topo  # Mininet library for defining network topologies
from mininet.node import RemoteController  # Mininet library for adding remote controllers
from mininet.cli import CLI  # Mininet library for interacting with the network via CLI
from mininet.log import setLogLevel  # Mininet function to set log levels
from ryu.base.app_manager import RyuApp  # Ryu library for creating Ryu applications
from ryu.controller import ofp_event  # Ryu library for handling OpenFlow events
from ryu.ofproto import ofproto_v1_3  # Ryu library for defining OpenFlow protocol version 1.3
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls  # Ryu library for event handling
import threading  # Python library for threading
import time  # Python library for time-related operations
import random  # Python library for generating random numbers

# Global variable to store the counter
counter = 0

# Define a simple network topology
class SimpleTopology(Topo):
    def build(self):
        # Add two switches and connect them
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(s1, s2)

# Ryu application for primary and backup controller functionality
class PrimaryBackupController(RyuApp):
    # Specify OpenFlow protocol version
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(PrimaryBackupController, self).__init__(*args, **kwargs)
        # Initialize instance variables
        self.is_primary = False  # Flag to indicate whether this instance is acting as the primary controller
        # Start a thread to perform failover handling
        self.failover_thread = threading.Thread(target=self.perform_failover, args=())
        self.failover_thread.daemon = True  # Set the thread as daemon to terminate with the main thread
        self.failover_thread.start()  # Start the failover handling thread

    # Event handler for switch features negotiation
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # Get datapath and OpenFlow protocol objects
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Add a flow entry to each switch to forward all packets to the controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                           ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    # Method to add a flow entry to a switch
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    # Method to simulate failover from primary to backup controller and vice versa
    def perform_failover(self):
        global counter
        while True:
            # Generate random sleep interval
            sleep_interval = random.uniform(5, 20)
            # Simulate failure of the primary controller after random seconds
            time.sleep(sleep_interval)
            print("Primary controller failure detected. Switching to backup controller.")
            self.is_primary = False  # Set this instance as not primary
            time.sleep(sleep_interval)
            print("Switching back to primary controller.")
            self.is_primary = True  # Set this instance as primary

# Main function
def main():
    setLogLevel('info')  # Set Mininet log level to info

    topo = SimpleTopology()  # Create an instance of the SimpleTopology class
    net = Mininet(topo=topo, controller=None)  # Create Mininet network with no default controller
    # Add primary and backup controllers to Mininet network
    primary_controller = net.addController('primary_controller', controller=RemoteController, ip='127.0.0.1', port=7000)
    backup_controller = net.addController('backup_controller', controller=RemoteController, ip='127.0.0.1', port=7001)

    net.start()  # Start Mininet network

    # Start Primary controller
    primary = PrimaryBackupController('primary_controller')
    primary.is_primary = True  # Set this instance as primary
    primary.start()

    # Start Backup controller
    backup = PrimaryBackupController('backup_controller')
    backup.start()

    try:
        global counter
        while True:
            if primary.is_primary:
                counter += 1  # Increment the counter only when the primary controller is active
                print(f"Counter on Primary Controller: {counter}")
            else:
                counter += 1  # Increment the counter even when the backup controller is active
                print(f"Counter on Backup Controller (Synced with Primary): {counter}")

            time.sleep(5)  # Sleep for 5 seconds

    except KeyboardInterrupt:
        pass
    finally:
        net.stop()  # Stop Mininet network
        primary.stop()  # Stop Primary controller
        backup.stop()  # Stop Backup controller

if __name__ == '__main__':
    main()
