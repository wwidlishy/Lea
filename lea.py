#TODO: Independence from pythons 'eval' function
import os, sys
import re

def find_substring_indexes(string, substring):
    indexes = []
    index = -1
    while True:
        # Find the next occurrence of the substring after the previous index
        index = string.find(substring, index + 1)
        if index == -1:
            break  # No more occurrences
        indexes.append(index)
    return indexes

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
        'echo', 'input', "type", "inc"
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
    def llen(match):
        lcontent = f"[{match.group(1)}]"
        return str(len(eval(str(lcontent))))
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

def evaluate(arg, line, noErrExit=False, fname=""):
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
            arg, strings = replace_strings_with_index(arg)
            while function in arg:
                if arg.count(function)/2 == arg.count(f"/{function}"):
                    ocontent = arg[arg.index(function)+len(function):len(arg)]
                    skip = ocontent.count(function)-ocontent.count(f"/{function}")

                    index = None

                    for i in find_substring_indexes(ocontent, f"/{function}"):
                        if skip == 0:
                            index = i
                            break
                        skip -= 1
                    
                    if index:
                        content = ocontent[0:index]
                    else:
                        err(f"Lea: at line {line}, file '{fname}': function's '{function}' arguments aren't properly enclosed")
                    arg = replace_index_with_strings(arg, strings)

                    ret = ""
                    content = replace_index_with_strings(content, strings)
                    parsed_content = str(evaluate(content, line, noErrExit, fname)).strip()

                    if function == 'echo':
                        print(eval(parsed_content))
                        pass
                    if function == 'input':
                        ret = f'"{input(eval(parsed_content))}"'
                    if function == 'type':
                        parsed_content = eval(parsed_content)
                        if isinstance(parsed_content, str):
                            ret = '"string"'
                        if isinstance(parsed_content, int) or isinstance(parsed_content, float):
                            ret = '"number"'
                        if isinstance(parsed_content, list):
                            ret = '"array"'
                    if function == "inc":
                        os.chdir(os.path.dirname(os.path.abspath(fname)))
                        if os.path.exists(eval(parsed_content)):
                            lib_file = open(eval(parsed_content), 'r').read().split('\n')
                            parse(lib_file, noErrExit, line, eval(parsed_content))
                            
                        else:
                            err(f"Lea: at line {line}, file {fname}: File '{eval(parsed_content)}' not found")
                    arg = arg.replace(f"{function}{replace_index_with_strings(content, strings)}/{function}", ret)

                else:
                    err(f"Lea: at line {line}, file '{fname}': function's '{function}' arguments aren't properly enclosed")
            arg = replace_index_with_strings(arg, strings)    

        funcall = 0
        for function in gl.stdfunctions:
            function_call = re.search(fr'{function}(.*?)\/{function}', arg)
            if function_call:
                funcall += 1
        if funcall == 0: break

    while True:
        for function in gl.functions:
            arg, strings = replace_strings_with_index(arg)
            while function in arg:
                if arg.count(function)/2 == arg.count(f"/{function}"):
                    ocontent = arg[arg.index(function)+len(function):len(arg)]
                    skip = ocontent.count(function)-ocontent.count(f"/{function}")

                    index = None

                    for i in find_substring_indexes(ocontent, f"/{function}"):
                        if skip == 0:
                            index = i
                            break
                        skip -= 1
                    
                    if index:
                        content = ocontent[0:index]
                    else:
                        err(f"Lea: at line {line}, file '{fname}': function's '{function}' arguments aren't properly enclosed")
                    arg = replace_index_with_strings(arg, strings)

                    ret = ""
                    content = replace_index_with_strings(content, strings)
                    parsed_content = str(evaluate(content, line, noErrExit, fname)).strip()
                    
                    toparse = gl.functions[function][0]
                    reqArgs = gl.functions[function][1]
                    
                    if parsed_content == '':
                        if reqArgs == ['']:
                            ret = str(parse(toparse, noErrExit, line, fname))
                            if ret == None:
                                ret = ""
                        else:
                            err(f"Lea: at line {line}, file '{fname}': Insufficient arguments")
                    elif isinstance(eval(parsed_content), tuple):
                        
                        if len(reqArgs) == len(eval(parsed_content)):
                            index = -1
                            for rarg in reqArgs:
                                index += 1
                                gl.vars[rarg] = eval(str(evaluate(str(eval(parsed_content)[index]), line, noErrExit, fname)))
                            ret = str(parse(toparse, noErrExit, line, fname))
                            if ret == None:
                                ret = ""

                        else:
                            err(f"Lea: at line {line}, file '{fname}': Insufficient arguments")
                    else:
                        if reqArgs != ['']:
                            if len(reqArgs) == 1:
                                gl.vars[reqArgs[0]] = eval(parsed_content)
                                ret = parse(toparse, noErrExit, line, fname)
                                if ret == None:
                                    ret = ""
                                
                            else:
                                err(f"Lea: at line {line}, file '{fname}': Insufficient arguments")
                        else:
                            if parsed_content == '':
                                parse(toparse, noErrExit, line, fname)
                            else:
                                err(f"Lea: at line {line}, file '{fname}': Insufficient arguments")

                    arg = arg.replace(f"{function}{replace_index_with_strings(content, strings)}/{function}", ret)

                else:
                    err(f"Lea: at line {line}, file '{fname}': function's '{function}' arguments aren't properly enclosed")
            arg = replace_index_with_strings(arg, strings)    

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
    arg = re.sub(r"\[(.*?)\]\.len", Regex.llen, arg)

    inc_match = re.search(r"(\d+)\+\+", arg)
    dec_match = re.search(r"(\d+)\-\-", arg)
    len_match = re.search(r'"((?:[^"\\]|\\.)*?)"(?!(?:[^"\\]|\\)")\.len', arg)
    len_match2 = re.search(r"'((?:[^'\\]|\\.)*?)'(?!(?:[^'\\]|\\)')\.len", arg)
    nlen_match = re.search(r'(\d+).len', arg)
    sin_match = re.search(r'"(.*?)"\[(.*?)\]', arg)
    sin_match2 = re.search(r'\'(.*?)\'\[(.*?)\]', arg)
    llen_match = re.search(r"\[(.*?)\]\.len", arg)

    if inc_match: arg = evaluate(arg, line, noErrExit, fname)
    if dec_match: arg = evaluate(arg, line, noErrExit, fname)
    if len_match: arg = evaluate(arg, line, noErrExit, fname)
    if llen_match: arg = evaluate(arg, line, noErrExit, fname)
    if nlen_match: arg = evaluate(arg, line, noErrExit, fname)
    if sin_match: arg = evaluate(arg, line, noErrExit, fname)
    if sin_match2: arg = evaluate(arg, line, noErrExit, fname)
    if llen_match: arg = evaluate(arg, line, noErrExit, fname)

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
        err(f"Lea: at line {line}, file '{fname}': invalid syntax '{arg}'", noErrExit)
        return ""

