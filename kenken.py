import csp
import re
import sys
import randomize_grid
from time import time
from csv import writer
from sys import stderr, stdin

# from random import randint, shuffle, choice
# import numpy as np

class KenKen():
    
    def __init__(self, size, lines):

        self.vars = list()
        self.adjecent = dict()
        self.block_V = list()
        self.block_Op = list()
        self.block_Val = list()
        self.block_Vs = list()
        
        
        """make variables list from input"""
        for i in range(size):
            for j in range(size):
                self.vars.append('K' + str(i) + str(j))
    
        """make domains dictionary """
        dict_Domains_Vals = list(range(1, size+1))
        self.domains = dict((v, dict_Domains_Vals) for v in self.vars)
    
        """make neighbors dictionary"""
        for v in self.vars:
            dict_Adjecent_Val = []
            coord_X = int(list(v)[1])
            coord_Y = int(list(v)[2])
    
            for i in range(size):
                if i != coord_Y:
                    string = 'K' + str(coord_X) + str(i)
                    dict_Adjecent_Val.append(string)
                if i != coord_X:
                    string = 'K' + str(i) + str(coord_Y)
                    dict_Adjecent_Val.append(string)
    
            self.adjecent[v] = dict_Adjecent_Val
    
    
        """make constraint data lists"""
        for l in lines:
            Variable, op, value = l.split()

            self.block_V.append(re.findall('\d+', Variable))
            # print(self.block_V)
            self.block_Op.append(op)
            self.block_Val.append(int(value))
    
    
        for i in range(len(self.block_V)):
            block_List = []
            for j in range(0, len(self.block_V[i]), 2):
                string = 'K' + str(self.block_V[i][j]) + str(self.block_V[i][j+1])
                block_List.append(string)
            # print(self.block_Vs)
            self.block_Vs.append(block_List)                
    
    def insertGame(self,game):
        self.game_kenken = game
 
    def constraint(self, var1, val1, var2, val2):
        if var2 in self.adjecent[var1]:
            if val1 == val2:
                return False

        for i in self.adjecent[var1]:
            if i in self.game_kenken.get_partially_assigned_vars_dict():
                if self.game_kenken.get_partially_assigned_vars_dict()[i] == val1:
                    return False

        for j in self.adjecent[var2]:
            if j in self.game_kenken.get_partially_assigned_vars_dict():
                if self.game_kenken.get_partially_assigned_vars_dict()[j] == val2:
                    return False

        block_A_Num = block_B_Num = 0
        Block_var_length = len(self.block_Vs)
        for x in range(Block_var_length):
            if var1 in self.block_Vs[x]:
                block_A_Num = x
            if var2 in self.block_Vs[x]:
                block_B_Num = x
        if block_A_Num == block_B_Num:
            block_Num = block_A_Num
            if self.block_Op[block_Num] == "''":
                if var2 != var1:
                    return False
                elif val2 != val1:
                    return False
                elif self.block_Val[block_Num] != val1:
                    return False

                return True

            
            elif self.block_Op[block_Num] == 'mult':
                mult_SameBlock = 1
                num_Assignments = 0
                # we go through to each var and in the block 
                # and check if it has on value in his domain 
                # if it's we just mult it, if not we don't return value of it
                for i in self.block_Vs[block_Num]:
                    if var1 == i:
                        mult_SameBlock *= val1
                        num_Assignments = num_Assignments + 1
                    elif var2 == i:
                        mult_SameBlock =mult_SameBlock * val2
                        num_Assignments = num_Assignments + 1
                    elif i in self.game_kenken.get_partially_assigned_vars_dict():
                        mult_SameBlock = mult_SameBlock * self.game_kenken.get_partially_assigned_vars_dict()[i]
                        num_Assignments = num_Assignments + 1

                block_var_len = len(self.block_Vs[block_Num])
                # we check if the mult is equal it the required result or not
                # we check if the number of the var we assinged equal to the number of var or not 
                if mult_SameBlock == self.block_Val[block_Num] and num_Assignments == block_var_len:
                    return True
                # we check if the mult is less it the required result or not
                # we check if the number of the var we assinged less to the number of var or not 
                elif mult_SameBlock <= self.block_Val[block_Num] :
                    if num_Assignments < len(self.block_Vs[block_Num]):
                       return True
                else:
                    return False


            elif self.block_Op[block_Num] == 'div':
                flag = 0
                result = max(val1, val2) / min(val1, val2)
                if result == self.block_Val[block_Num]:
                    flag = 1
                return flag

            elif self.block_Op[block_Num] == 'sub':
                flag2 = 0
                result = max(val1, val2) - min(val1, val2)
                if result == self.block_Val[block_Num] :
                    flag2= 1
                return  flag2
            elif self.block_Op[block_Num] == 'add':
                sum_SameBlock = num_Assignments = 0
                # we go through to each var and in the block 
                # and check if it has on value in his domain 
                # if it's we just sum it, if not we don't return value of it
                for y in self.block_Vs[block_Num]:
                    if var1 == y:
                        sum_SameBlock = sum_SameBlock + val1
                        num_Assignments =num_Assignments+ 1
                    elif var2 == y:
                        sum_SameBlock =sum_SameBlock + val2
                        num_Assignments =num_Assignments +  1
                    elif y in self.game_kenken.get_partially_assigned_vars_dict():
                        sum_SameBlock = sum_SameBlock + self.game_kenken.get_partially_assigned_vars_dict()[y]
                        num_Assignments =num_Assignments + 1
                
                # we check if the sum is equal it the required result or not 
                # we check if the number of the var we assinged equal to the number of var or not 
                if sum_SameBlock == self.block_Val[block_Num]:
                    if num_Assignments == len(self.block_Vs[block_Num]):
                        return True
                # we check if the sum is less it the required result or not      
                # we check if the number of the var we assinged less to the number of var or not 
                elif sum_SameBlock < self.block_Val[block_Num]:
                    if num_Assignments < len(self.block_Vs[block_Num]):
                        return True
                else:
                    return False


        else:
            constraintA = self.constraint_op(var1, val1, block_A_Num)
            constraintB = self.constraint_op(var2, val2, block_B_Num)

            return constraintA and constraintB
        		
  def constraint_op(self, variable, value, block_Num):
        if self.block_Op[block_Num] == "''":
            return value == self.block_Val[block_Num]
    
        elif self.block_Op[block_Num] == 'add':
            sum = 0
            num_Assignment2 = 0
            # we go through to each var and in the block 
            # and check if it has on value in his domain 
            # if it's we just sum it, if not we don't return value of it    
            for V in self.block_Vs[block_Num]:

                if V == variable:
                    sum += value
                    num_Assignment2 += 1
                elif V in self.game_kenken.get_partially_assigned_vars_dict():
                    sum += self.game_kenken.get_partially_assigned_vars_dict()[V]
                    num_Assignment2 += 1

            # we check if the sum is equal it the required result or not 
             # we check if the number of the var we assinged equal to the number of var or not 
   
            if sum == self.block_Val[block_Num] and num_Assignment2 == len(self.block_Vs[block_Num]):
                    return True
            # we check if the sum is less it the required result or not      
            # we check if the number of the var we assinged less to the number of var or not 
  
            elif sum <= self.block_Val[block_Num] and num_Assignment2 < len(self.block_Vs[block_Num]):
                    return True
            else:
                return False
    
        elif self.block_Op[block_Num] == 'mult':
            mult2 = 1
            num_Assignment2 = 0
            
            # we go through to each var and in the block 
            # and check if it has on value in his domain 
            # if it's we just mult it, if not we don't return value of it
            for V in self.block_Vs[block_Num]:
            
                if V == variable:
                    mult2 *= value
                    num_Assignment2 += 1
                elif V in self.game_kenken.get_partially_assigned_vars_dict():
                    mult2 *= self.game_kenken.get_partially_assigned_vars_dict()[V]
                    num_Assignment2 += 1

            # we check if the mult is equal it the required result or not
            # we check if the number of the var we assinged equal to the number of var or not 
            if mult2 == self.block_Val[block_Num] and num_Assignment2 == len(self.block_Vs[block_Num]):
                    return True

            # we check if the mult is less it the required result or not
            # we check if the number of the var we assinged less to the number of var or not 
            elif mult2 <= self.block_Val[block_Num] and num_Assignment2 < len(self.block_Vs[block_Num]):
                    return True
            else:
                return False
    
        elif self.block_Op[block_Num] == 'div':
            for V in self.block_Vs[block_Num]:
                if V != variable:
                    constraint_Var2 = V
    
            if constraint_Var2 in self.game_kenken.get_partially_assigned_vars_dict():
                constraint_Val2 = self.game_kenken.get_partially_assigned_vars_dict()[constraint_Var2]
                value= max(constraint_Val2, value) / min(constraint_Val2, value)
                res=value == self.block_Val[block_Num]
                return res
            else:
                for d in self.game_kenken.values_options(constraint_Var2):
                    x=max(d, value) / min(d, value)
                    if x == self.block_Val[block_Num]:
                        return True
    
                return False
        elif self.block_Op[block_Num] == 'sub':
            for x in self.block_Vs[block_Num]:
                if x != variable:
                    constraint_Var2 = x
    
            if constraint_Var2 in self.game_kenken.get_partially_assigned_vars_dict():
                constraint_Val2 = self.game_kenken.get_partially_assigned_vars_dict()[constraint_Var2]
                temp = max(constraint_Val2, value) - min(constraint_Val2, value)
                res = temp == self.block_Val[block_Num]
                return res
            else:
                for x in self.game_kenken.values_options(constraint_Var2):
                    temp = max(x, value) - min(x, value)
                    if temp  == self.block_Val[block_Num]:
                        return True
    
                return False	
    
    def display(self, dic, size):
        for i in range(size):
            for j in range(size):
                string = 'K' + str(i) + str(j)
                sys.stdout.write(str(dic[string]) + " ")
            print()
    
