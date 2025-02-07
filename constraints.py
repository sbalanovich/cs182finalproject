def lack_required_skill(assignment, domain, cost):
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
        wanted = int(task.wanted_workers)
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
        wanted = int(task.wanted_workers)
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
        wanted = int(worker.wanted_tasks)
        assigned = len(assignment[worker.name])
        if assigned > wanted:
            weight = float((assigned + 1)) / (wanted + 1)
            total_cost += (assigned - wanted) * cost * weight
    return total_cost

def too_few_tasks(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in workers.values():
        wanted = int(worker.wanted_tasks)
        assigned = len(assignment[worker.name])
        if assigned < wanted:
            weight = float((wanted + 1)) / (assigned + 1)
            total_cost += (wanted - assigned) * cost * weight
    return total_cost

def print_cost_summary(assignment, domain, constraints_dict):
    skill = lack_required_skill(assignment, domain, constraints_dict['lack_required_skill'])
    many_workers = too_many_workers(assignment, domain, constraints_dict['too_many_workers'])
    few_workers = too_few_workers(assignment, domain, constraints_dict['too_few_workers'])
    many_tasks = too_many_tasks(assignment, domain, constraints_dict['too_many_tasks'])
    few_tasks = too_few_tasks(assignment, domain, constraints_dict['too_few_tasks'])
    print "SKILL", skill
    print "TOO MANY WORKERS", many_workers
    print "TOO FEW WORKERS", few_workers
    print "TOO MANY TASKS", many_tasks
    print "TOO FEW TASKS", few_tasks
    print "TOTAL: ", skill + many_workers + many_tasks + few_workers + few_tasks

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

