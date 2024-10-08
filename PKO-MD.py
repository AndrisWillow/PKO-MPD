import json
import sys
import random
import copy
import time

class Truck:
    def __init__(self, truck_id, capacity=80): 
        self.truck_id = truck_id
        self.capacity = capacity  # Solves this requirement: Katra mašīna var pāvadāt 80 kravas vienības;
        self.cargo = capacity     # Current cargo
        self.route = []           # List of location indices (starts and ends at depot)
        self.total_time = 9*60    # Total time a truck has based on work hours # TODO delete or drag with?
        self.total_time_delivering = 0       # Total time spent on the route #TODO delete

    def reset_cargo(self):
        self.cargo = self.capacity # when a truck returns to depot it can load back up to 80 capacity

    def deliver(self, demand, customer_index):
        if self.cargo >= demand:
            # Deliver to customer
            self.route.append(customer_index)
        else:
            # Not enough cargo, return to depot
            self.route.append(0)
            self.reset_cargo()

            # Go to customer
            self.route.append(customer_index)

        self.cargo -= demand

# Read json and reurn distance_matrix and demand
def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    distance_matrix = data["distance_matrix"]
    demands = data["demands"]
    return distance_matrix, demands

def gen_inital_solution(demands, num_trucks):
    trucks = [Truck(truck_id=i) for i in range(num_trucks)]
    solution = {}
    all_locations_to_visit = list(range(1, len(demands))) # List of customer indices (excluding depot at index 0)
    # By adding each site we are addressing this constraint -	Katrs klients ir jāapkalpo;
    
    # Split the customers into batches for each truck, so we start with an even distribution for each car as per soft requirement -> Jānodrošina, lai katra mašīna pēc iespējas ir vienlīdz nodarbināta. 
    batches = [[] for _ in range(num_trucks)]
    for idx, location in enumerate(all_locations_to_visit):
        batches[idx % num_trucks].append(location)

    # For each truck, create its route
    for i, truck in enumerate(trucks):
        truck.route.append(0)  # Start at depot
        for customer_index in batches[i]:
            demand = demands[customer_index]
            truck.deliver(demand, customer_index)

        truck.route.append(0)  # Return to depot at the end
        solution[truck.truck_id] = truck.route

    return solution

# Function that evaluates solutions and outputs the cost of it
def get_cost(solution, distance_matrix):
    cost = 0
    total_time_per_truck = 9*60
    truck_times = []

    # 1st lets address this constraint. 	Ir noteikts piegāžu darba laiks no 8:00-17:00. 17:00 visām mašīnām ir jāatgriežas uzņēmuma depo
    for truck_id, route in solution.items():
        total_time_delivering = 0
        for i in range(len(route) - 1):
            from_loc = route[i]
            to_loc = route[i + 1]
            travel_time = distance_matrix[from_loc][to_loc]
            total_time_delivering += travel_time

        # if it violates the work time, large penelty
        if total_time_delivering > total_time_per_truck:
            cost += 1e6
    
        # 2nd constraint # Jāsamazina laiks, cik katra mašīna pavada braucot;
        cost += total_time_delivering

        truck_times.append(total_time_delivering)
        # print(f"Truck {truck_id}: {total_time_delivering} minutes") # TODO add this to end results?

    # 3rd constaint #Jānodrošina, lai katra mašīna pēc iespējas ir vienlīdz nodarbināta.
    avg_time = sum(truck_times) / len(truck_times)
    workload_variance = sum(abs(time - avg_time) for time in truck_times)
    cost += workload_variance

    return cost

# Utility function that will adjust a solution once mutated to enforce that when a customer is visited with enough cargo & when needed go to depo to get more
def adjust_routes(solution, demands):
    adjusted_solution = {}

    for truck_id, route in solution.items():
        adjusted_route = []  
        cargo = Truck(truck_id).capacity
        # We remove all previous routes to go to depo and recalculate them for simplicity, when the mutation happens some depo visits might be too early or too late
        route = [0] + [loc for loc in route if loc != 0] + [0]

        # Iterate through the route to handle deliveries
        for loc in route:
            demand = demands[loc]
            if cargo < demand:
                # Return to depot to refill cargo if necessary
                adjusted_route.extend([0, loc])
                cargo = Truck(truck_id).capacity - demand
            else:
                adjusted_route.append(loc)
                cargo -= demand

        adjusted_solution[truck_id] = adjusted_route

    return adjusted_solution

