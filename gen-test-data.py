import json
import random
import sys

# Function that generates the distance matrix (nxn) where n is the amount that there are customers + company depot
def generate_distance_matrix(num_customers, min_distance=5, max_distance=60):
    num_locations = num_customers + 1  # Including the depot
    distance_matrix = []

    for i in range(num_locations):
        row = []
        for j in range(num_locations):
            if i == j:
                distance = 0  # same location, so 0
            else:
                distance = random.randint(min_distance, max_distance)
            row.append(distance)
        distance_matrix.append(row)
    
    return distance_matrix

# Function to generate demands for customers
# solves requirement: #	Katrs klients var pieprasīt no 5-20 kravas vienībām;
def generate_demands(num_customers, min_demand=5, max_demand=20):
    demands = [0]  # Depot is first value and it has no demand
    for _ in range(num_customers):
        demand = random.randint(min_demand, max_demand)
        demands.append(demand)
    return demands

# Generating distance matrix + costomer demands, combining both in 1 json file, 0-th element is company depot
def main():
    if len(sys.argv) > 1:
        json_filename = sys.argv[1]
    else: 
        json_filename = 'test-data.json'

    if len(sys.argv) > 2:
        num_customers = int(sys.argv[2])
    else: 
        num_customers = int(input("Enter the number of customer locations: "))
    
    distance_matrix = generate_distance_matrix(num_customers)
    demands = generate_demands(num_customers)

    data = {
        'distance_matrix': distance_matrix,
        'demands': demands
    }

    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    main()
