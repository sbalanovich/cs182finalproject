def skill_constraint(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in assignment.keys():
        for task in assignment[worker]:
            for skill in tasks[task].skill_reqs:
                if skill not in workers[worker].skills:
                    total_cost += cost
    return total_cost

def too_many_workers(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for task in tasks.values():
        wanted = int(task.num_workers)
        assigned = 0
        for worker in workers.keys():
            for task2 in assignment[worker]:
                if task.name == task2:
                    assigned += 1
        if assigned > wanted:
            weight = float((assigned + 1)) / (wanted + 1)
            total_cost += (assigned - wanted) * cost * weight
    return total_cost

def too_few_workers(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for task in tasks.values():
        wanted = int(task.num_workers)
        assigned = 0
        for worker in workers.keys():
            for task2 in assignment[worker]:
                if task.name == task2:
                    assigned += 1
        if assigned < wanted:
            weight = float((wanted + 1)) / (assigned + 1)
            total_cost += (wanted - assigned) * cost * weight
    return total_cost

def too_many_tasks(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in workers.values():
        wanted = int(worker.num_tasks)
        assigned = len(assignment[worker.name])
        if assigned > wanted:
            weight = float((assigned + 1)) / (wanted + 1)
            total_cost += (assigned - wanted) * cost * weight
    return total_cost

def too_few_tasks(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in workers.values():
        wanted = int(worker.num_tasks)
        assigned = len(assignment[worker.name])
        if assigned < wanted:
            weight = float((wanted + 1)) / (assigned + 1)
            total_cost += (wanted - assigned) * cost * weight
    return total_cost

def print_cost_summary(assignment, domain, constraints_dict):
    print "SKILL", skill_constraint(assignment, domain, constraints_dict['skill_constraint'][1])
    print "TOO MANY WORKERS", too_many_workers(assignment, domain, constraints_dict['too_many_workers'][1])
    print "TOO FEW WORKERS", too_few_workers(assignment, domain, constraints_dict['too_few_workers'][1])
    print "TOO MANY TASKS", too_many_tasks(assignment, domain, constraints_dict['too_many_tasks'][1])
    print "TOO FEW TASKS", too_few_tasks(assignment, domain, constraints_dict['too_few_tasks'][1])

def all_assigned_constraint(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    assigned_tasks = [assigned_task for worker_tasks in assignment.values() for assigned_task in worker_tasks]
    for task in tasks.keys():
        if task not in assigned_tasks:
            total_cost += cost
    return total_cost
    
def assigned_once_constraint(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    assigned_tasks = [assigned_task for worker_tasks in assignment.values() for assigned_task in worker_tasks]
    for task in tasks.keys():
        if assigned_tasks.count(task) > 1:
            total_cost += cost
    return total_cost


def efficiency_constraint(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in assignment.keys():
        numeffs = len(workers[worker].effs)
        for task in workers[worker].effs.keys():
            inv_eff = numeffs-workers[worker].effs[task]
            totalcost += cost*inv_eff
    return total_cost

def preference_constraint(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in assignment.keys():
        numprefs = len(workers[worker].prefs)
        for task in workers[worker].prefs.keys():
            inv_pref = numprefs-workers[worker].prefs[task]
            totalcost += cost*inv_pref
    return total_cost

def time_constraint(assignment, domain, cost):
    raise("Not Defined")

def labor_cost_constraint(assignment, domain, cost):
    raise("Not Defined")

