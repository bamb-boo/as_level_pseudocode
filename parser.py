import re
from enum import StrEnum
from tokenizer import token, tokentype

class parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def beginning(self):
        if self.current == 0:
            return True
        else:
            return False
    
    def end(self):
        if self.current >= len(self.tokens):
            return True
        else:
            if self.tokens[self.current].type == tokentype.eof:
                return True
            else:
                return False
            
    def previous(self):
        if self.beginning() == True:
            return self.tokens[0]
        return self.tokens[self.current - 1]
        
    def next(self):
        if self.end() == False:
            self.current = self.current + 1
        return self.previous()


    def check(self, token_type):
        if self.end() == False:
            if self.tokens[self.current].type == token_type:
                return True
            return False
        else:
            return False

    def match(self, *token_type):
        for i in token_type:
            if self.check(i) == True:
                self.next()
                return True
        return False

    def consume(self, token_type):
        if self.check(token_type):
            return self.next()

        raise SyntaxError(f"line {self.tokens[self.current].line}- got {self.tokens[self.current].string_}")

    def get_statement(self):
        # add more as i code more parsing rules
        if self.check(tokentype.declare):
            return self.declaration()
        elif self.check(tokentype.constant_):
            return self.constant()
        elif self.check(tokentype.output_):
            return self.output_statement()
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
        elif self.check(tokentype.identifier):
            return self.assignment()
        elif self.check(tokentype.call_):
            return self.call_subroutine()

    # to DECLARE    
    def declaration(self):
        self.consume(tokentype.declare)
        var = self.consume(tokentype.identifier)
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
    
    # to ASSIGN a CONSTANT
    def constant(self):
        self.consume(tokentype.constant_)
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
        var = self.consume(tokentype.identifier)
        if self.consume(tokentype.arrow):
            return Assignment(var.string_, self.next().string_)
        else:
            raise SyntaxError("nothing to assign to")

    # to OUTPUT    
    def output_statement(self):
        self.consume(tokentype.output_)
        branch = []
        while True:
            if self.tokens[self.current].string_ != "\n":
                x = self.next()
                if x.string_ != ",":
                    branch.append(x.string_)
            else:
                break

        return Output(branch)
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

class expression:
    def __init__(self, token_type, value, priority = 0):
        self.type = token_type
        self.value = value
        self.priority = priority
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"{self.value}"
    
def priority(tokens):

    base = {
    tokentype.plus: 1,
    tokentype.sub: 1,

    tokentype.mul: 2,
    tokentype.div: 2,

    tokentype.pow: 3
    }

    nodes = []
    current = 0

    for i in tokens:
        if i.type == tokentype.left_brkt:
            current = current + 4
        elif i.type == tokentype.right_brkt:
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
        return nodes[0].value

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

        combined = expression(left = left.value, right = right.value, high = high.value)
        high.value = combined
        high.priority = 0
        high.prev = left.prev

        if left.prev:
            left.prev.next = high

        high.next = right.next
        if right.next:
            right.next.prev = high

        nodes.remove(left)
        nodes.remove(right)

    return nodes[0].value
        
