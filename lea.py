import os, sys
import re

def replace_strings_with_index(newArg):
    strings_list = []
    index = 0

    def replace(match):
        nonlocal index
        string = match.group()
        strings_list.append(string)
        index += 1
        return f"$$$STR[{index - 1}]$$$"

    # Regular expression pattern to match strings enclosed in single or double quotes
    pattern = r'(["\'])(?:(?=(\\?))\2.)*?\1'

    replaced_arg = re.sub(pattern, replace, newArg)
    return replaced_arg, strings_list
def replace_index_with_strings(replaced_arg, strings_list):
    def replace(match):
        index = int(match.group(1))
        return strings_list[index]

    pattern = r'\$\$\$STR\[(\d+)\]\$\$\$'
    original_arg = re.sub(pattern, replace, replaced_arg)
    return original_arg

class gl:
    vars = {}
    stdfunctions = [
        'echo', 'tostring', 'input'
    ]
    #name[str] = [dict] -> {to_parse[list], args[list]}
    functions = {

    }
    IfJump = 0

class Regex:
    def increment(match):
        number = int(match.group(1))
        incremented = number + 1
        return str(incremented)
    def decrement(match):
        number = int(match.group(1))
        decremented = number - 1
        return str(decremented)
    def len(match):
        str_ = match.group(1)
        return str(len(str_))
    def nlen(match):
        num = match.group(1)
        return str(len(str(num)))
    def strindex(match):
        string, index = match.group(1), match.group(2)
        try:
            index = int(index)
        except:
            err(f"Index must be int")
        isin = False
        for i in range(0, len(string)):
            if i == index:
                isin = not isin
                break
        if isin:
            char = string[i]
            if char not in "'\"":
                return f"\"{char}\""
            else:
                if char == "'": return "\"'\""
                else: return "\"\\\"\""
        else:
            if index == -1:
                char = string[::-1]
                return f"\"{char}\""
            else:
                err("Index out of range")
def err(m, noErrExit=False):
    print(m)
    if not noErrExit:
        sys.exit(0)