def getLines(size):
        lines = []
        rarr = randomize_grid.randomize_grid(size)
        cages = randomize_grid.randomize_cages(rarr)

        for cage in cages:
            var = cage[0]
            op= cage[1]
            val = cage[2]
            strVar = str(var)
            l = strVar.split()
            varSt = ""
            for l1 in l:
                varSt += l1 
            # varSt.join(l)
            # print(varSt)
            lines.append( varSt + " "+ str(op) + " " + str(val) + "\n" )
        
        return lines
       
def gather(iterations, out):
  
            bt         = lambda ken: csp.backtracking_search(game_kenken)
            # bt_mrv     = lambda ken: csp.backtracking_search(game_kenken, select_unassigned_variable=csp.mrv)
            fc         = lambda ken: csp.backtracking_search(game_kenken, inference=csp.forwardCheckingFn)
            # fc_mrv     = lambda ken: csp.backtracking_search(game_kenken, inference=csp.forwardCheckingFn, select_unassigned_variable=csp.mrv)
            mac        = lambda ken: csp.backtracking_search(game_kenken, inference=csp.mac)
            # mconflicts = lambda ken: csp.min_conflicts(ken)

            algorithms = {
                "BT": bt,
                # "BT+MRV": bt_mrv,
                "FC": fc,
                # "FC+MRV": fc_mrv,
                "MAC": mac,
                # "MIN_CONFLICTS": mconflicts
            }

            with open(out, "w+") as file:

                out = writer(file)

                out.writerow(["Algorithm","Size","Avg Time Per Iteration"])    


                for name, algorithm in algorithms.items():
                    for size in range(3, 10):
                        checks, assignments, dt = (0, 0, 0)
                        for iteration in range(1, iterations + 1):
                        
                            # V=randomize_grid(size)
                            # lines =randomize_cages(V)
                            lines = getLines(size) 
                            # print(lines)
                            kenken=KenKen(size, lines)   
                            game_kenken = csp.Constrain_Satsified_Problem(kenken.vars, kenken.domains, kenken.adjecent, kenken.constraint)
                            kenken.insertGame(game_kenken)
                            assignment, time = benchmark(game_kenken, algorithm)
                        
                        print("algorithm =",  name, "size =", size, "iteration =", iteration, "result =", "Success" if assignment else "Failure", file=stderr)
                        time = time / iterations
                        out.writerow([name, size, time])




def benchmark(kenken, algorithm):


        dt = time()

        assignment = algorithm(kenken)

        dt = time() - dt

        return assignment,  dt

		
		
		
if __name__ == '__main__':
    

    gather(3, "ken.csv")
