import sys
import worker
import task
import local
import csv

if __name__ == '__main__':
    # initialize workers
    with open("test.csv", "rb") as inputfile:
        reader = csv.reader(inputfile)
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

    tasks = {}
    tasks['1'] = task.Task('1', skill_reqs = ['Computer'])
    tasks['2'] = task.Task('2', skill_reqs = ['Sorting'])

    # constraints_dict
    constraints_dict = {
        'skill_constraint' : (True, 1),
        'all_assigned_constraint' : (True, 1),
        'assigned_once_constraint' : (True, 1)
    }

    # get algorithm name argument
    algo = sys.argv[1]
    solution = getattr(local, algo)((workers, tasks), constraints_dict)
    print solution
    

    '''
    workers = {}
    workers['A'] = worker.Worker('A', skills = ['Computer'])
    workers['B'] = worker.Worker('B', skills = ['Sorting'])
    workers['C'] = worker.Worker('C', skills = ['Computer', 'Sorting'])
    workers['D'] = worker.Worker('D')
    
    # initialize tasks
    tasks = {}
    tasks['1'] = task.Task('1', skill_reqs = ['Computer'])
    tasks['2'] = task.Task('2', skill_reqs = ['Sorting'])
    
    # constraints_dict
    constraints_dict = {
        'skill_constraint' : (True, 1),
        'all_assigned_constraint' : (True, 1),
        'assigned_once_constraint' : (True, 1)
    }
    
    # get algorithm name argument
    algo = sys.argv[1]
    solution = getattr(local, algo)((workers, tasks), constraints_dict)
    print solution
    '''