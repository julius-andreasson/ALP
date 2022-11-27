import cfg
import re
### Compiler utilities ###
'''Applies the function `f` to each line in `block`.'''


def for_each_line(block, f):
    out = ""
    for line in block.split('\n'):
        out = f(line, out)
    out = out[:-1]  # Removes the final trailing '\n'.
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
    cfg.label_index = 0  # Todo: think of a solution which causes less coupling

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
                # Add padding so that the binary number is always 8 bits long.
                while (len(binary) < cfg.datawidth):
                    binary = '0' + binary
                new += binary + " "
            else:
                new += word + " "
        new = new[:-1]  # Remove final trailing whitespace.
        out += new + "\n"
        return out

    return for_each_line(block, f)


def format_to_hex(block):
    register_dict = {  # The register and their binary codes.
        " R0 ": "0",
        " R1 ": "1"
    }
    block = replace_using_dict(block, register_dict)

    def fu(line, out):
        i = int(line, 2)  # convert binary string to int
        h = hex(i)[2:]  # convert int to hex and cut off '0x' part.
        h = h.upper()
        while len(h) < 4:
            h = "0" + h
        return out + h + ";\n"

    block = for_each_line(block, fu)
    block += "\n"
    while block.count("\n") < 64:
        block += "0000;\n"
    return block


'''Compiler main function
Written to be self-explanatory'''


def compile(block):
    #block = remove_comments(block)
    #block = collect_labels(block)
    #block = replace_labels(block)
    #block = replace_decimals(block)
    #block = replace_instruction_names(block)
    #block = format_to_hex(block)

    return Compiler(block).result()


class Compiler:
    def __init__(self, source_code: str):
        self.__src_code = source_code
        self.__processed_code = source_code

        self.__finished_processing = False
        self.__labels = {  # Lambdas as values to be lazy
            "BEGIN": 0,
            "END": lambda: self.__lines_of_code(),
        }
        self.__compile()

    def __compile(self):
        self._remove_comments()
        self.__collect_and_remove_labels()

        self.__replace_labels()
        self.__decimal_to_binary()
        self.__replace_instruction_codes_and_registers()
        self._to_hex()
        self._pad_with_zeros()

        self.__finished_processing = True

    def __lines_of_code(self) -> int:
        return len(self.__processed_lines())

    def _remove_comments(self):
        # Remove totally blank rows.
        self.__processed_code = re.sub("(//).*\n", "", self.__processed_code)

    def __processed_lines(self) -> list[str]:
        return self.__processed_code.split("\n")

    def __collect_and_remove_labels(self):
        new = list()
        found = 0
        for (i, row) in enumerate(self.__processed_lines()):
            if row[0] == "#":
                self.__labels[re.findall("\A#+\w*", row)[0][1:]] = i - found  # This makes it be the
                found += 1
                # correct row even tho labels are removed
            else:
                new.append(row)
        self.__processed_code = "\n".join(new)

    def result(self):
        assert self.__finished_processing
        return self.__processed_code

    def __replace_labels(self):
        for label, index in self.__labels.items():
            def label_value(label_val):
                if isinstance(label_val, int):
                    return label_val
                else:
                    return label_val()
            self.__processed_code = re.sub("#"+label, str(label_value(index)), self.__processed_code)

    def __replace_instruction_codes_and_registers(self):
        for op, to in cfg.instruction_dict.items():
            # Only matches if op is first on the row and has blackspace right after.
            self.__processed_code = re.sub("(\n|\A)" + op + " ", "\n" + to + " ", self.__processed_code)
        for reg, to in cfg.register_dict.items():
            self.__processed_code = re.sub(" "+reg+" ", " " + to + " ", self.__processed_code)

    def __decimal_to_binary(self):
        def f(line):
            new = ""
            for word in line.split(" "):
                if word.isdigit():
                    integer = int(word)
                    binary = format(integer, 'b')
                    # Add padding so that the binary number is always 8 bits long.
                    while (len(binary) < cfg.datawidth):
                        binary = '0' + binary
                    new += binary + " "
                else:
                    new += word + " "
            return new[:-1]  # Remove final trailing whitespace.

        self.__processed_code = "\n".join(map(f, self.__processed_lines()))

    def _to_hex(self):
        def fu(line: str):
            if line:  # Shouldn't be needed
                line = line.replace(" ", "")
                i = int(str(line), 2)  # convert binary string to int
                h = hex(i)[2:]  # convert int to hex and cut off '0x' part.
                h = h.upper()
                while len(h) < 4:
                    h = "0" + h
                return h + ";"
            return ""
        self.__processed_code = "\n".join(l for l in map(fu, self.__processed_lines()))

    def _pad_with_zeros(self):
        self.__processed_code += "\n"
        while self.__processed_code.count("\n") < 64:
            self.__processed_code += cfg.nothing + ";\n"