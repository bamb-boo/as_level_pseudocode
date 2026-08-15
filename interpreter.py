from parser import Declaration, Constant, Assignment, Output, Input, If_loop, While_loop, For_loop, Repeat_loop, CaseOf, Call, Length, Integer, Random, Right, Mid, Lcase, Ucase, Arraydeclare
import random
from tokenizer import token
from typing import Final

class interpreter:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes
        self.variables = {}
        self.procedures = {}

    def get_str(self, val):
        if isinstance(val, token):
            return val.string_
        if val is not None:
            return str(val)
        else:
            return ""
        
    def eval(self, expression):
        if isinstance(expression, str):
            if (expression.startswith('"') and expression.endswith('"')) or (expression.startswith("'") and expression.endswith("'")):
                return expression[1:-1]
            
            if expression in self.variables:
                return self.variables[expression]
            try:
                return int(expression)
            except ValueError:
                try:
                    return float(expression)
                except ValueError:
                    return SyntaxError("variable not found")
                    
        return expression
    
    def run(self):
        for node in self.ast_nodes:
            if node is not None:
                self.resolve(node)
        
    def resolve(self, node):
        if isinstance(node, Declaration):
            var_name = self.get_str(node.name)
            self.variables[var_name] = node.datatype

        elif isinstance(node, Constant):
            var_name = self.get_str(node.name)
            self.variables[var_name] = Final[node.datatype]

        elif isinstance(node, Assignment):
            var_name = self.get_str(node.var)

            if isinstance(node.branch, list):
                    var_str = " ".join([self.get_str(i) for i in node.branch])
            else:
                var_str = self.get_str(node.branch)
            self.variables[var_name] = self.eval(var_str)

        elif isinstance(node, Output):
            eval = []
            if isinstance(node.branch, list):
                for i in node.branch:
                    eval.append(str(self.eval(self.get_str(i))))
            else:
                eval.append(str(self.eval(self.get_str(node.branch))))
            print(" ".join(eval))

        elif isinstance(node, Input):
            var_name = self.get_str(node.var)
            self.variables[var_name] = self.eval(input())

        elif isinstance(node, If_loop):
            if self.eval(self.get_str(node.condition)):
                for i in node.branch:
                    self.resolve(i)
            elif node.else_loop:
                for i in node.else_loop:
                    self.resolve(i)

        elif isinstance(node, While_loop):
            while self.eval(self.get_str(node.condition)):
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
            name = node.subroutine
            if name in self.procedures:
                for i in self.procedures[name].body:
                    self.resolve(i)
            else:
                raise SyntaxError("subroutine not defined")

        elif isinstance(node, Length):
            return len(str(self.eval(node.str_branch)))
        
        elif isinstance(node, Integer):
            return int(self.eval(node.branch))

        elif isinstance(node, Random):
            return random.randrange(int(self.eval(node.var)))

        elif isinstance(node, Right):
            var = str(self.eval(self.get_str(node.var)))
            length = int(self.eval(self.get_str(node.length)))
            return var[-length:] if length < len(var) else var

        elif isinstance(node, Mid):
            var = str(self.eval(self.get_str(node.var)))
            place = int(self.eval(self.get_str(node.place)))
            length = int(self.eval(self.get_str(node.length)))
            return var[place - 1:place - 1 + length]

        elif isinstance(node, Lcase):
            return str(self.eval(node.var)).lower()

        elif isinstance(node, Ucase):
            return str(self.eval(node.var)).upper()

        elif isinstance(node, Array):
            if not node.y:
                x = node.x
                return x
            else:
                x = node.x
                y = node.y
                both = []
                both.append(x)
                both.append(y)
                return both
            

def get_string(self, val):
    if isinstance(val, token):
        return val.string_
    if val is not None:
        return str(val)
    else:
        return ""

def get_string(self, val):
    if isinstance(val, token):
        return val.string_
    if val is not None:
        return str(val)
    else:
        return ""