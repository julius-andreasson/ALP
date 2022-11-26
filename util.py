import cfg

### IO methods ###
def read_src(path):
    file = open(path, "r")
    src = file.read()
    file.close()
    return src

def write_code(path, code):
    path = path[:-4] # Remove .alp from end of path.
    file = open(path, "w")
    file.write(code)
    file.close()

def get_path():
    if cfg.debug:
        path = cfg.default_path
    else:
        path = input("Input .alp file name:")
    # Add .alp to end of path if it's not already there.
    path = "Files/" + path
    if path[-4] != ".alp":
        path += ".alp"
    return path

def print_info(src, code):
    print("Source code:")
    print("=====================")
    print(src)
    print("=====================")
    print("Compiled code:")
    print("=====================")
    print(code)
    print("=====================")

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
    cfg.label_index = 0 # Maybe this is a poor solution
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

'''Compiler main function
Written to be self-explanatory'''
def compile(block):
    block = remove_comments(block)
    block = collect_labels(block)
    block = replace_labels(block)
    block = replace_decimals(block)
    block = replace_instruction_names(block)
    return block