import sys
import worker
import task
import local
import csv

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
            num_tasks = row[-1]
            workers[name] = worker.Worker(name, skills = skills, num_tasks = num_tasks)

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
            num_workers = row[-1]
            tasks[taskNumber] = task.Task(taskNumber, skill_reqs = skills, num_workers = num_workers)

    # constraints_dict
    constraints_dict = {
        'skill_constraint' : (True, 100),
        'too_many_workers' : (True, 5),
        'too_few_workers' : (True, 20),
        'too_many_tasks' : (True, 20),
        'too_few_tasks' : (True, 5)
        #'all_assigned_constraint' : (True, float("inf")),
        #'assigned_once_constraint' : (True, 1)
    }

    # get algorithm name argument
    algo = sys.argv[1]
    solution = getattr(local, algo)((workers, tasks), constraints_dict)
    print solution
