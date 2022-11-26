instruction_dict = {
    "CALL"  : "0000",
    "RET"   : "0001",
    "BZ"    : "0010",
    "B"     : "0011",
    "ADD"   : "0100",
    "SUB"   : "0101",
    "LD"    : "0110",
    "IN"    : "0111",
    "OUT"   : "1000",
    "AND"   : "1001"
}

def read_asm(path):
    file = open(path, "r")
    asm = file.read()
    file.close()
    return asm

def write_code(path, code):
    file = open(path, "w")
    file.write(code)
    file.close()

def print_info(asm, code):
    print("Pre-compilation code:")
    print("=====================")
    print(asm)
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
    for key in instruction_dict.keys():
        block = block.replace(key, instruction_dict[key])
    return block

# actual execution
path = "file"
asm = read_asm(path+".alp")
code = compile(asm)
write_code(path, code)
print_info(asm, code)