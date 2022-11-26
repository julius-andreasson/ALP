import cfg

### Compiler utilities ###
'''Applies the function `f` to each line in `block`.'''
def for_each_line(block, f):
    out = ""
    for line in block.split('\n'):
        out = f(line, out)
    out = out[:-1] # Removes the final trailing '\n'.
    return out

def replace_using_dict(block, dict):
    for key in dict.keys():
        block = block.replace(key, dict[key])
    return block

def replace_instruction_names(block):
    return replace_using_dict(block, cfg.instruction_dict)

def replace_labels(block):
    return replace_using_dict(block, cfg.label_dict)

'''Adds jump codes to label_dict'''
def collect_labels(block):
    cfg.label_index = 0 # Todo: think of a solution which causes less coupling
    def f(line, out):
        if line[0:1] != "#":
            out += line + '\n'
            cfg.label_index += 1
        else:
            cfg.label_dict[line] = str(cfg.label_index)
        return out
    return for_each_line(block, f)

def remove_comments(block):
    def f(line, out):
        if line[0:2] != "//":
            out += line + '\n'
        return out
    return for_each_line(block, f)

def replace_decimals(block):
    def f(line, out):
        new = ""
        for word in line.split(" "):
            if word.isdigit():
                integer = int(word)
                binary = format(integer, 'b')
                #Add padding so that the binary number is always 8 bits long.
                while(len(binary) < cfg.datawidth):
                    binary = '0'+binary
                new += binary + " "
            else:
                new += word + " "
        new = new[:-1] # Remove final trailing whitespace.
        out += new + "\n"
        return out
    return for_each_line(block, f)

def format_to_hex(block):
    dicte = {" R0 ": "0", " R1 ": "1"}
    block = replace_using_dict(block, dicte)
    def fu(line, out):
        i = int(line, 2) #convert binary string to int
        h = hex(i)[2:] #convert int to hex and cut off '0x' part.
        h = h.upper()
        while(len(h)<4):
            h = "0"+h
        return out + h +";\n"
    block = for_each_line(block, fu)
    block += "\n"
    while (block.count("\n") < 64):
        block += "0000;\n"
    return block

'''Compiler main function
Written to be self-explanatory'''
def compile(block):
    block = remove_comments(block)
    block = collect_labels(block)
    block = replace_labels(block)
    block = replace_decimals(block)
    block = replace_instruction_names(block)
    block = format_to_hex(block)
    return block