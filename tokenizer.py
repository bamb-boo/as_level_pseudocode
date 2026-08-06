# importing libs
import os
import re
from enum import Enum, unique
import datetime

#setting up class for tokens
@unique
class tokentype(Enum):
    left_par = 1 # (
    right_par = 2 # )
    left_brkt = 3 # [
    right_brkt = 4 # ]
    comma = 5 # ,
    mark_exclam = 6 # !
    colon = 7 # :
    ampersand = 8 # &

    plus = 9 # +
    sub = 10 # -
    mul = 11 # *
    div = 12 # /
    pow = 13 # ^
    mod_operate = 14 # MOD
    div_operate = 15 # DIV
    eql = 16 # =
    less = 17 # <
    less_eql = 18 # ≤
    more = 19 # >
    more_eql = 20 # ≥
    not_eql = 21 # <>
    arrow = 22 # <- or ←

    integer = 23
    real = 24
    char = 25
    string = 26
    boolean = 27
    date = 28
    array = 29

    declare = 30
    constant = 31
    identifier = 32
    newline = 33

    and_ = 34
    not_ = 35
    or_ = 36

    if_ = 37
    then_ = 38
    else_ = 39
    endif_ = 40

    for_ = 41
    to_ = 42
    step_ = 43
    next_ = 44

    while_ = 45
    do_ = 46
    endwhile = 47

    repeat_ = 48
    until_ = 49

    case = 50
    of = 51
    otherwise = 52
    endcase = 53

    input_ = 54
    output_ = 55

    procedure_ = 56
    endprocedure_ = 57

    call_ = 58
    function_ = 59
    returns_ = 60
    return_ = 61
    endfunction_ = 62

    openfile = 63
    readfile = 64
    writefile = 65
    closefile = 66
    read = 67
    write = 68
    append = 69
    byref = 70
    byval = 71
    eof = 72


# class for tokens to hold data such as type, the value it holds, and if an error pops up, the line where it comes
class token:
    def __init__(self, type: tokentype, string_: str, literal, line: int):
        self.type = type
        self.string_ = string_
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"token({self.type.name}), value: {self.string_}, line = {self.line} \n"


# declaring some variables
tokens = []
spaces = []
spacecheck = ""
index = 0
twolist = ["<-", "<>"] # reminder- the character "==" isn't in pseudocode
onelist = ["(", ")", "[", "]", ",", "!", ":", "&", "+", "-", "*", "/", "^", "=", "<", ">", "≤", "≥", "←"]

int_ = re.compile(r'^[-+]?[0-9]+$')
real_ = re.compile(r'[-+]?[0-9]*\.[0-9]{1,}$')
str_ = re.compile(r'^[\s\S]*$')
bool_ = ("FALSE", "TRUE")
def is_date(date):
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        return False

# linking symbols with names and the dict's inverse)
nospace = {"left_par" : "(", "right_par" : ")", "left_brkt" : "[", "right_brkt" : "]", "comma" : ",", "mark_exclam" :  "!", "colon" : ":","ampersand" : "&",
           "plus" : "+", "sub" : "-", "mul" : "*", "div" : "/", "pow" : "^", "mod_operate" : "mod", "div_operate" : "div", "eql" : "=", "less" : "<", "less_eql" : "≤", "more" : ">", "more_eql" : "≥", "not_eql" : "<>", "arrow" : "<-"}
inv_nospace = {'(': 'left_par', ')': 'right_par', '[': 'left_brkt', ']': 'right_brkt', ',': 'comma', '!': 'mark_exclam', ':': 'colon', '&': 'ampersand',
            '+': 'plus', '-': 'sub', '*': 'mul', '/': 'div', '^': 'pow', 'mod': 'mod_operate', 'div': 'div_operate', '=': 'eql', '<': 'less', '≤': 'less_eql', '>': 'more', '≥': 'more_eql', '<>': 'not_eql', '<-': 'arrow'}
in_string = False

file = 'DECLARE name : STRING \n name <- "Alice" \n IF index = 2 THEN \n status <- "passed" \n ENDIF' # test string

# checking for number of newlines in the file to know which line an error popped up in by using arrays to store the location of the newline and the current line
number_newline = 1
newlines = []
for i in range(len(file)):
    if file[i] == "\n":
        array = []
        number_newline = number_newline + 1
        array.append(number_newline)
        array.append(i)
        newlines.append(array)

token_index = 0

