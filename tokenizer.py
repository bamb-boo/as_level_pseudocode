import os
import re
from enum import Enum, unique

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


class token:
    def __init__(self, type: tokentype, string_: str, literal, line: int):
        self.type = type
        self.string_ = string_
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"token({self.type.name}), value = {self.string_}, line = {self.line} \n"

tokens = []

file = "DECLARE index<3 " # test string


number_newline = 1
for i in file:
    if i == "\n":
        number_newline = number_newline + 1


spacecheck = ""
index = 0
twolist = ["<-", "<>"]
onelist = ["(", ")", "[", "]", ",", "!", ":", "&", "+", "-", "*", "/", "^", "=", "<", ">", "≤", "≥", "←"]

while index < len(file):
    if index + 1 < len(file) and file[index:index + 2] in twolist:
        spacecheck = spacecheck + f" {file[index:index + 2]} "
        index = index + 2
    elif file[index] in onelist:
        spacecheck = spacecheck + f" {file[index]} "
        index = index + 1
    else:
        spacecheck = spacecheck + file[index]
        index = index + 1

while "  " in spacecheck:
    spacecheck = spacecheck.replace("  ", " ")

file = spacecheck

i_ = 0
for j in range(len(file)):
    if file[j] == " ":
        tokens.append(file[i_:j].lower())
        i_ = j + 1
    elif file[j] == file[::-1][0] and j == len(file) - 1:
        tokens.append(file[i_:j + 1].lower())
        i_ = j + 1
print(tokens)


underscore = []
for i in tokentype.__members__:
    if i.endswith("_"):
        underscore.append(i[:-1])

nospace = {"left_par" : "(", "right_par" : ")", "left_brkt" : "[", "right_brkt" : "]", "comma" : ",", "mark_exclam" :  "!", "colon" : ":","ampersand" : "&",
           "plus" : "+", "sub" : "-", "mul" : "*", "div" : "/", "pow" : "^", "mod_operate" : "mod", "div_operate" : "div", "eql" : "=", "less" : "<", "less_eql" : "≤", "more" : ">", "more_eql" : "≥", "not_eql" : "<>", "arrow" : "<-"}
inv_nospace = {'(': 'left_par', ')': 'right_par', '[': 'left_brkt', ']': 'right_brkt', ',': 'comma', '!': 'mark_exclam', ':': 'colon', '&': 'ampersand',
            '+': 'plus', '-': 'sub', '*': 'mul', '/': 'div', '^': 'pow', 'mod': 'mod_operate', 'div': 'div_operate', '=': 'eql', '<': 'less', '≤': 'less_eql', '>': 'more', '≥': 'more_eql', '<>': 'not_eql', '<-': 'arrow'}


for k in range(len(tokens)):
    matched = False
    if tokens[k] == "<-" or tokens[k] == "←":
        matched = True
        name = "arrow" # number 22
    else:
        if tokens[k] in underscore:
            tokens[k] = f"{tokens[k]}_"
        for j in tokentype.__members__:
            if j == tokens[k]:
                matched = True
                name = j
                break

        list_inv_nospace = list(inv_nospace)
        for i in range(len(list_inv_nospace)):
            if list_inv_nospace[i] == tokens[k]:
                matched = True
                name = inv_nospace[list_inv_nospace[i]]
                break

    if matched == True:
        obj = tokentype[name]
        tokens[k] = token(type = obj, string_ = tokens[k], literal = tokens[k], line = number_newline)
    elif matched == False:
        if tokens[k].isdigit() == True:
            tokens[k] = token(type=tokentype.integer, string_ = tokens[k], literal = int(tokens[k]), line = number_newline)
        else:
            tokens[k] = token(type=tokentype.identifier, string_ = tokens[k], literal = tokens[k], line = number_newline)

print(tokens)