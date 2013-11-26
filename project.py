import sys
import worker
import task
import local

if __name__ == '__main__':
    # initialize workers
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