# task class
class Task:
    
    # constructor
    def __init__(self, name, skill_reqs = [], num_workers=1):
        self.name = name
        self.skill_reqs = skill_reqs
        self.num_workers = num_workers

    # other stuff
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)