# forward and backward searching to see if "<>" can be confused as something else
while index < len(file):
    if file[index] == "\n":
        spacecheck = spacecheck + " \n "
        index = index + 1
        continue

    if file[index:index + 2] == "//":
        while index < len(file) and file[index] != "\n":
            index = index + 1
        continue

    if file[index] == "'" or file[index] == "\"":
        if in_string == False:
            in_string = True
            spacecheck = spacecheck + file[index]
            index = index + 1
        else:
            in_string = False
            spacecheck = spacecheck + file[index]
            index = index + 1
        continue

    if in_string == False:    
        if index + 1 < len(file) and file[index:index + 2] in twolist:
            prev = (file[index - 1] == " ")
            next = (file[index + 2] == " ")

            spacecheck = spacecheck + f" {file[index:index + 2]} "
            index = index + 2

            if prev and next:
                token_index = token_index + 2
            elif prev or next:
                token_index = token_index + 1
            

        elif file[index] in onelist:
            prev = (file[index - 1] == " ")
            next = (file[index + 1] == " ")

            spacecheck = spacecheck + f" {file[index]} "
            index = index + 1

            if prev and next:
                token_index = token_index + 2
            elif prev or next:
                token_index = token_index + 1

        else:
            if file[index] == " ":
                token_index = token_index + 1
            spacecheck = spacecheck + file[index]
            index = index + 1
            
    else:
        if file[index] == " ":
            spaces.append(token_index)
            spacecheck = spacecheck + "s"
        else:
            spacecheck = spacecheck + file[index]
        index = index + 1


while "  " in spacecheck:
    spacecheck = spacecheck.replace("  ", " ")

file = spacecheck

# slices strings
i_ = 0
token_place = []

for j in range(len(file)):
    if file[j] == " ":
        tokens.append(file[i_:j])
        token_place.append(i_)
        i_ = j + 1
    elif j == len(file) - 1:
        tokens.append(file[i_:j + 1])
        token_place.append(i_)
        i_ = j + 1

print(tokens)

# cleans for empty lines
cleaned = []
cleaned_pos = []

for i in range(len(tokens)):
    if tokens[i] != "":
        cleaned.append(tokens[i])
        cleaned_pos.append(token_place[i])

tokens = cleaned
token_place = cleaned_pos

# checking for things such as "input_" which have an underscore because they are also python keywords (note- because of consistency, even things which are not py keywords but are in a category of others which are py keywords have underscores.)
underscore = []
for i in tokentype.__members__:
    if i.endswith("_"):
        underscore.append(i[:-1])

# beeg thing
for k in range(len(tokens)):
    ltoken = tokens[k].lower()
    if ltoken in underscore:
        ltoken = f"{ltoken}_"

    # checking for arrows (may be redundant. old code)
    matched = False
    if tokens[k] == "<-" or tokens[k] == "←":
        matched = True
        name = "arrow" # number 22

    else:
        # same thing as the other underscore thing, but that was for the names, and this is for the tokens from the file
        if tokens[k] in underscore:
            tokens[k] = f"{tokens[k]}_"

        # to set the names for direct matches
        for j in tokentype.__members__:
            if j == ltoken:
                matched = True
                name = j
                break

        # to see if the given token is a symbol
        # changing it into a list for easier workability
        list_inv_nospace = list(inv_nospace)
        for i in range(len(list_inv_nospace)):
            if list_inv_nospace[i] == tokens[k]:
                matched = True
                name = inv_nospace[list_inv_nospace[i]]
                break

    line = 1
    for i in newlines:
        if token_place[k] > i[1]:
            line = i[0]


    # if it has been matched, then give it it's attributes
    if matched == True:
        obj = tokentype[name]
        tokens[k] = token(type = obj, string_ = tokens[k], literal = tokens[k], line = line)
    elif matched == False:
        if tokens[k] == "\n":
            tokens[k] = token(type = tokentype.newline, string_ = "\\n", literal = None, line = line)

        elif int_.match(tokens[k]):
            tokens[k] = token(type = tokentype.integer, string_ = tokens[k], literal = int(tokens[k]), line = line)

        elif real_.match(tokens[k]):
            tokens[k] = token(type = tokentype.real, string_ = tokens[k], literal = float(tokens[k]), line = line)
        # is it a string?
        elif ((tokens[k].startswith('"') and tokens[k].endswith('"')) or (tokens[k].startswith("'") and tokens[k].endswith("'"))) and len(tokens[k]) == 3:
            tokens[k] = token(type = tokentype.char, string_ = tokens[k], literal = tokens[k], line = line)

        elif (tokens[k].startswith('"') and tokens[k].endswith('"')) or (tokens[k].startswith("'") and tokens[k].endswith("'")):
            tokens[k] = token(type = tokentype.string, string_ = tokens[k], literal = tokens[k], line = line)

        elif tokens[k].lower() in bool_:
            tokens[k] = token(type = tokentype.boolean, string_ = tokens[k], literal = tokens[k], line = line)

        elif is_date(tokens[k]):
            tokens[k] = token(tokentype.date, string_ = tokens[k], literal = tokens[k], line = line)

        else:
            tokens[k] = token(type = tokentype.identifier, string_ = tokens[k], literal = tokens[k], line = line)
            
tokens.append(token(type = tokentype.eof, string_ = "EOF", literal = None, line = line))

print(tokens)