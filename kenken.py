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
        		
