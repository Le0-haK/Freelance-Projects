import threading
import time
import random

class PrimaryController:
    def __init__(self, monitor):
        # Initialize primary controller attributes
        self.is_alive = True  # Flag to indicate if the primary controller is alive
        self.heartbeat_interval = 3  # Heartbeat interval in seconds
        self.monitor = monitor  # Reference to the Monitor instance

    def start_heartbeat(self):
        """Start sending heartbeats."""
        # Start a new thread for sending heartbeats
        threading.Thread(target=self.send_heartbeat).start()

    def send_heartbeat(self):
        """Send periodic heartbeats to the monitor."""
        while True:
            # Wait for the heartbeat interval
            time.sleep(self.heartbeat_interval)
            # Check if primary controller is alive and send heartbeat to monitor
            if self.is_alive:
                self.monitor.receive_heartbeat("Primary")
            else:
                break  # Exit the loop if primary is not alive

    def simulate_failure(self):
        """Simulate primary controller failure and recovery."""
        while True:
            # Simulate primary failure after random time
            time.sleep(random.randint(10, 15))
            print("Primary is down")
            self.is_alive = False  # Set primary as down
            self.monitor.detect_failure("Primary")  # Notify monitor about primary failure
            # Simulate downtime
            time.sleep(random.randint(5, 10))
            print("Primary is up")
            self.is_alive = True  # Set primary as up
            self.monitor.restore_primary()  # Notify monitor about primary recovery

class BackupController:
    def __init__(self, monitor):
        # Initialize backup controller attributes
        self.is_active = False  # Flag to indicate if the backup controller is active
        self.heartbeat_interval = 3  # Heartbeat interval in seconds
        self.monitor = monitor  # Reference to the Monitor instance

    def start_heartbeat(self):
        """Start sending heartbeats."""
        # Start a new thread for sending heartbeats
        threading.Thread(target=self.send_heartbeat).start()

    def send_heartbeat(self):
        """Send periodic heartbeats to the monitor."""
        while True:
            # Wait for the heartbeat interval
            time.sleep(self.heartbeat_interval)
            # Check if backup controller is active and send heartbeat to monitor
            if self.is_active:
                self.monitor.receive_heartbeat("Backup")
            else:
                break  # Exit the loop if backup is not active

    def activate(self):
        """Activate the backup controller."""
        self.is_active = True  # Set backup as active
        print("Backup controller is active")

class Monitor:
    def __init__(self):
        # Initialize monitor attributes
        self.primary_controller = PrimaryController(self)  # Create an instance of PrimaryController
        self.backup_controller = BackupController(self)  # Create an instance of BackupController
        self.primary_alive = True  # Flag to indicate if the primary controller is alive
        self.lock = threading.Lock()  # Lock for thread safety

    def start(self):
        """Start monitoring the primary controller."""
        self.primary_controller.start_heartbeat()  # Start sending heartbeats

    def receive_heartbeat(self, controller_type):
        """Receive heartbeats from controllers."""
        with self.lock:
            if controller_type == "Primary":
                # If heartbeat received from primary, update primary_alive status
                if not self.primary_alive:
                    print("Heartbeat from primary is coming, so primary is up")
                    self.primary_alive = True  # Set primary as up if it was down
            elif controller_type == "Backup":
                print("Heartbeat from backup controller")

    def detect_failure(self, controller_type):
        """Detect failure of primary controller."""
        with self.lock:
            if controller_type == "Primary":
                print("No Heartbeat coming so Primary is down, activating backup...")
                self.primary_alive = False  # Set primary as down
                self.backup_controller.activate()  # Activate backup controller

    def restore_primary(self):
        """Restore the primary controller after recovery."""
        with self.lock:
            print("Heartbeat coming so Restoring primary controller...")
            self.primary_alive = True  # Set primary as up
            self.primary_controller.start_heartbeat()  # Start sending heartbeats again

if __name__ == "__main__":
    monitor = Monitor()  # Create an instance of Monitor
    monitor.start()  # Start monitoring the primary controller

    # Simulate repeated primary failures and recoveries
    threading.Thread(target=monitor.primary_controller.simulate_failure).start()