# Function that as it's input takes an existing solution and modifies it randomly 
def mutate_solution(solution, demands, changes=1):
    new_solution = copy.deepcopy(solution)
    for _ in range(changes):
        change_type = random.choice([1, 2])

        # 1st option swpas in 1 truck swpas 2 destinations
        if change_type == 1:
            truck_id = random.choice(list(new_solution.keys()))
            route = new_solution[truck_id]
            # Get indices of customer visits (exclude depots)
            customer_indices = [i for i, loc in enumerate(route) if loc != 0]
            if len(customer_indices) >= 2:
                idx1, idx2 = random.sample(customer_indices, 2)
                # Swap the customer locations
                route[idx1], route[idx2] = route[idx2], route[idx1]
                new_solution[truck_id] = route
        
        # 2nd option swaps 2 destinations in 2 trucks
        if change_type == 2:

            # Get 2 random trucks
            truck_ids = random.sample(list(new_solution.keys()), 2)
            route1 = new_solution[truck_ids[0]]
            route2 = new_solution[truck_ids[1]]
            
            # Get customer indices (exclude depots)
            customer_indices1 = [i for i, loc in enumerate(route1) if loc != 0]
            customer_indices2 = [i for i, loc in enumerate(route2) if loc != 0]

            if customer_indices1 and customer_indices2:
                idx1 = random.choice(customer_indices1)
                idx2 = random.choice(customer_indices2)
                # Swap the customer locations
                route1[idx1], route2[idx2] = route2[idx2], route1[idx1]
                new_solution[truck_ids[0]] = route1
                new_solution[truck_ids[1]] = route2

    # Re-evaluate the routes to ensure capacity constraints and depot visits
    new_solution = adjust_routes(new_solution, demands)

    return new_solution

# We use a primitive genetic algorithm, that takes the last best solution and mutates it slightly
# Then next solution is picked based on the best performance by fitness metric, which in this case is the cost function
def get_best_solution_using_gen_alg(solution, cost, demands, distance_matrix, population = 4):
    best_solution = solution
    best_solution_cost = cost
    mutated_solution = {}
    for _ in range(population):
        mutated_solution = mutate_solution(solution, demands)
        new_cost = get_cost(mutated_solution, distance_matrix)
        # print(best_solution_cost)
        if new_cost < best_solution_cost: 
             best_solution_cost = new_cost
             best_solution = mutated_solution
    return best_solution, best_solution_cost

def main():

    # Let user define input json
    if len(sys.argv) > 1:
        json_filename = sys.argv[1]
    else: 
        json_filename = 'test-data.json'
    # Let user define num of trucks
    if len(sys.argv) > 2:
        num_trucks = int(sys.argv[2])
    else:
        num_trucks = 3
    # Let user define how many steps will the genetic algorithm try to make to get output
    if len(sys.argv) > 3:
        steps = int(sys.argv[3])
    else:
        steps = 50

    start_time = time.time()
    distance_matrix, demands = read_json(json_filename)
    inital_solution = gen_inital_solution(demands, num_trucks)
    initial_cost = get_cost(inital_solution, distance_matrix)
    solution = inital_solution
    cost = initial_cost

    # Running genetic algorithm
    for _ in range(steps):
        solution, cost  = get_best_solution_using_gen_alg(solution, cost, demands, distance_matrix)


    print(f"Inital cost {initial_cost}. Initial solution:")
    print(inital_solution)
    print(f"Final cost {cost}. Final solution:")
    print(solution)

    elapsed_time = time.time() - start_time
    print(f"Program executed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
