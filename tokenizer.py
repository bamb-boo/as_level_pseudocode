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
    mod_operate = 13 # MOD
    div_operate = 14 # DIV
    eql = 15 # =
    less = 16 # <
    less_eql = 17 # ≤
    more = 18 # >
    more_eql = 19 # ≥
    not_eql = 20 # <>
    arrow = 21 # <- or ←

    integer = 22
    real = 23
    char = 24
    string = 25
    boolean = 26
    date = 27
    array = 28

    declare = 29 # done
    constant = 30 # done
    identifier = 31 # done
    newline = 32 # done

    and_ = 33
    not_ = 34
    or_ = 35

    if_ = 36 # done
    then_ = 37 # done
    else_ = 38 # done
    endif_ = 39 # done

    for_ = 40 # done
    to_ = 41 # done
    step_ = 42 # done
    next_ = 43 # done

    while_ = 44 # done
    do_ = 45 # done
    endwhile = 46 # done

    repeat_ = 47 # done
    until_ = 48 # done

    case = 49 # done
    of = 50 # done
    otherwise = 51 # done
    endcase = 52 # done

    input_ = 53 # done
    output_ = 54 # done

    procedure_ = 55
    endprocedure_ = 56

    call_ = 57 # done

    function_ = 58
    returns_ = 59
    return_ = 60
    endfunction_ = 61

    openfile = 62
    readfile = 63
    writefile = 64
    closefile = 65
    read = 66
    write = 67
    append = 68
    byref = 69
    byval = 70

    int_ = 71 # done
    rand = 72 # done
    length = 73 # done
    right = 74 # done
    mid = 75 # done
    lcase = 76 # done
    ucase = 77 # done

    type_ = 78
    endtype_ = 79
    set_ = 80
    define_ = 81
    caret = 82

    class_ = 83
    endclass_ = 84
    inherits = 85
    super_ = 86
    public_ = 87
    private_ = 88
    new_ = 89

    seek = 90
    getrecord = 91
    putrecord = 92

    dot = 93

    eof = 94


# class for tokens to hold data such as type, the value it holds, and if an error pops up, the line where it comes
class token:
    def __init__(self, type: tokentype, string_: str, literal, line: int):
        self.type = type
        self.string_ = string_
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"token({self.type.name}), value: {self.string_}, line = {self.line} \n"

    def tokenize(path):
        if path.lower().endswith(".pseudo"):
            with open(path, "r") as f:
                content = f.read()
            return content

def tokenize(path):
    if not path.lower().endswith(".pseudo"):
        raise ValueError("only .pseudo files are accepted")

    with open(path, "r") as f:
        content = f.read()
        
    # declaring some variables
    tokens = []
    spaces = []
    spacecheck = ""
    index = 0
    twolist = ["<-", "<>"] # reminder- the character "==" isn't in pseudocode
    onelist = ["(", ")", "[", "]", ",", "!", ":", "&", "+", "-", "*", "/", "^", "=", "<", ">", "≤", "≥", "←", "."]

    isint_ = re.compile(r'^[-+]?[0-9]+$')
    real_ = re.compile(r'[-+]?[0-9]*\.[0-9]{1,}$')
    str_ = re.compile(r'^[\s\S]*$')
    bool_ = ("false", "true")

    def is_date(date):
        try:
            datetime.datetime.strptime(date, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    # linking symbols with names and the dict's inverse)
    nospace = {"left_par" : "(", "right_par" : ")", "left_brkt" : "[", "right_brkt" : "]", "comma" : ",", "mark_exclam" :  "!", "colon" : ":","ampersand" : "&", "caret" : "^", "dot" : ".",
            "plus" : "+", "sub" : "-", "mul" : "*", "div" : "/", "mod_operate" : "mod", "div_operate" : "div", "eql" : "=", "less" : "<", "less_eql" : "≤", "more" : ">", "more_eql" : "≥", "not_eql" : "<>", "arrow" : "<-"}
    inv_nospace = {'(': 'left_par', ')': 'right_par', '[': 'left_brkt', ']': 'right_brkt', ',': 'comma', '!': 'mark_exclam', ':': 'colon', '&': 'ampersand', "^" : "caret", "." : "dot",
                '+': 'plus', '-': 'sub', '*': 'mul', '/': 'div', 'mod': 'mod_operate', 'div': 'div_operate', '=': 'eql', '<': 'less', '≤': 'less_eql', '>': 'more', '≥': 'more_eql', '<>': 'not_eql', '<-': 'arrow'}
    in_string = False

    file = content

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

        quotes = ["'", "'"]
        if file[index] in quotes:
            in_string = not in_string
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
                prev = (index > 0 and file[index - 1] == " ")
                next = (index < len(file) - 1 and file[index + 1] == " ")

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
                spacecheck = spacecheck + "\x00"
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
        tokens[k] = tokens[k].replace("\x00", " ")
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
                if list_inv_nospace[i] == tokens[k] and not is_date(tokens[k]):
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

            elif isint_.match(tokens[k]):
                tokens[k] = token(type = tokentype.integer, string_ = tokens[k], literal = int(tokens[k]), line = line)

            elif real_.match(tokens[k]):
                tokens[k] = token(type = tokentype.real, string_ = tokens[k], literal = float(tokens[k]), line = line)

            else:
                starts = ""
                for i in quotes:
                    if tokens[k].startswith(i):
                        starts = i
                        break

                ends = ""
                for i in quotes:
                    if tokens[k].endswith(i):
                        ends = i
                        break
                if starts == ends and starts != "":
                    if len(tokens[k]) == 3:
                        tokens[k] = token(type = tokentype.char, string_ = tokens[k], literal = tokens[k][1], line = line)
                    else:
                        tokens[k] = token(type = tokentype.string, string_ = tokens[k], literal = tokens[k][1:-1], line = line)

                elif tokens[k].lower() in bool_:
                    tokens[k] = token(type = tokentype.boolean, string_ = tokens[k], literal = tokens[k], line = line)

                elif is_date(tokens[k]):
                    tokens[k] = token(tokentype.date, string_ = tokens[k], literal = tokens[k], line = line)

                else:
                    tokens[k] = token(type = tokentype.identifier, string_ = tokens[k], literal = tokens[k], line = line)
                    
    tokens.append(token(type = tokentype.eof, string_ = "EOF", literal = None, line = line))

    print(tokens)
    return tokens

if __name__ == "__main__":
    path = r"C:\Users\sram7\Downloads\as_level_pseudocode-main\as_level_pseudocode-main\marks.pseudo"
    list = tokenize(path)
    print(list)