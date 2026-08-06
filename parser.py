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
        elif self.check(tokentype.output_):
            return self.output_statement()
        elif self.check(tokentype.input_):
            return self.input_statement
        elif self.check(tokentype.if_):
            return self.if_loop
        elif self.check(tokentype.identifier):
            return self.assignment
        
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

    def assignment(self):
        var = self.consume(tokentype.identifier)
        if self.consume(tokentype.arrow):
            return Assignment(var.string_, self.next().string_)
        else:
            raise SyntaxError("nothing to assign to")
            
    def output_statement(self):
        self.consume(tokentype.output_)
        return Output(self.next().string_)

    def input_statement(self):
        self.consume(tokentype.input_)
        return Input(self.next().string_)

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
                    else_loop.append(self.get_statement)

        self.consume(tokentype.endif_)
        return If_loop(condition, branch, else_loop)