def evaluate(arg, line, noErrExit=False):
    for var in gl.vars:
        value = ""

        if gl.vars[var] == "True" or gl.vars[var] == "False":
            value = gl.vars[var]
        elif isinstance(gl.vars[var], int) or isinstance(gl.vars[var], float):
            value = str(gl.vars[var])
        elif isinstance(gl.vars[var], list):
            value = str(gl.vars[var])
        else:
            value = f"\"{gl.vars[var]}\""

        if isinstance(value, str):
            try:
                int(value)
                value = f"{value}"
            except:
                pass
            
        arg = arg.replace(f'$"{var}"', value)
        arg = arg.replace(f"$'{var}'", value)

    invalid_variable = re.search(r'\$"(.*?)"', arg)
    invalid_variable2 = re.search(r'\$"(.*?)"', arg)

    if invalid_variable:
        arg = arg.replace(f'$"{invalid_variable.group(1)}"', "None")
    if invalid_variable2:
        arg = arg.replace(f'$"{invalid_variable2.group(1)}"', "None")

    while True:
        for function in gl.stdfunctions:
            function_call = re.search(fr'{function}(.*?)\/{function}', arg)
            if function_call:
                if function == "echo":
                    a = evaluate(function_call.group(1), line)
                    if isinstance(eval(str(a)), str):
                        a = eval(a)
                    print(a)
                    arg = arg.replace(f"echo{function_call.group(1)}/echo", "")
                if function == "input":
                    input_ = input(evaluate(function_call.group(1), line))
                    try: 
                        input_ = eval(input_)
                        arg = arg.replace(f"input{function_call.group(1)}/input", '"\'' + str(input_) + '\'"')
                    except:
                        arg = arg.replace(f"input{function_call.group(1)}/input", '"' + input_ + '"')
                if function == "tostring":
                    a = evaluate(function_call.group(1), line)
    
                    try:
                        a = eval(a)
                    except:
                        if isinstance(a, str):
                            arg = arg.replace(f"tostring{function_call.group(1)}/tostring", '"' + str(a) + '"')
                        else:
                            arg = arg.replace(f"tostring{function_call.group(1)}/tostring", '"\'' + str(a) + '\'"')
                    
                    if isinstance(a, str):
                        arg = arg.replace(f"tostring{function_call.group(1)}/tostring", '"' + str(a) + '"')
                    else:
                        arg = arg.replace(f"tostring{function_call.group(1)}/tostring", '"\'' + str(a) + '\'"')
        funcall = 0
        for function in gl.stdfunctions:
            function_call = re.search(fr'{function}(.*?)\/{function}', arg)
            if function_call:
                funcall += 1
        if funcall == 0: break

    while True:
        for function in gl.functions:
            function_call = re.search(fr'{function}(.*?)\/{function}', arg)
            if function_call:
                toparse = gl.functions[function][0]
                args = gl.functions[function][1]
                return_ = None

                rcontent = content = function_call.group(1)

                content = function_call.group(1).strip()
                content, strings = replace_strings_with_index(content)

                content = [evaluate(replace_index_with_strings(i, strings), line, noErrExit) for i in content.split(',')]
                
                if len(content) == len(args):
                    pass
                else:
                    err(f"Lea: at line {line}: for function call '{function}': expected {len(args)} arguments but got {len(content)}")

                index = 0
                for i in args:
                    gl.vars[i] = content[index]
                    index += 1
                return_ = parse(toparse, noErrExit, line)
                arg = arg.replace(f"{function}{rcontent}/{function}", str(evaluate(str(return_), line, noErrExit)))

        funcall = 0
        for function in gl.functions:
            function_call = re.search(fr'{function}(.*?)\/{function}', arg)
            if function_call:
                funcall += 1
        if funcall == 0: break

    arg = re.sub(r"(\d+)\+\+", Regex.increment, arg)
    arg = re.sub(r"(\d+)\-\-", Regex.decrement, arg)
    arg = re.sub(r'"((?:[^"\\]|\\.)*?)"(?!(?:[^"\\]|\\)")\.len', Regex.len, arg)
    arg = re.sub(r"'((?:[^'\\]|\\.)*?)'(?!(?:[^'\\]|\\)')\.len", Regex.len, arg)
    arg = re.sub(r'(\d+).len', Regex.nlen, arg)
    arg = re.sub(r'"(.*?)"\[(.*?)\]', Regex.strindex, arg)
    arg = re.sub(r'\'(.*?)\'\[(.*?)\]', Regex.strindex, arg)

    inc_match = re.search(r"(\d+)\+\+", arg)
    dec_match = re.search(r"(\d+)\-\-", arg)
    len_match = re.search(r'"((?:[^"\\]|\\.)*?)"(?!(?:[^"\\]|\\)")\.len', arg)
    len_match2 = re.search(r"'((?:[^'\\]|\\.)*?)'(?!(?:[^'\\]|\\)')\.len", arg)
    nlen_match = re.search(r'(\d+).len', arg)
    sin_match = re.search(r'"(.*?)"\[(.*?)\]', arg)
    sin_match2 = re.search(r'\'(.*?)\'\[(.*?)\]', arg)

    if inc_match: arg = evaluate(arg, line)
    if dec_match: arg = evaluate(arg, line)
    if len_match: arg = evaluate(arg, line)
    if len_match2: arg = evaluate(arg, line)
    if nlen_match: arg = evaluate(arg, line)
    if sin_match: arg = evaluate(arg, line)
    if sin_match2: arg = evaluate(arg, line)

    if str(arg).replace(" ", "") == "":
        return ""
    
    try:
        arg = eval(str(arg))
        if isinstance(arg, str):
            return f"'{arg}'"
        if arg == True:
            return 1
        if arg == False:
            return 0
        return arg
    except:
        err(f"On line {line}: invalid syntax '{arg}'", noErrExit)
        return ""

