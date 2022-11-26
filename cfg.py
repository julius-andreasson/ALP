### Settings ###
datawidth = 8           # The width (in bits) of the "data" field on the MCU. 
debug = True            # 
default_path = "file"   # The default path used for both reading and writing, if no other is specified.
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
flag_dict = {}
flag_index = 0