#### Day 1
Began working on the interpreter today. Began by writing out what words in the code should be lexed to-- all the tokens needed. pseudocode.pro is saving me.

Update- finished working on the tokens list, there's a lot of keywords :skull. I didn't use re from python since I read somewhere that it led to harder-to-show interpreting errors.

Next, I need to map the words to the words using a dictionary. After that, I think I need to come up with a way of reading the file itself. This means browsing through all of the words in the file, and tokenizing them using the dictionary and then, if I have understood everything properly, construct an abstract syntax tree (AST) to represent the structure of the code. Extrapolating further, we need to evaluate the AST. Again, given I am understanding everything properly, we need to, well, turn this into kind-of a python file, which can be run. The other option is to do the interpreter myself, which is more challenging, but this is what I have thought of right now. If I have time, I may do that too. The other option is more alluring, to be honest. Haha!

#### Day 2
Spent today working out a barely-working system that translated the words identified into those in my list of tokens. Next, I need to include acceptability even when things aren't separated by space. eg- "if Index < 3" and "if Index<3"
