import cfg

### IO methods ###
def read_alp(path):
    file = open(path, "r")
    alp = file.read()
    file.close()
    return alp

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

def print_info(alp, code):
    print("Pre-compilation code:")
    print("=====================")
    print(alp)
    print("=====================")
    print("Post-compilation code:")
    print("=====================")
    print(code)
    print("=====================")

### Compiler utilities ###
'''Applies the function `f` to each line in `block`.'''
def for_each_line(f, block):
    out = ""
    for line in block.split('\n'):
        out = f(line, out)
    out = out[:-1] # Removes the final trailing '\n'.
    return out

def remove_comments(block):
    def f(line, out):
        if line[0:2] != "//":
            out += line + '\n'
        return out
    return for_each_line(f, block)

def replace_decimals(block):
    def f(line, out):
        new = ""
        for word in line.split(" "):
            if word.isdigit():
                integer = int(word)
                binary = format(integer, 'b')
                while(len(binary) < cfg.datawidth):
                    binary = '0'+binary
                new += binary + " "
            else:
                new += word + " "
        new = new[:-1] # Remove final trailing whitespace.
        out += new + "\n"
        return out
    return for_each_line(f, block)

def replace_instruction_names(block):
    for key in cfg.instruction_dict.keys():
        block = block.replace(key, cfg.instruction_dict[key])
    return block

### Compiler main function ###
def compile(block):
    block = remove_comments(block)
    # block = replace_flags(block) #todo
    block = replace_decimals(block)
    block = replace_instruction_names(block)
    return block