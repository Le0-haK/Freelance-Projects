import itertools  # Import itertools module to work with iterators and combinations
import random  # Import random module to generate random numbers
import time  # Import time module to measure execution time

def distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5  # Calculate Euclidean distance using the formula

def total_latency(controllers, switches):
    """Calculate the total latency for a given controller placement."""
    total = 0
    for switch in switches:
        closest_controller_dist = min(distance(switch, controller) for controller in controllers)  # Find the closest controller to each switch
        total += closest_controller_dist  # Add the distance to the total latency
    return total  # Return the total latency

def optimal_controller_placement(switches, num_controllers):
    """Find the optimal placement of controllers to minimize latency."""
    # Generate all possible combinations of controller placements
    controller_placements = list(itertools.combinations(switches, num_controllers))  # Generate all combinations of switches and controllers
    
    # Initialize variables to keep track of the best placement and its latency
    best_placement = None
    best_latency = float('inf')  # Set initial best latency to infinity (maximum value)
    
    # Record start time
    start_time = time.time()  # Record the current time
    
    # Iterate through all possible placements and find the one with the minimum latency
    for placement in controller_placements:
        current_latency = total_latency(placement, switches)  # Calculate latency for the current placement
        if current_latency < best_latency:  # If the current latency is better than the best latency found so far
            best_placement = placement  # Update the best placement
            best_latency = current_latency  # Update the best latency
            
    # Calculate convergence time
    convergence_time = time.time() - start_time  # Calculate the time taken for convergence
        
    return best_placement, best_latency, convergence_time  # Return the best placement, best latency, and convergence time

if __name__ == "__main__":
    # Define parameters range
    min_switches = 10
    max_switches = 30
    min_controllers = 2
    max_controllers = 3
    
    # Initial latency of the network without controller placement optimization
    initial_latency = 500  # Example initial latency in milliseconds
    
    scenarios = ["Best Case", "Average Case", "Worst Case"]  # Define different scenarios to evaluate
    
    for scenario in scenarios:  # Iterate over each scenario
        print(f"Calculating {scenario} Scenario...")  # Print the current scenario being evaluated
        
        best_result = None  # Initialize variable to store the best result
        best_latency = float('inf') if scenario != "Worst Case" else -1  # Initialize best latency
        
        # Iterate through all combinations of switches and controllers
        for num_switches in range(min_switches, max_switches + 1):  # Loop through the range of switch counts
            for num_controllers in range(min_controllers, min(num_switches, max_controllers) + 1):  # Loop through the range of controller counts
                switches = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_switches)]  # Generate random switch locations
                best_placement, latency, convergence_time = optimal_controller_placement(switches, num_controllers)  # Find optimal controller placement for the current configuration
                latency_reduction = initial_latency - latency  # Calculate latency reduction
                
                # Check if this configuration yields the best/worst result so far
                if scenario == "Best Case" and latency < best_latency:  # If this is the best case scenario and the latency is better
                    best_latency = latency  # Update the best latency
                    best_result = {
                        "num_switches": num_switches,  # Store the number of switches
                        "num_controllers": num_controllers,  # Store the number of controllers
                        "latency": latency,  # Store the latency
                        "convergence_time": convergence_time,  # Store the convergence time
                        "latency_reduction": latency_reduction  # Store the latency reduction
                    }
                elif scenario == "Average Case" and abs(latency_reduction - 250) <= 50:  # If this is the average case scenario and latency reduction is within 50 ms of 250 ms
                    best_latency = latency  # Update the best latency
                    best_result = {
                        "num_switches": num_switches,  # Store the number of switches
                        "num_controllers": num_controllers,  # Store the number of controllers
                        "latency": latency,  # Store the latency
                        "convergence_time": convergence_time,  # Store the convergence time
                        "latency_reduction": latency_reduction  # Store the latency reduction
                    }
                elif scenario == "Worst Case" and latency > best_latency:  # If this is the worst case scenario and the latency is worse
                    best_latency = latency  # Update the best latency
                    best_result = {
                        "num_switches": num_switches,  # Store the number of switches
                        "num_controllers": num_controllers,  # Store the number of controllers
                        "latency": latency,  # Store the latency
                        "convergence_time": convergence_time,  # Store the convergence time
                        "latency_reduction": latency_reduction  # Store the latency reduction
                    }
        
        # Output the best result for the current scenario
        print(f"Best Result for {scenario}:")
        if best_result is not None:  # If a valid result was found
            print("Number of Switches:", best_result["num_switches"])  # Print the number of switches
            print("Number of Controllers:", best_result["num_controllers"])  # Print the number of controllers
            print("Latency:", best_result["latency"], "milliseconds")  # Print the latency
            print("Convergence Time:", best_result["convergence_time"], "seconds")  # Print the convergence time
            print("Latency Reduction:", best_result["latency_reduction"], "milliseconds")  # Print the latency reduction
        else:
            print("No valid result found for this scenario.")  # Print a message indicating no valid result was found
        print()  # Print an empty line for better readability
