from tokenizer import tokenize
from parser import parser
from interpreter import interpreter

def run(path):
    ''' tokens = tokenize(path)
    print(tokens)

    parsed = parser(tokens)
    print(parsed)

    asttree = parsed.parse()
    print(asttree)
    interpreted = interpreter(asttree)
    interpreted.run()
    '''
    tokens = tokenize(path)

    parsed = parser(tokens)
    print("BEFORE PARSE")
    asttree = parsed.parse()
    print("AFTER PARSE")

    print("AST:")
    print(asttree)

    interpreted = interpreter(asttree)

    print("VARIABLES BEFORE:")
    print(interpreted.variables)

    interpreted.run()

    print("VARIABLES AFTER:")
    print(interpreted.variables)
if __name__ == "__main__":
    run("marks.pseudo")
