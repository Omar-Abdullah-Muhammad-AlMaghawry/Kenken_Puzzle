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


   
    def undo_removals(self, removals):
        #add or restore the Removed values again
        for vari, val in removals:
            self.curr_domains[vari].append(val)

    def num_conflicted_vars(self, current):
        #Return a list of variables that are in conflict in the current assignment
        temp_vars = []
        for var in self.variables:
            if self.num_of_conflicts(var, current[var], current) > 0:
                temp_vars.append(var)

        return temp_vars



def Arc_Consistency3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(A, k) for A in csp.variables for k in csp.neighbors[A]]
    csp.support_pruning()
    while queue:
        (A, B) = queue.pop()
        if revised(csp, A, B, removals):
            if not csp.curr_domains[A]:
                return False

            for k in csp.neighbors[A]:
                if k != A:
                    queue.append((k, A))
    return True
def revised(csp, A, B, removals):
    "Return true if we remove a value."
    res = False
    for x in csp.curr_domains[A][:]:
        #check if their is no value in A not conflict with all valuse of B,remove X and return true
        if all(not csp.constraints(A, x, B, y) for y in csp.curr_domains[B]):#chanage constraints
            csp.prune(A, x, removals)
            res = True
    return res

# def first_unassigned_variable(assignment, csp):
#     "The default variable order."
#     return first([var for var in csp.variables if var not in assignment]) 
def first_unassigned_variable(assignment, csp):
    #return the first variable in the list
    temp_vars = []
    for var in csp.variables:
        if var not in assignment:
            temp_vars.append(var)
    return temp_vars[0]


def mrv(assignment, csp):
    varList = []
    # we go through in each var in the variable of 
    # the problem, and check if var in dictionary assigement as an index 
    # or not
    # if it's not we add it to hte list
    for var in csp.variables:
        if var not in assignment:
            varList.append(var)
    # we count the number 
    def key(var):
        return num_legal_values(csp, var, assignment)
    # key = lambda var: num_legal_values(csp, var, assignment)
    return argmin_random_tie(varList,key)
        # [v for v in csp.variables if v not in assignment],
        # key=lambda var: num_legal_values(csp, var, assignment))




def num_legal_values(csp, variable, assign):
    flag = 0
    for v in csp.domains[variable] :
        if csp.num_of_conflicts(variable, v, assign) == 0 :
            flag += 1
        return flag


# Value ordering


def unordered_domain_values(var, assignment, csp):
    "The default value order."
    return csp.values_options(var)




def no_inference(csp, var, value, assignment, removals):
    return True


#here the forward checking that it will be used for help us 
#in like back tracking
def forwardCheckingFn(csp, var, value, assignment, removals):
    
    "Prune neighbor values inconsistent with var=value."

    #we go through for each var (B) in the neighbors
    for B in csp.neighbors[var]:
    
        #not all var, just the vars who has have on values in its domain yet
        if B not in assignment:
    
            # we go through the domain  of this neighbor who hasn't 
            # been assigned yet 
            for b in csp.curr_domains[B][:]:

                # now we see if we give this value will pass the constrain or not
                # if it doesn't pass we, so we have a problem with this value
                # so we have to del from the domain
                if not csp.constraints(var, value, B, b):
                    # we just del this value from the domain,
                    # and add it to the removals, which we remove from the domain 
                    csp.prune(B, b, removals)
            
            # After finishing the loop, and remove from the values
            # from the domain of this neighbor, if the domain
            # become empty so, the forward checkin failed 
            if not csp.curr_domains[B]:
                return False

            #other wise we go to the next neighbor who hasn't been assigned yet
            #and for each value of its domain, and change its domain
    
    return True



def mac(csp, var, value, assignment, Removal):
    temp = []
    for x in csp.neighbors[var] :
        temp.append((x, var))
    return Arc_Consistency3(csp, temp , Removal)



def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    
    # we defin this function inside the general func 
    # to use it inside
    # which take the var wit its assignment 
    # and try to solve the problem
    # by giving each var an value, without violete the 
    # constraints
    def backtrack(assignment):
        #if the assinment equal the var so we are finsined, 
        # we don't need to do any thing
        if len(assignment) == len(csp.variables):
            return assignment
        # here we get the var that aren't assigned yet
        # to make the alogritm on it, which give one value to it
        var = select_unassigned_variable(assignment, csp)
        
        # here we go through to thi values in the domai of the var 
        # just we choose
        for value in order_domain_values(var, assignment, csp):#csp.choices(var)
            
            # now we check if we can give our var, this value or not
            # if by check the number of conflicts with his neighbor
            # in the row , col, and the block
            if 0 == csp.num_of_conflicts(var, value, assignment):

                # if there is no conflict we just assign this 
                # val to this var, by adding it to the dic of 
                # of the assingment
                csp.assigned_value(var, value, assignment)

                # and del it from the domain of that var
                # also add it to the val we romve in th removal
                removals = csp.assume(var, value)

                # if we want to make backtrack with any other algoritm like
                # forward checking or arc consistance , we do it,
                # and check if it's posible for other neighbours 
                # if we choose the current val to our assignment 
                # and also propgate the result to minimze the domains of them
                if inference(csp, var, value, assignment, removals):

                    #once we minimize thier domains 
                    # that means there will be some var has already assigned,
                    # and other not so we do the backtrack to other one 
                    result = backtrack(assignment)

                    # if the result is not none so it's done
                    if result is not None:
                        return result
                # if the result is none we restore every thing, or if the val fialed
                csp.undo_removals(removals)
        csp.Remove_assigned_value(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result