from parser import Declaration, Constant, Assignment, Output, Input, If_loop, While_loop, For_loop, Repeat_loop, CaseOf, Call, Length, Integer, Random, Right, Mid, Lcase, Ucase, Arraydeclare, priority, calculate, Procedure_def, Call
import random
from tokenizer import token, tokentype, tokenize
from typing import Final
import numpy as np

class interpreter:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes
        self.variables = {}
        self.types = {}
        self.procedures = {}

    def check_type(self, var_name, value):
        expected = self.types[var_name].upper()

        if expected == "INTEGER" and not isinstance(value, int):
            raise TypeError("datatype mismatch")
        elif expected == "REAL" and not isinstance(value, (int, float)):
            raise TypeError("datatype mismatch")
        elif expected == "STRING" and not isinstance(value, str):
            raise TypeError("datatype mismatch")
        elif expected == "CHAR" and not (isinstance(value, str) and len(value) == 1):
            raise TypeError("datatype mistmatch")
        elif expected == "BOOLEAN" and not isinstance(value, bool):
            raise TypeError("datatype mismatch")
        
    def get_str(self, val):
        if isinstance(val, token):
            return val.string_
        if val is not None:
            return str(val)
        else:
            return ""
        
    # def eval(self, expression):
    #     if isinstance(expression, str):
    #         if (expression.startswith('"') and expression.endswith('"')) or (expression.startswith("'") and expression.endswith("'")):
    #             return expression[1:-1]

    #         if "[" in expression and "]" in expression:
    #             open = expression.find("[")
    #             close = expression.find("]")
    #             var_name = expression[0:open].strip()
    #             text = expression[open + 1:close].strip()
    #             part = text.split(",")

    #             if len(part) == 1:
    #                 return self.variables[var_name][int(self.eval(part[0]))]
    #             elif len(part) == 2:
    #                 return self.variables[var_name][int(self.eval(part[0])), int(self.eval(part[1]))]
                
    #         if expression in self.variables:
    #             return self.variables[expression]
            
    #         try:
    #             return int(expression)  
    #         except ValueError:
    #             try:
    #                 return float(expression)
    #             except ValueError:
    #                 pass

    #         for i in self.variables:
    #             val = self.variables[i]
    #             if val is not None:
    #                 expression = expression.replace(i, str(val))
    #         tokens = tokenize(expression)
    #         nodes = priority(tokens)
    #         result = calculate(nodes)
    #         if hasattr(result, "value"):
    #             val = result.value
    #         else:
    #             val = result
    #         try:
    #             return int(val)
    #         except ValueError:
    #             try:
    #                 return float(val)
    #             except TypeError:
    #                 return TypeError("wrong datatypes")

    #     return expression
    
    def eval(self, expression):
        if isinstance(expression, str):
            expression = expression.strip()

            # 1. Strip string literals
            if (expression.startswith('"') and expression.endswith('"')) or (expression.startswith("'") and expression.endswith("'")):
                return expression[1:-1]

            # 2. Handle array index expressions
            if "[" in expression and "]" in expression:
                open_b = expression.find("[")
                close_b = expression.find("]")
                var_name = expression[0:open_b].strip()
                text = expression[open_b + 1:close_b].strip()
                part = text.split(",")

                if len(part) == 1:
                    return self.variables[var_name][int(self.eval(part[0]))]
                elif len(part) == 2:
                    return self.variables[var_name][int(self.eval(part[0])), int(self.eval(part[1]))]
            
            # 3. Direct variable lookup
            if expression in self.variables:
                return self.variables[expression]
            
            # 4. Direct number check
            try:
                return int(expression)  
            except ValueError:
                try:
                    return float(expression)
                except ValueError:
                    pass

            # 5. Safe Variable Substitution
            # Replaces exact matching identifiers without corrupting words/operators
            for key, v in self.variables.items():
                if v is not None and key in expression:
                    # Token-boundary replacement check
                    import re
                    pattern = r'\b' + re.escape(key) + r'\b'
                    expression = re.sub(pattern, str(v), expression)

            # 6. Parse and evaluate
            tokens = tokenize(expression)
            nodes = priority(tokens)
            result = calculate(nodes)

            # Extract underlying value if stored in an object attribute
            if hasattr(result, "value"):
                val = result.value
            elif hasattr(result, "string_"):
                val = result.string_
            else:
                val = result

            # 7. Safe Type Conversion
            try:
                return int(val)
            except (ValueError, TypeError):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return val  # Returns raw result (e.g. string or evaluated boolean) if non-numeric

        return expression
    
    def run(self):
        for node in self.ast_nodes:
            if node is not None:
                self.resolve(node)
        
    def resolve(self, node):
        if isinstance(node, Declaration):
            var_name = self.get_str(node.name)
            self.variables[var_name] = None
            datatype = self.get_str(node.datatype).upper()
            self.types[var_name] = datatype

        elif isinstance(node, Constant):
            var_name = self.get_str(node.name)
            self.variables[var_name] = Final[node.datatype]

        elif isinstance(node, Assignment):
            var_name = self.get_str(node.var)

            if isinstance(node.branch, list):
                    var_str = " ".join([self.get_str(i) for i in node.branch])
            else:
                var_str = self.get_str(node.branch)

            var_str = var_str.replace("<-", "").strip()
            val = self.eval(var_str)

            if getattr(node, "indices", None):
                if len(node.indices) == 1:
                    first = int(self.get_str(node.indices[0]))
                    self.variables[var_name][first] = val
                
                elif len(node.indices) == 2:
                    first = int(self.get_str(node.indices[0]))
                    second = int(self.get_str(node.indices[1]))
                    self.variables[var_name][first, second] = val
            else:
                self.variables[var_name] = val

        elif isinstance(node, Output):
            eval = []
            if isinstance(node.branch, list):
                string = ""
                for i in node.branch:
                    string = string + self.get_str(i)
                result = str(self.eval(string))
            else:
                result = str(self.eval(self.get_str(node.branch)))
            print(result)

        elif isinstance(node, Input):
            var_name = self.get_str(node.var)
            val= input()
            if var_name in self.types:
                expected = self.types[var_name]
                if expected == "INTEGER":
                    val = int(val)
                elif expected == "REAL":
                    val = float(val)
                elif expected == "BOOL":
                    val = bool(val)
            self.check_type(var_name, val)
            self.variables[var_name] = val

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
                self.check_type(node.index, i)
                self.variables[node.index] = i
                for j in node.branch:
                    self.resolve(j)

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

        elif isinstance(node, Arraydeclare):
            var_name = self.get_str(node.name)
            try:
                first = int(node.dimensions[0]) + 1
                second = int(node.dimensions[1]) + 1
                third = int(node.dimensions[2]) + 1
                fourth = int(node.dimensions[3]) + 1
                var = np.empty((second, fourth))
            except IndexError:
                first = int(node.dimensions[0]) + 1
                second = int(node.dimensions[1]) + 1
                var = np.empty(second)

            self.variables[var_name] = var

        elif isinstance(node, Procedure_def):
            self.procedures[node.name] = node

        elif isinstance(node, Call):
            name = node.subroutine
            if name in self.procedures:
                pro = self.procedures[name]
                if hasattr(node, "parameters") and node.parameters is not None:
                    args = []
                    if isinstance(node.parameters, str):
                        raw_args = node.parameters.replace(",", " ").split()
                    else:
                        raw_args = node.parameters

                    for arg in raw_args:
                        args.append(self.eval(arg))
                    
                    min = len(pro.params)
                    if len(pro.params) > len(args):
                        min = len(args)

                    for i in range(min):
                        if isinstance(pro.params[i], tuple):
                            name, type = pro.params[i]
                        else:
                            name, type = pro.params[i], ""

                        if type:
                            self.types[name] = type
                            
                        self.check_type(name, args[i])
                        self.variables[name] = args[i]

                for i in pro.body:
                    self.resolve(i)
            else:
                raise SyntaxError("procedure not fount")

    def get_string(self, val):
        if isinstance(val, token):
            return val.string_
        if val is not None:
            return str(val)
        else:
            return ""
