# importing libs
import re
from enum import StrEnum
import random as r
from tokenizer import token, tokentype

class Declaration:
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype

class Arraydeclare:
    def __init__(self, name, datatype, dimensions):
        self.name = name
        self.datatype = datatype
        self.dimensions = dimensions

class Constant:
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype

class Assignment:
    def __init__(self, var, branch, indices = None):
        self.var = var
        self.branch = branch
        if indices is not None:
            self.indices = indices
        else:
            self.indices = []

class Output:
    def __init__(self, branch):
        self.branch = branch

class Input:
    def __init__(self, var):
        self.var = var

class If_loop:
    def __init__(self, condition, branch, else_loop):
        self.condition = condition
        self.branch = branch
        self.else_loop = else_loop

class While_loop:
    def __init__(self, condition, branch):
        self.condition = condition
        self.branch = branch

class For_loop:
    def __init__(self, index, value1, value2, step, branch):
        self.index = index
        self.value1 = value1
        self.value2 = value2
        self.step = step
        self.branch = branch

class Repeat_loop:
    def __init__(self, branch, condition):
        self.branch = branch
        self.condition = condition

class CaseOf:
    def __init__(self, identifier, branch):
        self.identifier = identifier
        self.branch = branch

class Call:
    def __init__(self, subroutine, parameters):
        self.subroutine = subroutine
        self.parameters = parameters
        
class Length:
    def __init__(self, str_branch):
        self.str_branch = str_branch

class Integer:
    def __init__(self, branch):
        self.branch = branch

class Random:
    def __init__(self, var):
        self.var = var

class Right:
    def __init__(self, var, length):
        self.var = var
        self.length = length

class Mid:
    def __init__(self, var, place, length):
        self.var = var
        self.place = place
        self.length = length

class Lcase:
    def __init__(self, var):
        self.var = var

class Ucase:
    def __init__(self, var):
        self.var = var

class Function_def:
    def __init__(self, var, returning, body):
        self.var = var
        self.returning = returning
        self.body = body

