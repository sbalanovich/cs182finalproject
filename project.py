import sys
import worker
import task
import local
import csv
from constraints import print_cost_summary

if __name__ == '__main__':
    # initialize workers
    with open("workers.csv", "rb") as workersFile:
        reader = csv.reader(workersFile)
        skillList = next(reader, None)[1:-1]
        workers = {}
        for row in reader:
            name = row[0]
            skillsTF = row[1:-1] # e.g. ['T', 'F', 'T', 'F']
            skills = [] # e.g. ['Computer', 'Sorting']
            for i in xrange(len(skillsTF)):
                if skillsTF[i] == 'T':
                    skills.append(skillList[i])
            wanted_tasks = row[-1]
            workers[name] = worker.Worker(name, skills = skills, wanted_tasks = wanted_tasks)

    # initialize tasks
    with open("tasks.csv", "rb") as tasksFile:
        reader = csv.reader(tasksFile)
        skillList = next(reader, None)[1:-1]
        tasks = {}
        for row in reader:
            taskNumber = row[0]
            skillsTF = row[1:-1] # e.g. ['T', 'F', 'T', 'F']
            skills = [] # e.g. ['Computer', 'Sorting']
            for i in xrange(len(skillsTF)):
                if skillsTF[i] == 'T':
                    skills.append(skillList[i])
            wanted_workers = row[-1]
            tasks[taskNumber] = task.Task(taskNumber, skill_reqs = skills, wanted_workers = wanted_workers)

    # constraints_dict
    constraints_dict = {
        'skill_constraint' : 200,
        'too_many_workers' : 10,
        'too_few_workers' : 20,
        'too_many_tasks' : 10,
        'too_few_tasks' : 20
    }

    # get algorithm name argument
    algo = sys.argv[1]
    solution = getattr(local, algo)((workers, tasks), constraints_dict)
    print solution
    print_cost_summary(solution, (workers, tasks), constraints_dict)
