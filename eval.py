import constraints

# evaluator class
class Evaluator:
    
    # constructor
    def __init__(self, assignment, workers, tasks, constraints = {}):
        for key in constraints.keys():
            if constraints[key]:
                
                

    # other stuff
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)
        
import constraints

def evaluation_func(constraints_dict):
    total_cost = 0
    for key in constraints_dict.keys():
        if constraints_dict[key]:
            total_cost += getattr(constraints, key)()
    return cost