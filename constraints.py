
def skill_constraint(assignment, domain):
    workers, tasks = domain
    cost = 0
    for task in assignment.keys():
        for skill in tasks[task].skill_reqs:
            for worker in assignment[task]:
                if skill not in workers[worker].skills:
                    cost += float("inf")
    return cost