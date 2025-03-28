import traci
import pandas as pd
import numpy as np

# Initialise the simulation
sumo_binary = "sumo"  # Or "sumo-gui" for the GUI version
sumo_config_file = "your_network.sumocfg"  # Path to your SUMO config file

# Start the SUMO simulation
traci.start([sumo_binary, "-c", sumo_config_file])

# Prepare a list to store data
data = []

# Run the simulation for a specific time period (e.g., 3600 seconds)
for step in range(3600):  # Simulation time
    traci.simulationStep()  # Advance simulation by one step

    # Collect vehicle counts at intersections (assuming 'intersection_1' is your intersection)
    vehicle_count = traci.edge.getLastStepVehicleNumber("intersection_1")  # Replace with your intersection's edge ID

    # Save data (time, vehicle count)
    data.append([step, vehicle_count])

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(data, columns=["Time", "Vehicle Count"])

# Save the data to a CSV file
df.to_csv("traffic_data.csv", index=False)

# Close the simulation
traci.close()
