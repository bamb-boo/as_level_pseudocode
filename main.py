from tokenizer import tokenize
from parser import parser
from interpreter import interpreter
import sys

def run(path):
    tokens = tokenize(path)

    parsed = parser(tokens)

    asttree = parsed.parse()
    interpreted = interpreter(asttree)
    interpreted.run()
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        runn = sys.argv[1]
    else:
        runn = "examples/example2.pseudo"
    run(runn)