import sys
import worker
import task
import local
import csv

if __name__ == '__main__':
    # initialize workers
    with open("workers.csv", "rb") as workersFile:
        reader = csv.reader(workersFile)
        skillList = next(reader, None)[1:]
        workers = {}
        for row in reader:
            name = row[0]
            skillsTF = row[1:] # e.g. ['T', 'F', 'T', 'F']
            skills = [] # e.g. ['Computer', 'Sorting']
            for i in xrange(len(skillsTF)):
                if skillsTF[i] == 'T':
                    skills.append(skillList[i])
            workers[name] = worker.Worker(name, skills = skills)

    # initialize tasks
    with open("tasks.csv", "rb") as tasksFile:
        reader = csv.reader(tasksFile)
        skillList = next(reader, None)[1:]
        tasks = {}
        for row in reader:
            taskNumber = row[0]
            skillsTF = row[1:] # e.g. ['T', 'F', 'T', 'F']
            skills = [] # e.g. ['Computer', 'Sorting']
            for i in xrange(len(skillsTF)):
                if skillsTF[i] == 'T':
                    skills.append(skillList[i])
            tasks[taskNumber] = task.Task(taskNumber, skill_reqs = skills)

    # constraints_dict
    constraints_dict = {
        'skill_constraint' : (True, 1),
        'all_assigned_constraint' : (True, float("inf")),
        'assigned_once_constraint' : (True, 5)
    }

    # get algorithm name argument
    algo = sys.argv[1]
    solution = getattr(local, algo)((workers, tasks), constraints_dict)
    print solution
