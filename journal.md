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

#### Day idk + 6
Just realized I messed up a lot of functions-- some of them repeated, some of them from the syllabus weren't even in the list in tokenizer.py. Because of that, I had to re-write a lot of numbers. I would've completely torn down the list to arrange the functions group-wise to satisfy my brain, but that would've taken a minimum of 20 minutes which I didn't want to waste on such an unproductive thing. 
Right now, I never write comments, so it is hard for me to just look at a piece of code and realize what it does, and it's structure. In this project, the structure of a variable is very important because only the structure dictates how we can use and manipulate the variable. An example would be tokens[k]. Unless one knows the structure of tokens[k], realizing how to use it is quite hard. On smaller projects with less variables, it is easier to remember, but for this project, due to the number of variables, and the presence of similar variables (eg- int and int_. int is for integer while declaration and int_ is to convert a real into an integer.) makes it even more complicated. Also, it's hard to know what else to do due to the same reason-- there are too many functions to satisfy. I need to re-write the functions which I've taken care of in notes.md. 
The parser.py is quite a mess right now. I might need to update it and make it a bit more ordered before going to the actual interpretor, but that depends on time.
Things like LENGTH and RIGHT and UCASE need to be implemented.
Oh, and also I need a way to calculate expressions of equal priority and for more than 3 in a token.

#### Day idk + 7
Today was incredibly tiring. I had a lot of work at school, and work to do after coming back home too. Working on this project was quite more tiring since I'm kind of unsure how to proceed too... 
But today I just wrote a small function which will help me run a .pseudo file with the pseudocode gives it's file path. I was able to tokenize the code in the file, which was fun. Spent some time trying to find bugs and asking help from AI to help me find bugs. And then since it told me I had to write classes for each of the functions (functions such as DECLARE and ASSIGN etc) (note- I knew I had to do this, but forgot), so spent some time doing that.
Oh and also I just remembered- I meddled more with my expression parser to fix some stuff. 
I need to implement things like LENGTH and RIGHT and UCASE. Don't forget.

#### Day idk + 8
Today was quite good-- I wrapped up some functions. However, while writing those functions, I realized I needed a way to keep track of quotations, and because of that I also had to include quotation marks (' and "). Can't believe I didn't have them till now haha. Yeah, so after implementing the quotation marks, I also finished functions which required quotes such as UCASE, LCASE, MID, RIGHT etc. After completing that I jut added the new functions to their respective class (what I mentioned yesterday). After this, I'm *kind of* unsure what to do besides going to build the interpreter.
Update- I just remembered. I have to add all the functions to the get_statement() loop.

#### Day idk + 9
Haywire. I didn't know what to exactly do for the interpreter, so whipped up some code which may or may not work-- haven't tested it out yet. The interpreter is to look at the broken down tokens (from tokenizer.py) and, using the respective parsing function (in parser.py), to give the final output. This is the stage where all the action occurs. I didn't know how code the interpreter for functions like the loops, so I kept that aside. I also worked on coding the function in parser.py. I have an idea of how we can store all the body text, but my main worry is that things such as indentation may not be captured. Guess I need to test to find out! Indentation should be captured for things like loops. After coding the function, I tried to do the same for the procedure before realizing that a procedure can have either parameters or have no parameters at all. Because of that I need to verify the existence of paramters before proceeding further. May do that tomorrow.

#### Day idk + 10
Asked my cs teacher for some tips on how to improve and she suggested some changes which I implemented. 
Coded the loops in the interpreter. It was kind of challenging to implement them because of my vague understanding of classes, but I used help from my teacher to code it. 
Update- My teacher just made me realize that the self.check() function is in parser.py, and not here. I need to switch methods to identify datatype, or I need to see if I can use the same function.
Second update- teacher told me about the function isinstant(). I can use that to compare datatypes. 

#### Day idk + 11
Asked the help of my cs teacher again. Today was quite bad because I thought I finished it, and gave a simple 3 line code to test, but it didn't work at all. After trying to diagnoise the problem by myself for some time, I enlisted the help of AI. AI suggested multiple changes but none of them worked (I even tried different AIs but none of them were able to fix the problem). I've got work today, so I'm going to try a bit more tomorrow to find out the problem.
PS- for the reviewers, AI time took about 40 minutes of work.

#### Day idk + 12
*Very* relieving. The interpreter is working! I had to fix my helper functions, specifically next and check. Then spent some time playing with my interpreter-- trying random codes, before trying to find bugs. Found a couple or two. There was a problem with string outputting, so I changed that (before, if *x* was a string, then *x <- hi* worked, but only *x <- "hi"* is supposed to work.) I also began working on arrays. For arrays I used numpy to initialize arrays, which I don't think you can do in python natively since it can't store empty data. I don't know how I'll enable array access. Right now, I'm thinking of doing something along the lines of-- if var is an array, then python spits out the index of the array we want. If it's a 2-d array then we can use second-level access likewise. For the array declaration code, I initially made it accept n-d arrays, where n is an arbitrary integer, but then I realized that-
1. it is unnecessary (syllabus only has upto 2-d arrays)
2. array dimension entering and array accessing will be harder.
Of course, it could be a fun challenge to code and bypass the other two problems (I'm sure they can be solved), but I just don't want to invest time into thinking how it can be done. Right now my main priority is to finish arrays. After that, functiosn and procedures. 