dict = {
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

text = """CALL 0 2
//comment
AND 0 04"""

def compile(block):
    block = remove_comments(block)
    block = replace_instruction_names(block)
    return block

def replace_instruction_names(block):
    for key in dict.keys():
        block = block.replace(key, dict[key])
    return block

def remove_comments(block):
    out = ""
    for line in block.split("\n"):
        if line[0:2] != "//":
            out += line + "\n"
    return out


print("Pre-compilation code:")
print(text)
print("Post-compilation code:")
print(compile(text))