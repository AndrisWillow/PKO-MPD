import json
import sys

class Truck:
    def __init__(self, truck_id, capacity=80): 
        self.truck_id = truck_id
        self.capacity = capacity  # Solves this requirement: Katra mašīna var pāvadāt 80 kravas vienības;
        self.cargo = capacity     # Current cargo
        self.route = []           # List of location indices (starts and ends at depot)
        self.total_time = 9*60    # Total time a truck has based on work hours
        self.total_time_delivering = 0       # Total time spent on the route

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

    distance_matrix, demands = read_json(json_filename)

    inital_solution = gen_inital_solution(demands, num_trucks)
    print (inital_solution)

if __name__ == "__main__":
    main()



# # Function that evaluates solutions and outputs the cost of it
# def get_cost(solution):
#     cost = 0

# ### Define the cost function
# # take as input json file data

#     return cost

#     # # solution = optim_genetic_alg(distance_matrix, demands, num_trucks) # intial solution, make it random
#     # for step in steps-1:
#     #     solution = optim_genetic_alg(distance_matrix, demands, num_trucks) # using genetic algorithm modify the solution
#     #     cost = get_cost(solution) # evaluate the solution
#     #     print(cost)

#     # print(solution, cost)

# # Function that as it's input takes an existing solution and modifies it slightly (changes some destinations between trucks, delete depot visit if capacity still allows for more visits)
# def mutate_solution(solution):
#     return 0

# def optim_genetic_alg(solution, population = 4):
#     best_solution = {}
#     best_solution_cost = 1000
#     solution = {0: [0, 1, 3, 2, 0, 15, 0]}
#     for _ in population:
#         # solution = mutate_solution(solution),
#         # cost = get_cost(solution)
#         # if best_solution_cost > cost: 
#             #  best_solution_cost = cost
#             #  best_solution = solution

# # solution object contains a list of all the trucks and their route, something like:
# # {0: [0, 1, 3, 2, 0, 15... 0], 1: [0, 2, 4... 0], ...} - Trucks always start and end at 0th location - company depot
#     return solution

# # Define soft constraints

# # 	Jāsamazina laiks, cik katra mašīna pavada braucot;
# #	Jānodrošina, lai katra mašīna pēc iespējas ir vienlīdz nodarbināta.
# #	Ir noteikts piegāžu darba laiks no 8:00-17:00. 17:00 visām mašīnām ir jāatgriežas uzņēmuma depo.