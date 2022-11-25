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
AND 0 04"""

def compile(block):
    for key in dict.keys():
        block = block.replace(key, dict[key])
    return block

print("Pre-compilation code:")
print(text)
print("Post-compilation code:")
print(compile(text))