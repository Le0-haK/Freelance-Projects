import itertools  # Import itertools module for generating combinations
import random  # Import random module for generating random numbers
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import matplotlib.patches as patches  # Import patches module from matplotlib for drawing shapes

def distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5  # Calculate the Euclidean distance between two points using the distance formula

def total_latency(controllers, switches):
    """Calculate the total latency for a given controller placement."""
    total = 0  # Initialize total latency to 0
    for switch in switches:  # Loop through each switch
        # Calculate the distance between the current switch and its closest controller
        closest_controller_dist = min(distance(switch, controller) for controller in controllers)
        total += closest_controller_dist  # Add the distance to the total latency
    return total  # Return the total latency

def optimal_controller_placement(switches, num_controllers):
    """Find the optimal placement of controllers to minimize latency."""
    # Generate all possible combinations of controller placements
    controller_placements = list(itertools.combinations(switches, num_controllers))
    
    # Initialize variables to keep track of the best placement and its latency
    best_placement = None
    best_latency = float('inf')  # Initialize best latency to positive infinity
    
    # Iterate through all possible placements and find the one with the minimum latency
    for placement in controller_placements:  # Loop through each possible placement
        current_latency = total_latency(placement, switches)  # Calculate the total latency for the current placement
        if current_latency < best_latency:  # Check if the current latency is better than the best latency found so far
            best_placement = placement  # Update the best placement
            best_latency = current_latency  # Update the best latency
            
        # Visualize current placement and latency
        visualize_placement(switches, placement, current_latency)  # Call function to visualize the current placement
        
    return best_placement, best_latency  # Return the best placement and its latency

def visualize_placement(switches, controllers, latency):
    """Visualize current controller placement."""
    plt.figure(figsize=(8, 8))  # Create a new figure with size 8x8 inches
    plt.scatter(*zip(*switches), color='blue', label='Switches')  # Plot switches
    for controller in controllers:  # Loop through each controller
        plt.scatter(controller[0], controller[1], color='red', label='Controller')  # Plot controllers
        # Plot a circle around the controller to represent its coverage area
        circle = patches.Circle((controller[0], controller[1]), radius=20, edgecolor='red', fill=False)
        plt.gca().add_patch(circle)  # Add the circle to the plot
    plt.xlim(0, 100)  # Set x-axis limit from 0 to 100
    plt.ylim(0, 100)  # Set y-axis limit from 0 to 100
    plt.xlabel('X')  # Set x-axis label
    plt.ylabel('Y')  # Set y-axis label
    plt.title(f'Current Controller Placement (Total Latency: {latency})')  # Set title with current latency
    plt.legend()  # Show legend
    plt.grid(True)  # Show grid
    plt.show()  # Show the plot

if __name__ == "__main__":
    # Define parameters
    network_size = (100, 100)  # Size of the network area (e.g., 100x100 units)
    num_switches = 20  # Number of switches in the network
    num_controllers = 3  # Number of controllers to place

    # Step 1: Generate random switch locations
    switches = [(random.uniform(0, network_size[0]), random.uniform(0, network_size[1])) for _ in range(num_switches)]

    # Step 2 & 3: Find and visualize optimal controller placement
    best_placement, best_latency = optimal_controller_placement(switches, num_controllers)

    # Step 4: Final visualization
    plt.figure(figsize=(8, 8))  # Create a new figure with size 8x8 inches
    plt.scatter(*zip(*switches), color='blue', label='Switches')  # Plot switches
    for controller in best_placement:  # Loop through each controller in the best placement
        plt.scatter(controller[0], controller[1], color='red', label='Controller')  # Plot controllers
        # Plot a circle around the controller to represent its coverage area
        circle = patches.Circle((controller[0], controller[1]), radius=20, edgecolor='red', fill=False)
        plt.gca().add_patch(circle)  # Add the circle to the plot
    plt.xlim(0, network_size[0])  # Set x-axis limit based on network size
    plt.ylim(0, network_size[1])  # Set y-axis limit based on network size
    plt.xlabel('X')  # Set x-axis label
    plt.ylabel('Y')  # Set y-axis label
    plt.title(f'Final Controller Placement (Minimum Latency: {best_latency})')  # Set title with best latency
    plt.legend()  # Show legend
    plt.grid(True)  # Show grid
    plt.show()  # Show the plot