def parse(arg, noErrExit=False, lindex=0):
    skip_ = 0
    index = -1
    for line in arg:
        line = line.strip()

        index += 1
        lindex += 1

        if skip_ != 0:
            skip_ -= 1
            continue
        if len(line.replace(" ", "")) == 0:
            continue
        if line[0] == "#":
            continue

        line, strings = replace_strings_with_index(line)

        if ';;' in line:
            line = line.split(';;')
            line = [replace_index_with_strings(i, strings) for i in line]
            lline = len(line)
            rest = arg[index+1:len(arg)]
            line += rest
            parse(line, noErrExit, lindex-lline+1)
            break

        line = replace_index_with_strings(line, strings)

        if line[0] == '"' or line[0] == "'":
            line, strings = replace_strings_with_index(line)
            if line[0:len("$$$STR[0]$$$:")].replace(" ", "") == "$$$STR[0]$$$:":
                name = strings[0][1:len(strings[0])-1]

                value = line[len("$$$STR[0]$$$:"):len(line)].strip()
                value = replace_index_with_strings(value, strings)

                value = evaluate(value, lindex, noErrExit)
                try:
                    value = eval(value)
                except:
                    pass
                gl.vars[name] = value
        elif line[0:len("if")] == "if":
            line, strings = replace_strings_with_index(line)

            try:
                condition = replace_index_with_strings(line[len("if"):line.index("??")], strings).strip()
            except:
                err(f"Lea: at line {lindex}: Invalid syntax '{replace_index_with_strings(line, strings)}'")
            
            block = arg[index+1:len(arg)]
            ifstatements = 1
            in_ = 0

            for i in block:
                if i.strip()[0:len('if')] == "if":
                    ifstatements += 1
                if i.strip().replace(" ", "") == f"/if":
                    ifstatements -= 1
                    if ifstatements == 0:
                        break
                in_ += 1

            block = block[0:in_]
            skip_ += len(block)

            if evaluate(condition, lindex, noErrExit) == 1:
                output = parse(block, noErrExit, lindex)
                if output != None:
                    return output

        elif line[0:len('/if')] == '/if':
            continue
        elif line[0:len("loop")] == "loop":
            line, strings = replace_strings_with_index(line)

            try:
                condition = replace_index_with_strings(line[len("loop"):line.index("??")], strings).strip()
            except:
                err(f"Lea: at line {lindex}: Invalid syntax '{replace_index_with_strings(line, strings)}'")
            
            block = arg[index+1:len(arg)]
            loopstatements = 1
            in_ = 0

            for i in block:
                if i.strip()[0:len("loop")] == "loop":
                    loopstatements += 1
                if i.strip().replace(" ", "") == f"/loop":
                    break
                in_ += 1

            block = block[0:in_]
            skip_ += len(block)

            try:
                while evaluate(condition, lindex, noErrExit) == 1:
                    output = parse(block, noErrExit, lindex)
                    if output != None:
                        return output
                    if evaluate(condition, lindex, noErrExit) != 1:
                        break
            except KeyboardInterrupt:
                err(f"Lea: at line {lindex}: Loop force exited by ^C")

        elif line[0:len('/loop')] == '/loop':
            continue
        elif line[0:len("function")] == "function":
            line, strings = replace_strings_with_index(line)

            try:
                name = replace_index_with_strings(line[len("function"):line.index("??")], strings).strip()
                args = line[line.index("??")+2:len(line)].strip().split(',')
                args = [eval(replace_index_with_strings(i, strings)) for i in args]
            except:
                err(f"Lea: at line {lindex}: Invalid syntax '{replace_index_with_strings(line, strings)}'")
            
            for i in " \t()[]{}*&^%$#@!-=+*/":
                if i in name:
                    err(f"Lea: at line {lindex}: invalid function name '{name}'")

            block = arg[index+1:len(arg)]
            functionstatement = 1
            in_ = 0

            for i in block:
                if i.strip()[0:len("functions")] == "functions":
                    functionstatement += 1
                if i.strip().replace(" ", "") == f"/function":
                    functionstatement -= 1
                    if functionstatement == 0:
                        break
                in_ += 1

            block = block[0:in_]
            skip_ += len(block)

            gl.functions[name] = [block, args]

        elif line[0:len('/function')] == '/function':
            continue
        elif line[0:len('return')] == 'return':
            if "/return" in line:
                return evaluate(line[len("return"):line.index("/return")].strip(), lindex, noErrExit)
            else:
                err(f"Lea: at line {lindex}: return statement isn't ended by '/return'")
        else:
            a = evaluate(line, lindex, noErrExit)
try:
    file = open(sys.argv[1], 'r').read().split('\n')
except:
    if len(sys.argv) == 1:
        try:
            print("Lea Shell")
            while True:
                input_ = input(">>>")
                parse([input_], True)

        except KeyboardInterrupt:
            sys.exit(0)
    err("Invalid File")

parse(file)