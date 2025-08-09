import threading  # Import threading module for managing multiple threads
import time  # Import time module for time-related functions
import random  # Import random module for generating random numbers

class PrimaryBackupController:
    def __init__(self, *args, **kwargs):
        # Initialize variables to store failover times and data consistencies
        self.failover_times = []  # List to store failover times
        self.data_consistencies = []  # List to store data consistencies

        # Initialize threads for failover and data synchronization
        self.failover_thread = threading.Thread(target=self.perform_failover, args=())  # Thread for failover simulation
        self.failover_thread.daemon = True  # Set the thread as daemon (background) thread
        self.failover_thread.start()  # Start the failover thread

        self.sync_thread = threading.Thread(target=self.perform_sync, args=())  # Thread for data synchronization simulation
        self.sync_thread.daemon = True  # Set the thread as daemon (background) thread
        self.sync_thread.start()  # Start the synchronization thread

    def perform_failover(self):
        while True:  # Run indefinitely
            # Simulate failover process
            failover_time = random.uniform(0.5, 5)  # Generate a random failover time between 0.5 and 5 seconds
            self.failover_times.append(failover_time)  # Add the failover time to the list
            time.sleep(failover_time)  # Sleep for the duration of the failover time

    def perform_sync(self):
        while True:  # Run indefinitely
            # Simulate data consistency update
            data_consistency = random.uniform(90, 100)  # Generate a random data consistency value between 90 and 100
            self.data_consistencies.append(data_consistency)  # Add the data consistency value to the list
            time.sleep(10)  # Sleep for 10 seconds (sync interval)

    def get_failover_time_stats(self):
        if self.failover_times:  # Check if failover times list is not empty
            best_failover_time = min(self.failover_times)  # Find the minimum failover time
            average_failover_time = sum(self.failover_times) / len(self.failover_times)  # Calculate the average failover time
            worst_failover_time = max(self.failover_times)  # Find the maximum failover time
            return best_failover_time, average_failover_time, worst_failover_time  # Return statistics
        else:
            return None, None, None  # Return None if no data is available

    def get_data_consistency_stats(self):
        if self.data_consistencies:  # Check if data consistencies list is not empty
            best_data_consistency = max(self.data_consistencies)  # Find the maximum data consistency value
            average_data_consistency = sum(self.data_consistencies) / len(self.data_consistencies)  # Calculate the average data consistency
            worst_data_consistency = min(self.data_consistencies)  # Find the minimum data consistency value
            return best_data_consistency, average_data_consistency, worst_data_consistency  # Return statistics
        else:
            return None, None, None  # Return None if no data is available

def main():
    # Seed the random number generator for consistency
    random.seed(42)

    backup_controller = PrimaryBackupController()  # Create an instance of PrimaryBackupController
    primary = PrimaryBackupController()  # Create another instance of PrimaryBackupController

    try:
        while True:  # Run indefinitely
            time.sleep(5)  # Sleep for 5 seconds

            # Calculate best, average, and worst case scenarios for failover time
            best_ft, avg_ft, worst_ft = backup_controller.get_failover_time_stats()  # Get failover time statistics
            print("Failover Time:")
            print(f"Best Case: {best_ft} seconds" if best_ft is not None else "No data available")
            print(f"Average Case: {avg_ft} seconds" if avg_ft is not None else "No data available")
            print(f"Worst Case: {worst_ft} seconds" if worst_ft is not None else "No data available")

            # Calculate best, average, and worst case scenarios for data consistency
            best_dc, avg_dc, worst_dc = backup_controller.get_data_consistency_stats()  # Get data consistency statistics
            print("\nData Consistency:")
            print(f"Best Case: {best_dc:.2f}%" if best_dc is not None else "No data available")
            print(f"Average Case: {avg_dc:.2f}%" if avg_dc is not None else "No data available")
            print(f"Worst Case: {worst_dc:.2f}%" if worst_dc is not None else "No data available")

    except KeyboardInterrupt:  # Handle keyboard interrupt
        pass

if __name__ == '__main__':
    main()
