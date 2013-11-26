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
        n = random.random(1, len(workers))
        assignment[task] = random.sample(workers, n)
    for w in workers:
        flipped_asst[w.name] = []
    for k in assignment.keys():
        for worker in assignment[k]:
            flipped_asst[worker].append(k)
    return flipped_asst

# hill_climbing
def hill_climbing(domain, constraints_dict):
    workers, tasks = domain
    assignment = init_assignment(domain)
    best_assignment = assignment
    best_cost = float("inf")
    for worker in assignment.keys():
        for task in tasks:
            new_assignment = copy.deepcopy(assignment)
            if task.name in assignment[worker]:
                new_assignment[worker].remove(task.name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
            else:
                new_assignment[worker].append(task.name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
            if cost < best_cost:
                best_cost = cost
                best_assignment = new_assignment
    