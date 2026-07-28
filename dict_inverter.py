nospace = {"left_par" : "(", "right_par" : ")", "left_brkt" : "[", "right_brkt" : "]", "comma" : ",", "mark_exclam" :  "!", "colon" : ":","ampersand" : "&",
           "plus" : "+", "sub" : "-", "mul" : "*", "div" : "/", "pow" : "^", "mod_operate" : "MOD", "div_operate" : "DIV", "eql" : "=", "less" : "<", "less_eql" : "≤", "more" : ">", "more_eql" : "≥", "not_eql" : "<>", "arrow" : "<-"}
invdict = {v: k for k, v in nospace.items()}
print(invdict)
