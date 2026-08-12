from parser import Declaration, Constant, Assignment, Output, Input, If_loop, While_loop, For_loop, Repeat_loop, CaseOf, Call, Length, Integer, Random, Right, Mid, Lcase, Ucase
import random
from typing import Final

class interpreter:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes
        self.variables = {}

    def resolve(self, node):
        if self.check(node, Declaration):
            self.variables[node.var.string_] = node.datatype
        elif self.check(node, Constant):
            self.variables[node.var.string_] = Final[node.datatype]
        elif self.check(node, Assignment):
            var_str = " ".join(node.branch)
            self.variables[node.var] = self. # finish this
        elif self.check(node, Output):
            print(node.branch)
        elif self.check(node, Input):
            node.var = input()
        elif self.check(node, If_loop):
        elif self.check(node, While_loop):
        elif self.check(node, For_loop):
        elif self.check(node, Repeat_loop):
        elif self.check(node, CaseOf):
        elif self.check(node, Call):
            parameter_str = ", ".join(node.parameters)
            node.subrouting.string_(parameter_str)
        elif self.check(node, Length):
            return len(node.str_branch)
        elif self.check(node, Integer):
            return int(node.branch)
        elif self.check(node, Random):
            return random.randrange(node.var)
        elif self.check(node, Right):
            return node.var[len(node.var)-node.length:len(node)]
        elif self.check(node, Mid):
            return node.var[node.place - 1:node.place - 1 + node.length]
        elif self.check(node, Lcase):
            return node.var.lower()
        elif self.check(node, Ucase):
            return node.var.upper()