class parser:
    # properties of self
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # defining helper functions to reduce code length and to make it easier
    # helper function to see if analysis has begun/current token is the 1st (or 0th) token
    def beginning(self):
        if self.current == 0:
            return True
        else:
            return False

    # helper function to see if the current token is the last token, which is eof (first line is to see if the current token is greater than the number of tokens)
    def end(self):
        if self.current >= len(self.tokens):
            return True
        else:
            if self.tokens[self.current].type == tokentype.eof:
                return True
            else:
                return False

    # helper function to get the prior token
    def previous(self):
        if self.beginning() == True:
            return self.tokens[0]
        return self.tokens[self.current - 1]

    # helper function to get the next token after reading it and advancing
    def next(self):
        token = self.tokens[self.current]
        if not self.end():
            self.current = self.current + 1
        return token

    # helper function to check if the token is of a certain datatype without advancing
    def check(self, token_type):
        if self.current < len(self.tokens):
            return self.tokens[self.current].type == token_type
        return False

    # helper function to check if the token is of a datatype and advances if it matches
    def match(self, *token_type):
        for i in token_type:
            if self.check(i) == True:
                self.next()
                return True
        return False

    # consumes the next token
    def consume(self, token_type):
        if self.check(token_type):
            return self.next()

        raise SyntaxError(f"line {self.tokens[self.current].line}- got {self.tokens[self.current].string_}")

    # to use the functions declares later on such as declare, if_loop etc. this will be used in the interpreter later on
    def get_statement(self):
        # add more as i code more parsing rules
        if self.check(tokentype.declare):
            return self.declaration()
        elif self.check(tokentype.constant):
            return self.constant()
        elif self.check(tokentype.output_):
            return self.output_statement()
        elif self.check(tokentype.identifier):
            return self.assignment()
        elif self.check(tokentype.input_):
            return self.input_statement()
        elif self.check(tokentype.if_):
            return self.if_loop()
        elif self.check(tokentype.while_):
            return self.while_loop()
        elif self.check(tokentype.for_):
            return self.for_loop()
        elif self.check(tokentype.repeat_):
            return self.repeat_loop()
        elif self.check(tokentype.case):
            return self.case_of()
        elif self.check(tokentype.call_):
            return self.call_subroutine()
        elif self.check(tokentype.length):
            return self.length_()
        elif self.check(tokentype.integer):
            return self.integer_()
        elif self.check(tokentype.rand):
            return self.rand_()
        elif self.check(tokentype.right):
            return self.right_()
        elif self.check(tokentype.mid):
            return self.mid_()
        elif self.check(tokentype.lcase):
            return self.lcase_()
        elif self.check(tokentype.ucase):
            return self.ucase_()
        elif self.check(tokentype.function_):
            return self.function__()
        else:
            self.next()
            return None

    def parse(self):
        nodes = []
        while not self.end():
            if self.check(tokentype.newline):
                self.next()
                continue

            value = self.get_statement()
            if value is not None:
                nodes.append(value)
        return nodes
    
    # to DECLARE    
    def declaration(self):
        self.next()  
        var = self.tokens[self.current]
        self.next()
        
        if self.check(tokentype.colon):
            self.next()

        if self.check(tokentype.array):
            self.consume(tokentype.array)
            self.consume(tokentype.left_brkt)
            dimensions = []
            low = int(self.consume(tokentype.integer).string_)
            self.consume(tokentype.colon)
            up = int(self.consume(tokentype.integer).string_)
            dimensions.append(low)
            dimensions.append(up)

            if self.check(tokentype.comma):
                self.consume(tokentype.comma)
                lower = int(self.consume(tokentype.integer).string_)
                self.consume(tokentype.colon)
                upper = int(self.consume(tokentype.integer).string_)
                dimensions.append(lower)
                dimensions.append(upper)

            self.consume(tokentype.right_brkt)
            self.consume(tokentype.of)
            datatype = self.tokens[self.current]

            '''while True:
                low = int(self.consume(tokentype.integer).string_)
                self.consume(tokentype.colon)
                up = int(self.consume(tokentype.integer).string_)
                dimensions.append(low)
                dimensions.append(up)
                if self.check(tokentype.comma):
                    self.consume(tokentype.comma)
                else:
                    break'''

            self.next()
            return Arraydeclare(var, datatype, dimensions)

        datatype = self.tokens[self.current]
        self.next()
        return Declaration(var, datatype)
    '''
    def declaration(self):
        self.consume(tokentype.declare)
        var = self.tokens[self.current]
        self.consume(tokentype.colon)

        if self.match(tokentype.integer):
            datatype = "integer"
        elif self.match(tokentype.real):
            datatype = "real"
        elif self.match(tokentype.char):
            datatype = "char"
        elif self.match(tokentype.string):
            datatype = "string"
        elif self.match(tokentype.boolean):
            datatype = "boolean"
        elif self.match(tokentype.date):
            datatype = "date"

        else:
            raise SyntaxError("no datatype provided")

        return Declaration(var.string_, datatype)
        '''
    
    # to ASSIGN a CONSTANT
    def constant(self):
        self.consume(tokentype.constant)
        var = self.consume(tokentype.identifier)
        self.consume(tokentype.arrow)

        if self.match(tokentype.integer):
            datatype = "integer"
        elif self.match(tokentype.real):
            datatype = "real"
        elif self.match(tokentype.char):
            datatype = "char"
        elif self.match(tokentype.string):
            datatype = "string"
        elif self.match(tokentype.boolean):
            datatype = "boolean"
        elif self.match(tokentype.date):
            datatype = "date"
        else:
            raise SyntaxError("no datatype provided")
        
        return Constant(var.string_, datatype)
    
    # to ASSIGN    
    def assignment(self):
        # var = self.consume(tokentype.identifier)
        var = self.tokens[self.current]
        self.next()

        if self.check(tokentype.arrow):
            self.next()

        indices = []
        if self.check(tokentype.left_brkt):
            self.consume(tokentype.left_brkt)
            indices.append(self.tokens[self.current])
            self.next()

            if self.check(tokentype.comma):
                self.consume(tokentype.comma)
                indices.append(self.tokens[self.current])
                self.next()

            self.consume(tokentype.right_brkt)

        branch = []
        while not self.check(tokentype.newline) and not self.check(tokentype.eof):
            branch.append(self.tokens[self.current])
            self.next()

        if len(branch) == 1:
            branch = branch[0]

        return Assignment(var, branch, indices = indices)
    
    # to OUTPUT    
    def output_statement(self):
        self.next()
        branch = []

        while not self.check(tokentype.newline) and not self.check(tokentype.eof):
            branch.append(self.tokens[self.current])
            self.next()

        if len(branch) == 1:
            branch = branch[0]

        return Output(branch)
    ''' while True:
        if self.tokens[self.current].string_ != "\n":
            x = self.next()
            if x.string_ != ",":
                branch.append(x.string_)
        else:
            break
    return Output(branch)'''

    # to INPUT
    def input_statement(self):
        self.consume(tokentype.input_)
        var = self.next().string_
        return Input(var)

    # for IF loops
    def if_loop(self):
        self.consume(tokentype.if_)
        condition_tokens = []
        InCondition = True

        while InCondition:
            if self.check(tokentype.then_):
                InCondition = False
            else:
                condition_tokens.append(self.next().string_)
        condition = " ".join(condition_tokens)
        self.consume(tokentype.then_)

        branch = []
        else_loop = None

        while not self.check(tokentype.endif_) and not self.check(tokentype.else_):
            branch.append(self.get_statement())

        if self.match(tokentype.else_):
            if self.check(tokentype.if_):
                else_loop = [self.if_loop()]
            else:
                else_loop = []
                while not self.check(tokentype.endif_):
                    else_loop.append(self.get_statement())

        self.consume(tokentype.endif_)
        return If_loop(condition, branch, else_loop)

    # for WHILE loops
    def while_loop(self):
        self.consume(tokentype.while_)
        condition_tokens = []
        InCondition = True

        while InCondition:
            if self.check(tokentype.do_):
                InCondition = False
            else:
                condition_tokens.append(self.next().string_)
        condition = " ".join(condition_tokens)
        self.consume(tokentype.do_)

        branch = []
        
        while not self.check(tokentype.endwhile):
            branch.append(self.get_statement())
        self.consume(tokentype.endwhile)
        return While_loop(condition, branch)

    # for FOR loops
    def for_loop(self):
        self.consume(tokentype.for_)
        index = self.consume(tokentype.identifier)
        self.consume(tokentype.arrow)
        value1 = self.consume(tokentype.integer)
        self.consume(tokentype.to_)
        value2 = self.consume(tokentype.integer)
        if self.match(tokentype.step_):
            step = self.next().string_
        else:
            step = "1"

        branch = []
        while not self.check(tokentype.next_):
            branch.append(self.get_statement())
        self.consume(tokentype.next_)
        if self.consume(tokentype.identifier).string_ != index.string_:
            raise SyntaxError("identifiers don't match")
        else:
            return For_loop(index.string_, value1.string_, value2.string_, step, branch)

    # for REPEAT...UNTIL loops
    def repeat_loop(self):
        self.consume(tokentype.repeat_)
        branch = []
        while not self.check(tokentype.until_):
            branch.append(self.get_statement())
        self.consume(tokentype.until_)
        condition_tokens = []
        while not self.check(tokentype.newline):
            condition_tokens.append(self.next().string_)
        condition = " ".join(condition_tokens)
        return Repeat_loop(branch, condition)

    # for CASE OF statements
    def case_of(self):
        usable = [tokentype.string, tokentype.char, tokentype.date, tokentype.integer, tokentype.real, tokentype.boolean, tokentype.identifier]
        self.consume(tokentype.case)
        self.consume(tokentype.of)
        identifier = self.consume(tokentype.identifier)
        branch = []
        while not self.end():
            if self.tokens[self.current].type in usable:
                sub_branch = []
                variable = self.next()
                self.consume(tokentype.colon)
                statement = self.get_statement()
                sub_branch.append(variable.string_)
                sub_branch.append(statement)
                branch.append(sub_branch)

            elif self.tokens[self.current].type == tokentype.otherwise:
                self.next()
                self.consume(tokentype.colon)
                sub_branch = []
                while not self.check(tokentype.endcase):
                    sub_branch.append(self.get_statement())
                branch.append("otherwise")
                branch.append(sub_branch)

            elif self.tokens[self.current].type == tokentype.endcase:
                self.next()
                break

        return CaseOf(identifier.string_, branch)

    # for things like CALL
    def call_subroutine(self):
        self.consume(tokentype.call_)
        subroutine = self.consume(tokentype.identifier)
        self.consume(tokentype.left_par)

        branch = []
        while True:
            if self.tokens[self.current].string_ != ")":
                x = self.next()
                if x.string_ != ",":
                    branch.append(x.string_)
            else:
                break
            
        self.consume(tokentype.right_par)
        parameters = " ".join(branch)

        return Call(subroutine.string_, parameters)

    def length_(self):
        self.consume(tokentype.length)
        self.consume(tokentype.left_par)
        branch = []
        i = 0
        while True:
            if self.tokens[self.current + i].type != tokentype.right_par:
                branch.append(self.tokens[self.current + i].string_)
                i = i + 1

            else:
                break
        self.current = self.current + (i + 1)
        str_branch = " ".join(branch)
        return Length(str_branch)

    def integer_(self):
        self.consume(tokentype.int_)
        self.consume(tokentype.left_par)
        branch = []
        while not self.check(tokentype.right_par) and not self.end():
            branch.append(self.next().string_)
        
        self.consume(tokentype.right_par)
        str_branch = " ".join(branch)
        return Integer(str_branch)

    def rand_(self):
        self.consume(tokentype.rand)
        self.consume(tokentype.left_par)
        var = int(self.consume(tokentype.integer).string_)
        self.consume(tokentype.right_par)
        return Random(var)

    def right_(self):
        self.consume(tokentype.right)
        self.consume(tokentype.left_par)
        var = self.next().string_
        self.consume(tokentype.comma)
        length = self.consume(tokentype.integer).string_
        self.consume(tokentype.right_par)
        return Right(var, length)

    def mid_(self):
        self.consume(tokentype.mid)
        self.consume(tokentype.left_par)
        var = self.next()
        self.consume(tokentype.comma)
        place = self.consume(tokentype.integer)
        self.consume(tokentype.comma)
        length = self.consume(tokentype.integer)
        self.consume(tokentype.right_par)
        return Mid(var, place, length)

    def lcase_(self):
        self.consume(tokentype.lcase)
        self.consume(tokentype.left_par)
        var = self.next()
        self.consume(tokentype.right_par)
        return Lcase(var)

    def ucase_(self):
        self.consume(tokentype.ucase)
        self.consume(tokentype.left_par)
        var = self.next()
        self.consume(tokentype.right_par)
        return Ucase(var)
    
    def function__(self):
        self.consume(tokentype.function_)
        var = self.consume(tokentype.identifier).string_
        params = []
        self.consume(tokentype.left_par)
        while True:
            if self.next().type != tokentype.right_par:
                params.append(self.next())
                self.consume(tokentype.colon)
                params.append(self.next())
                if self.next().type == tokentype.comma:
                    self.consume(tokentype.comma)
            else:
                break
        self.consume(tokentype.right_par)
        self.consume(tokentype.returns_)
        returning = self.consume(tokentype.identifier)
        body = []
        while not self.check(tokentype.endfunction_):
            if self.next().type == tokentype.newline:
                self.next()
                continue
            statement = self.get_statement()
            body.append(statement)
        self.consume(tokentype.endfunction_)
        return Function_def(var, returning, body)

    # def procedure__(self):

    # def 

