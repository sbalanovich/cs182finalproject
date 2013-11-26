
def skill_constraint(assignment, domain, cost):
    workers, tasks = domain
    total_cost = 0
    for worker in assignment.keys():
        for task in assignment[worker]:
            for skill in tasks[task].skill_reqs:
                if skill not in workers[worker].skills:
                    total_cost += cost
    return total_cost
    
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