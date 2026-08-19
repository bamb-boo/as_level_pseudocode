helper functions-

beginning-> to see if the current token is at the start
end-> to see if the current token is at the end
previous-> to see the previous token
next-> to see the next token
check-> to see if a token is of a specified datatype
match-> cycles through the provided token types, and if the current token is one of those types, then it advances
consume-> if the current token is of a specified datatype, return the next token 


parsing rules-
declaration (done)
assignment (done)

output (done)
input (done)

if (done)
while (done)
repeat (done)
for (done)

add (done)
sub (done)
mul (done)
div (done)
pow (done)
mod
div

and
or
not

eql
less
less_eql
more
more_eql
not_eql

pratt parsing-
main question- what is expected to be seen to the left of the token-
left denotation (led)
null denotation (nud)

only ned-
integers, reals, literals
variables
unary (-5 etc)

update- never mind, i'm not going to use pratt parsing. i'm going to try and implement a method i thought of myself.