# for math expressions
class expression:
    def __init__(self, token_type = None, value = None, priority = 0, left = None, right = None):
        self.type = token_type
        self.value = value
        self.priority = priority
        self.left = left
        self.right = right
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"{self.value}"

# priority for operations (PEMDAS)
def priority(tokens):

    base = {
    tokentype.plus: 1,
    tokentype.sub: 1,

    tokentype.mul: 2,
    tokentype.div: 2,

    tokentype.mod_operate: 2,
    tokentype.div_operate: 2
    }

    nodes = []
    current = 0
    for i in tokens:
        #adds priority for left bracket
        if i.type == tokentype.left_par:
            current = current + 4
        # subtracts priority for right bracket
        elif i.type == tokentype.right_par:
            current = current - 4
        elif i.type in base:
            priority = base[i.type] + current
            nodes.append(expression(i.type, i.string_, priority = priority))
        else:
            nodes.append(expression(i.type, i.string_, priority = 0))

    for i in range(len(nodes)):
        if i > 0:
            nodes[i].prev = nodes[i-1]
        if i < len(nodes) - 1:
            nodes[i].next = nodes[i + 1]

    return nodes

def calculate(nodes):
    if len(nodes) == 1:
        return nodes[0]

    while True:
        high = None
        max = 0

        # to get highest priority
        for i in nodes:
            if i.priority > max and i.priority > 0:
                max = i.priority
                high = i

        if high == None:
            break

        left = high.prev
        right = high.next

        if not left or not right:
            raise SyntaxError(f"incomplete expression near {high.value}")

        high.left = left
        high.right = right
        high.priority = 0
        high.prev = left.prev

        # main token has left token's value and right token's value
        if left.prev:
            left.prev.next = high

        high.next = right.next
        if right.next:
            right.next.prev = high

        # values of left and right are put into the main token, so left and right are not needed, and because of that, removed
        nodes.remove(left)
        nodes.remove(right)

    return nodes[0]
        
