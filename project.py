import sys
import worker
import task
import local

if __name__ == '__main__':
    # initialize workers
    
    # initialize tasks
    
    # constraints_dict
    
    # get algorithm name argument
    algo = sys.argv[0]
    getattr(local, algo)((workers, tasks), constraints_dict)