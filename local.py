import copy
import random
import constraints

# constraints_dict is dict where keys are constraint function names
# and values are (boolean, int) tuples representing (enabled, cost)

def evaluation_func(assignment, domain, constraints_dict):
    total_cost = 0
    for key in constraints_dict.keys():
        enabled, cost = constraints_dict[key]
        if enabled:
            total_cost += getattr(constraints, key)(assignment, domain, cost)
    return total_cost
    
def init_assignment(domain):
    workers, tasks = domain
    assignment = {}
    flipped_asst = {}
    for task in tasks:
        n = 1 + int(random.random() * (len(workers) - 1))
        assignment[task] = random.sample(workers, n)
    for w in workers.values():
        flipped_asst[w.name] = []
    for k in assignment.keys():
        for worker in assignment[k]:
            flipped_asst[worker].append(k)
    return flipped_asst

def find_best_neighbor(assignment, domain, constraints_dict, best_cost):
    workers, tasks = domain
    best_assignment = copy.deepcopy(assignment)
    for worker in assignment.keys():
        for task in tasks.values():
            new_assignment = copy.deepcopy(assignment)
            if task.name in assignment[worker]:
                new_assignment[worker].remove(task.name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
            else:
                new_assignment[worker].append(task.name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
            #print "Cost:", cost
            #print "Best Cost:", best_cost
            if cost < best_cost:
                best_cost = cost
                best_assignment = new_assignment
                print "New assignment with cost", best_cost
                print best_assignment
    return (best_assignment, best_cost)

# hill climbing
def hill_climbing(domain, constraints_dict):
    assignment = init_assignment(domain)
    best_cost = float("inf")
    best_neighbor, neighbor_cost = find_best_neighbor(assignment, domain, constraints_dict, best_cost)
    while(neighbor_cost < best_cost):
        assignment = best_neighbor
        best_cost = neighbor_cost
        best_neighbor, neighbor_cost = find_best_neighbor(assignment, domain, constraints_dict, best_cost)
    return best_neighbor