def parse(arg, noErrExit=False, lindex=0, fname=''):
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

                value = evaluate(value, lindex, noErrExit, fname)
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
                err(f"Lea: at line {lindex}, file '{fname}': Invalid syntax '{replace_index_with_strings(line, strings)}'")
            
            block = arg[index+1:len(arg)]
            ifstatements = 1
            in_ = 0

            for i in block:
                if i.strip()[0:len('if')] == "if":
                    ifstatements += 1
                if i.strip().replace(" ", "")[0:len("/if")] == f"/if":
                    ifstatements -= 1
                    if ifstatements == 0:
                        break
                in_ += 1

            block = block[0:in_]
            skip_ += len(block)

            if evaluate(condition, lindex, noErrExit, fname) == 1:
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
                err(f"Lea: at line {lindex}, file '{fname}': Invalid syntax '{replace_index_with_strings(line, strings)}'")
            
            block = arg[index+1:len(arg)]
            loopstatements = 1
            in_ = 0

            for i in block:
                if i.strip()[0:len("loop")] == "loop":
                    loopstatements += 1
                if i.strip().replace(" ", "")[0:len("/loop")] == f"/loop":
                    loopstatements -= 1
                    if loopstatements == 0: break
                in_ += 1

            block = block[0:in_]
            skip_ += len(block)

            try:
                while evaluate(condition, lindex, noErrExit, fname) == 1:
                    output = parse(block, noErrExit, lindex)
                    if output != None:
                        return output
                    if evaluate(condition, lindex, noErrExit, fname) != 1:
                        break
            except KeyboardInterrupt:
                err(f"Lea: at line {lindex}, file '{fname}': Loop force exited by ^C")

        elif line[0:len('/loop')] == '/loop':
            continue
        elif line[0:len("function")] == "function":
            line, strings = replace_strings_with_index(line)

            try:
                name = replace_index_with_strings(line[len("function"):line.index("??")], strings).strip()
                args = line[line.index("??")+2:len(line)].strip().split(',')
                if len(args) == 1 and args[0] == '':
                    pass
                else:
                    args = [eval(replace_index_with_strings(i, strings)) for i in args]
            except:
                err(f"Lea: at line {lindex}, file '{fname}': Invalid syntax '{replace_index_with_strings(line, strings)}'")
            
            for i in " \t()[]{}*&^%$#@!-=+*/":
                if i in name:
                    err(f"Lea: at line {lindex}, file '{fname}': invalid function name '{name}'")

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
                return evaluate(line[len("return"):line.index("/return")].strip(), lindex, noErrExit, fname)
            else:
                err(f"Lea: at line {lindex}, file '{fname}': return statement isn't ended by '/return'")
        else:
            a = evaluate(line, lindex, noErrExit, fname)
try:
    file = open(sys.argv[1], 'r', encoding='utf-8').read().split('\n')
except:
    if len(sys.argv) == 1:
        try:
            print("Lea Shell")
            while True:
                input_ = input(">>>")
                parse([input_], True, 0, '<stdin>')

        except KeyboardInterrupt:
            sys.exit(0)
    err("Invalid File")

parse(file)