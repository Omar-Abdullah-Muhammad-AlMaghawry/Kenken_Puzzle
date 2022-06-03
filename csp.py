"""CSP (Constraint Satisfaction Problems) problems and solvers. (Chapter 6)."""

from unittest import result
from utils import argmin_random_tie, count, first
#import search


class Constrain_Satsified_Problem():
    def __init__(self, variables, domains, neighbors, constraints):
        "Construct a CSP problem. If variables is empty, it becomes domains.keys()."
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
    def assigned_value(self, V, value, assignment):
        "make an assignment for the variable(V) the value(value) ."
        assignment[V] = value
        self.nassigns += 1
    def Remove_assigned_value(self, V, assignment):
        "remove assigned val for the assigned variable"
        if V in assignment:
            del assignment[V]

    def num_of_conflicts(self, V, value, assignment):
        "Return the number of conflicts of the variable with other variables when assign to it the value."
        def conflict_with_neigh(V2):
            if(V2 in assignment and not self.constraints(V, value, V2, assignment[V2])):
                return 1
            else:
                return 0

        x=count(conflict_with_neigh(v) for v in self.neighbors[V])
            
        return x


    def display(self, assignment):
        "Show a human-readable representation of the CSP."
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    def result(self, state, action):

        (var, val) = action

        newState = state + ((var, val),)

        return newState 


  

    # this var check if we acjieve our goal or not,
    # by checking if each var has its value and
    # and satisfy his constraint or not
    def goal_test(self, state):
        assignment = dict(state)
        # we go through each var, and count the 
        # number of the conflicts with its neighbirs
        # by passing the var and the val assigned to it
        # and the total assinment
        count = 0
        for v in self.variables:
            count += self.num_of_conflicts(v,assignment[v], assignment)
        
        #if it's zero conflict 
        # that mean there no conflict here
        conflict = True
        if count == 0:
            conflict = False

        #check if all the variable assigned or not
        allAssigned = False
        if len(assignment) == len(self.variables):
            allAssigned= True

        return ( allAssigned and not conflict)


    
    def support_pruning(self):
        # prune values from domains
        if self.curr_domains is None:
            keys = []
            for y in self.variables:
                keys.append(y)
                self.curr_domains = { y: list(self.domains[y]) for y in keys if y in self.domains}

    
    def assume(self, variable, val):
        #from assuming var=value accumulating inferences
        self.support_pruning()
        temp_var = []
        for x in self.curr_domains[variable] :
          if x != val:
            temp_var.append((variable, x))
        self.curr_domains[variable] = [val]
        return temp_var


    def prune(self, variable, val, Removal):
        #  rule out var=value
        self.curr_domains[variable].remove(val)
        if Removal is not None:
            Removal.append((variable, val))

   
    def values_options(self, var):
        #Retriev all values for this variable that aren't ruled out till now
        #print('inside choices')
        if self.curr_domains:
            if var in self.curr_domains:
                return self.curr_domains[var]
        if self.domains:
            if var in self.domains:
                return self.domains[var]

    def get_partially_assigned_vars_dict(self):
        #return a dictionary of the vars that have been assigned by the current inference .i.e Algorithm

        #list of wanted keys
        wanted_keys = []
        self.support_pruning()

        for x in self.variables:
            if len(self.curr_domains[x]) == 1:
                wanted_keys.append(x)

        return {k: self.curr_domains[k][0] for k in wanted_keys if k in self.curr_domains }
