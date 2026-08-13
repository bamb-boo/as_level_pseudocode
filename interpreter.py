from parser import Declaration, Constant, Assignment, Output, Input, If_loop, While_loop, For_loop, Repeat_loop, CaseOf, Call, Length, Integer, Random, Right, Mid, Lcase, Ucase
import random
from typing import Final

class interpreter:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes
        self.variables = {}

    def eval(self, expression):
        if isinstance(expression, str):
            if expression in self.variables:
                return self.variables[expression]
            try:
                return int(expression)
            except ValueError:
                try:
                    return float(expression)
                except ValueError:
                    return expression
        return expression
        
    def resolve(self, node):
        if isinstance(node, Declaration):
            self.variables[node.var.string_] = node.datatype

        elif isinstance(node, Constant):
            self.variables[node.var.string_] = Final[node.datatype]

        elif isinstance(node, Assignment):
            if self.check(node.branch, list):
                var_str = " ".join(node.branch)
            else:
                node.branch()

            self.variables[node.var] = self.eval(var_str)

        elif isinstance(node, Output):
            eval = []
            for i in node.branch:
                eval.append(str(self.eval(i)))
            print(" ".join(eval))

        elif isinstance(node, Input):
            self.variables[node.var] = self.eval(input())

        elif isinstance(node, If_loop):
            if self.eval(node.condition):
                for i in node.branch:
                    self.resolve(i)
            elif node.else_loop:
                for i in node.else_loop:
                    self.resolve(i)

        elif isinstance(node, While_loop):
            while self.eval(node.condition):
                for i in node.branch:
                    self.resolve(i)

        elif isinstance(node, For_loop):
            start = int(self.eval(node.value1))
            end = int(self.eval(node.value2))
            step = int(self.eval(node.step))
            if step > 0:
                x = 1
            else:
                x = -1
            for i in range(start, end + x, step):
                self.variables[node.index] = i
                for x in node.branch:
                    self.resolve(x)

        elif isinstance(node, Repeat_loop):
            while True:
                for i in node.branch:
                    self.resolve(i)
                if self.eval(node.condition):
                    break

        elif isinstance(node, CaseOf):
            case_target = str(self.eval(node.identifier))
            for i in node.branch:
                if isinstance(i, list)and len(i) == 2:
                    value = i[0]
                    statement = i[1]
                    if str(self.eval(value)) == case_target:
                        self.resolve(statement)
                        break

        elif isinstance(node, Call):
            parameter_str = ", ".join(node.parameters)
            node.subroutine.string_(parameter_str)

        elif isinstance(node, Length):
            return len(str(self.eval(node.str_branch)))
        
        elif isinstance(node, Integer):
            return int(self.eval(node.branch))

        elif isinstance(node, Random):
            return random.randrange(int(self.eval(node.var)))

        elif isinstance(node, Right):
            var = str(self.eval(node.var))
            length = str(self.eval(node.length))
            if length >= len(var):
                return node.var
            else:
                return node.var[-node.length:]

        elif isinstance(node, Mid):
            var = str(self.eval(node.var))
            place = str(self.eval(node.place)) - 1
            length = str(self.eval(node.length))
            return var[place - 1:place - 1 + length]

        elif isinstance(node, Lcase):
            return str(self.eval(node.var)).lower()

        elif isinstance(node, Ucase):
            return str(self.eval(node.var)).upper()