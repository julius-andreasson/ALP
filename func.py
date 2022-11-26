import cfg

### Functions ###
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

def print_info(alp, code):
    print("Pre-compilation code:")
    print("=====================")
    print(alp)
    print("=====================")
    print("Post-compilation code:")
    print("=====================")
    print(code)
    print("=====================")

def compile(block):
    block = remove_comments(block)
    block = replace_instruction_names(block)
    return block

def remove_comments(block):
    out = ""
    for line in block.split("\n"):
        if line[0:2] != "//":
            out += line + "\n"
    out = out[:-2] # Removes the final '\n', so that there isn't a trailing newline in the output.
    return out

def replace_instruction_names(block):
    for key in cfg.instruction_dict.keys():
        block = block.replace(key, cfg.instruction_dict[key])
    return block

def get_path():
    if cfg.debug:
        path = cfg.default_path
    else:
        path = input("Input .alp file name:")
    # Add .alp to end of path if it's not already there.
    if path[-4] != ".alp":
        path += ".alp"
    return path