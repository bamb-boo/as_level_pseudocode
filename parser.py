from tokenizer import token, tokentype


class parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def begin(self):
        if self.current == 0:
            istrue = True
        else:
            istrue = False
        return istrue
    
    def end(self):
        istrue = self.current >= len(self.tokens)
        return istrue
    
    def next(self):
        if self.end() == False:
            self.current = self.current + 1
        return self.tokens[self.current]

    def previous(self):
        if self.begin() == False:
            return self.tokens[self.current - 1]

    def check(self, token_type):
        if self.end() == False:
            if self.tokens[self.current].type == token_type:
                return True
            return False

    def match(self, tokentype):
        for i in tokentype:
            if self.check(i):
                self.current = self.current + 1
                return True
        return False