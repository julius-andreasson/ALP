### Settings ###
datawidth = 8           # The width (in bits) of the "data" field on the MCU.
debug = True            #
default_path = "file"   # The default path used for both reading and writing, if no other is specified.
instruction_dict = {
    "CALL"  : "0000",
    "RET"   : "0001",
    "BZ"    : "0010",
    "B": "0011",
    "SUB"   : "0101",   # SUB has to be checked before B, otherwise the B in SUB will be replaced by the code of B
    "ADD"   : "0100",
    "LD"    : "0110",
    "IN"    : "0111",
    "OUT"   : "1000",
    "AND"   : "1001"
}

register_dict = {  # The register and their binary codes.
    "R0": "0",
    "R1": "1"
}

nothing = "0000" # What to pad with

label_dict = {}
label_index = 0