from tokenizer import tokenize
from parser import parser
from interpreter import interpreter

def run(path):
    tokens = tokenize(path)

    parsed = parser(tokens)

    asttree = parsed.parse()
    interpreted = interpreter(asttree)
    interpreted.run()
    
if __name__ == "__main__":
    run("marks.pseudo")
