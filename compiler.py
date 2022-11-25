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

def get_asm(s):
    asm_file = open(s, "r")
    asm = asm_file.read()
    asm_file.close()
    return asm

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

asm = get_asm("file.asm")
code = compile(asm)

print("Pre-compilation code:")
print("=====================")
print(asm)
print("=====================")
print("Post-compilation code:")
print("=====================")
print(code)
print("=====================")