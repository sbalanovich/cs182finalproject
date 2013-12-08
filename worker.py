# worker class
class Worker:
    
    # constructor
    def __init__(self, name, skills = [], effs = {}, prefs = {}, num_tasks = 0):
        self.name = name
        self.skills = skills
        self.effs = effs
        self.prefs = prefs
        self.num_tasks = num_tasks

    # other stuff
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)