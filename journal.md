#### Day 1
Began working on the interpreter today. Began by writing out what words in the code should be lexed to-- all the tokens needed. pseudocode.pro is saving me.

Update- finished working on the tokens list, there's a lot of keywords :skull. I didn't use re from python since I read somewhere that it led to harder-to-show interpreting errors.

Next, I need to map the words to the words using a dictionary. After that, I think I need to come up with a way of reading the file itself. This means browsing through all of the words in the file, and tokenizing them using the dictionary and then, if I have understood everything properly, construct an abstract syntax tree (AST) to represent the structure of the code. Extrapolating further, we need to evaluate the AST. Again, given I am understanding everything properly, we need to, well, turn this into kind-of a python file, which can be run. The other option is to do the interpreter myself, which is more challenging, but this is what I have thought of right now. If I have time, I may do that too. The other option is more alluring, to be honest. Haha!

#### Day 2
Spent today working out a barely-working system that translated the words identified into those in my list of tokens. Next, I need to include acceptability even when things aren't separated by space. eg- "if Index < 3" and "if Index<3"

#### Day 3
Spent today working on yesterday's problem- "Index<3" not being registered individually. Took a long time to fix that, but works better now!

#### Day idk
Found a lot of things new, especially about regular expressions, or regex. Will probably overwrite a lot of the code with it since I have just realized it's potential.
Update- regex is kind of tiring to understand and write. Moreover, I think I am going to stick with my own code for now unless the need for regex comes up again. I used it now because it helped me in classifying tokens as real numbers.

#### Day idk + 1
I think tokenizer is done, since I can't think of anything else to tokenize right now (may change in the future). Beginning work on the parser now!
Update- I'm going to implement top-down parsing. A top-down parser goes from left, and try a "production rule" (an if-else statement). if the rule fails, the steps are reversed, and another rule is implemented. (Could try lookahead, but seems complicated). The type of parser I'm going to implement is called the recursive descent parser. If I want to expand the scope of the project, I could also try using an LL(1) parser which uses a parsing table, but they seem very complicated based on the geeksforgeeks article I read, but that's future me to worry about!
Initially, the parser will read the code left to right, and built an abstract syntax tree based on that. It uses a global pointer which tracks the current position of the cursor, upon which the abstract syntax tree is built upon.

#### Day idk + 2
Began work on the parser. Spent like 15-20 minutes re-writing the tokenizer's class identifier names. Only after completion did I realize I can import the class and then make use of .type, since I had already broken each token into its type.

#### Day idk + 3
Finished more helper functions, which are functions which make it easy for my parser to build an AST and run things. It has things such as looking at the next token, previous token, seeing if the current token is the first/last, matching a token and a tokentype inputted etc. Next, I also began building (I don't know what it is called) functions which take in the token and then return the important things from each token set. A token set is a set of tokens to do something united such as- if loops, while loops, print statements etc. By returning the needed things from each token set, a map can be built to show how to take the needed things from each set, and actually translating it into python code. I've finished 3 functions for now- 
the declaration function (DECLARE x : integer)
the output function (OUTPUT "hello world")
the input function (INPUT x)

#### Day idk + 4
Finished more functions-
while loops
subroutine calls
assignments
+ made the output function better

#### Day idk + 5
Forgot to journal yday
I began to implement pratt parsing, but then felt that to be too... eh? So I tried coming up with my own method using priority additions. Began implementing that today, but I'm kinda (very) unsure about this abstract syntax tree stuff and how to do things using it. 
The priority addition thing works by keeping all tokens in a straight line with equal priority, and if it encounters a + or a * etc, it gives them a priority, which pushes them higher up the AST. it follows pemdas. After the AST is organized, I need to break it down and evaluate it, which I know how to do in my head, but I don't know how to implement it due to my lack of knowledge of AST.
Current update on my method- what the program does is, for something like 2 + 3 * 4, it looks at the priority. * has more priority than +, so it looks at things immediately to the left and right, giving you 3 and 4. Now, the token * is replaced by 3 * 4, and the tokens 3 and 4 are removed. 