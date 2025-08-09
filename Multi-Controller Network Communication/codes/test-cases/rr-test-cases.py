from mininet.net import Mininet
from mininet.log import setLogLevel
from random import shuffle

class RoundRobinBalancer:
    def __init__(self, net):
        """
        Initialize the RoundRobinBalancer class.

        Parameters:
        - net: Mininet object
        """
        self.net = net
        self.servers = {}  # Dictionary to store server host info
        self.hosts = []  # List to store Mininet host objects
        self.current_index = 0  # Index to track current server for round-robin
        self.request_distribution = {}  # To track request distribution among servers
        self.load_balancing_efficiency = 0  # To track load balancing efficiency

    def add_hosts(self, num_hosts):
        """
        Method to add hosts to the network.

        Parameters:
        - num_hosts: Number of hosts to add to the network
        """
        for i in range(num_hosts):
            host_name = 'h{}'.format(i + 1)
            host = self.net.addHost(host_name)
            self.hosts.append(host)
            self.servers[host_name] = host
            self.request_distribution[host_name] = 0  # Initialize request count for each host

    def simulate_requests(self, num_requests):
        """
        Method to simulate incoming requests.

        Parameters:
        - num_requests: Number of requests to simulate
        """
        for i in range(num_requests):
            server = self.get_next_server()
            self.request_distribution[server] += 1

    def perform_load_balancing(self):
        """
        Method to perform round-robin load balancing.
        """
        total_requests = sum(self.request_distribution.values())
        ideal_load = total_requests / len(self.servers)  # Ideal load for perfect balancing

        # Calculate load balancing efficiency
        actual_loads = list(self.request_distribution.values())
        max_load = max(actual_loads)
        min_load = min(actual_loads)
        self.load_balancing_efficiency = 100 * (1 - ((max_load - min_load) / ideal_load))

    def get_next_server(self):
        """
        Method to get next server in round-robin sequence.
        """
        server = list(self.servers.keys())[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server

def run_simulation(num_hosts, num_requests):
    """
    Function to run the simulation.

    Parameters:
    - num_hosts: Number of hosts in the network
    - num_requests: Number of requests to simulate
    """
    net = Mininet()
    balancer = RoundRobinBalancer(net)
    balancer.add_hosts(num_hosts)

    # Simulate incoming requests
    balancer.simulate_requests(num_requests)

    # Perform load balancing
    balancer.perform_load_balancing()

    # Print results
    print("\nRequest Distribution (%):")
    for host, requests in balancer.request_distribution.items():
        percentage = (requests / sum(balancer.request_distribution.values())) * 100
        print(f"{host}: {percentage:.2f}%")

    print("\nLoad Balancing (%):")
    print(f"{balancer.load_balancing_efficiency:.2f}%")

    net.stop()

def main():
    setLogLevel('info')

    # Test Cases
    test_cases = [
        {"num_hosts": 3, "num_requests": 100},  # Best Case
        {"num_hosts": 3, "num_requests": 1000},  # Average Case
        {"num_hosts": 3, "num_requests": 10},  # Worst Case
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i + 1}:")
        run_simulation(test_case["num_hosts"], test_case["num_requests"])

if __name__ == '__main__':
    main()
