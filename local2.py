import copy
import random
import constraints
from operator import itemgetter
from math import log, e
import numpy as np

# Find cost of assignment.
def evaluation_func(assignment, domain, constraints_dict):
    total_cost = 0
    for name, cost in constraints_dict.iteritems():
        if cost:
            constraint_func = getattr(constraints, name)
            total_cost += constraint_func(assignment, domain, cost)
    return total_cost

# Initialize a new assignment by assigning the wanted number of workers to each task.
def init_assignment(domain):
    workers, tasks = domain
    assignment = {}
    flipped_asst = {}
    for name, task in tasks.iteritems():
        wanted = int(task.wanted_workers)
        if wanted > len(workers):
            assignment[task.name] = workers
        else:
            assignment[task.name] = random.sample(workers, wanted)
    for worker in workers:
        flipped_asst[worker] = []
    for task in assignment:
        for worker in assignment[task]:
            flipped_asst[worker].append(task)
    return flipped_asst

# Neighbors of the current assignment are generated in one of two ways:
# either remove one of a worker's assigned tasks or assign the worker a new task

# Returns a list of the (assignment, cost) of all neighbors
def find_all_neighbors(assignment, domain, constraints_dict):
    workers, tasks = domain
    neighbors = []
    for worker in assignment:
        for name, task in tasks.iteritems():
            new_assignment = copy.deepcopy(assignment)
            if name in assignment[worker]:
                new_assignment[worker].remove(name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
            else:
                new_assignment[worker].append(name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
            neighbors.append((new_assignment, cost))
    return neighbors

# Return the (assignment, cost) of the neighbor with the lowest cost.
def find_best_neighbor(assignment, domain, constraints_dict, best_cost):
    nodes = 0
    workers, tasks = domain
    best_assignment = copy.deepcopy(assignment)
    for worker in assignment:
        for name, task in tasks.iteritems():
            new_assignment = copy.deepcopy(assignment)
            if name in assignment[worker]:
                new_assignment[worker].remove(name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
                nodes+=1
            else:
                new_assignment[worker].append(name)
                cost = evaluation_func(new_assignment, domain, constraints_dict)
                nodes+=1
            if cost < best_cost:
                (best_assignment, best_cost) = new_assignment, cost
    return (best_assignment, best_cost, nodes)
    
# Returns the (assignment, cost) of a random neighbor
def find_random_neighbor(assignment, domain, constraints_dict):
    workers, tasks = domain
    new_assignment = copy.deepcopy(assignment)
    worker = random.choice(workers.values())
    task = random.choice(tasks.values())
    if task.name in assignment[worker.name]:
        new_assignment[worker.name].remove(task.name)
    else:
        new_assignment[worker.name].append(task.name)
    cost = evaluation_func(new_assignment, domain, constraints_dict)
    return (new_assignment, cost)

# Returns True if no neighbor has a lower cost
def is_local_mimimum(assignment, domain, constraints_dict):
    current_cost = evaluation_func(assignment, domain, constraints_dict)
    successors = find_all_neighbors(assignment, domain, constraints_dict)
    for s in successors:
        if s[1] < current_cost:
            return False
    return True

# LOCAL SEARCHES!!

def hill_climbing(domain, constraints_dict):
    line_data = []
    nodes = 0
    assignment = init_assignment(domain)
    best_cost = evaluation_func(assignment, domain, constraints_dict)
    best_neighbor, neighbor_cost, n = find_best_neighbor(assignment, domain, constraints_dict, best_cost)
    nodes+=n
    k = 0
    while neighbor_cost < best_cost:
        assignment = best_neighbor
        best_cost = neighbor_cost
        best_neighbor, neighbor_cost, n = find_best_neighbor(assignment, domain, constraints_dict, best_cost)
        for i in range(n):
            line_data.append(best_cost)
        nodes+=n
        k += 1
    return (best_neighbor, nodes, line_data)

# Random restart hill climbing
def rr_hill_climbing(domain, constraints_dict):
    line_data = []
    nodes = 1
    # SET MAX ITERATIONS HERE
    MAX_ITERS = 5
    best_result = (None, float("inf"))
    k = 0
    for i in xrange(MAX_ITERS):
        assignment = init_assignment(domain)
        best_cost = float("inf")
        best_neighbor, neighbor_cost, n = find_best_neighbor(assignment, domain, constraints_dict, best_cost)
        nodes+=n
        while neighbor_cost < best_cost :
            assignment = best_neighbor
            best_cost = neighbor_cost
            best_neighbor, neighbor_cost, n = find_best_neighbor(assignment, domain, constraints_dict, best_cost)
            if i == 0:
                for count in range(n):
                    line_data.append(best_cost)
            nodes+=n
            k += 1
        if neighbor_cost < best_result[1]:
            best_result = (best_neighbor, neighbor_cost)
    return (best_result[0], nodes, line_data)

# Stochastic hill climbing
def stoc_hill_climbing(domain, constraints_dict):
    line_data= []
    nodes = 1
    assignment = init_assignment(domain)
    curr_cost = evaluation_func(assignment, domain, constraints_dict)
    k = 0
    while True:
        neighbors = find_all_neighbors(assignment, domain, constraints_dict)
        nodes += len(neighbors)
        for i in range(len(neighbors)):
            line_data.append(curr_cost)
        diffs = map(lambda x: curr_cost - x[1], neighbors)
        diffs = map(lambda x: 0 if x < 0 else x, diffs)
        diff_sum = float(sum(diffs))
        if diff_sum == 0.0: # local maximum
            return (assignment, nodes, line_data)
        else:
            probs = map(lambda x: x / diff_sum, diffs)
            idx = list(np.random.multinomial(1, probs, 1)[0]).index(1)
            assignment = neighbors[idx][0]
            curr_cost = neighbors[idx][1]
        k += 1

# GLOBALS
TEMP_FUNCTION = 0 # 0 for exp, 1 for fast, 2 for boltz
INIT_TEMP = 1000
MIN_TEMP = 1

def temperature(k):
    if TEMP_FUNCTION == 0: # exponential
        return INIT_TEMP * 0.9995**k
    elif TEMP_FUNCTION == 1: # fast
        return INIT_TEMP / (k+1)
    elif TEMP_FUNCTION == 2: # boltz
        return INIT_TEMP / log(k+2)
    else:
        raise("Invalid TEMP_FUNCTION")

def p_move(new_cost, cost, temp):
    return e**((new_cost-cost)/temp)

def simulated_annealing(domain, constraints_dict):
    line_data = []
    nodes = 1
    assignment = init_assignment(domain)
    cost = evaluation_func(assignment, domain, constraints_dict)
    best_assignment, lowest_cost = assignment, cost
    k = 0
    while True:
        temp = temperature(k)
        if temp < MIN_TEMP:
            return (best_assignment, nodes, line_data)
        rand_neighbor, new_cost = find_random_neighbor(assignment, domain, constraints_dict)
        nodes += 1
        if new_cost < cost or p_move(new_cost, cost, temp) < random.random():
            assignment = rand_neighbor
            cost = new_cost
            if cost < lowest_cost:
                best_assignment = assignment
                lowest_cost = cost
        line_data.append(lowest_cost)
        k += 1

# Similar to simulated annealing, but never moves to a worse point.
def rand_stoc_hill_climbing(domain, constraints_dict):
    line_data = []
    nodes = 1
    assignment = init_assignment(domain)
    cost = evaluation_func(assignment, domain, constraints_dict)
    best_assignment, lowest_cost = assignment, cost
    # SET MAX ITERATIONS HERE
    max_iters = 50000
    for k in xrange(max_iters):
        rand_neighbor, new_cost = find_random_neighbor(assignment, domain, constraints_dict)
        nodes+=1
        if new_cost < cost and e**(new_cost-cost) < random.random():
            assignment = rand_neighbor
            cost = new_cost
            if cost < lowest_cost:
                best_assignment = assignment 
                lowest_cost = cost
        line_data.append(lowest_cost)
    return (best_assignment, nodes, line_data)

def beam_search(domain, constraints_dict, k=3):
    line_data = []
    nodes = k
    initial_assignments = [init_assignment(domain) for i in range(k)]
    current_k = []
    for a in initial_assignments:
        cost = evaluation_func(a, domain, constraints_dict)
        current_k.append((a, cost))
    max_iters = 30000
    for i in xrange(max_iters):
        successors = []
        for asst in current_k:
            neighbors = find_all_neighbors(asst[0], domain, constraints_dict)
            nodes += len(neighbors)
            for neighbor in neighbors:
                successors.append(neighbor)
        current_k += successors
        current_k = sorted(current_k, key=itemgetter(1))
        for i in range(len(current_k)):
            line_data.append(current_k[0][1])
        current_k = current_k[:k]
        best = current_k[0]
        if is_local_mimimum(best[0], domain, constraints_dict):
            return (best[0], nodes, line_data)
