import cfg
import re
### Compiler utilities ###
'''Applies the function `f` to each line in `block`.'''


class bcolors:
    """TAKEN FROM https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


'''Compiler main function
Written to be self-explanatory'''


def compile(block):
    return Compiler(block).result()


class Compiler:
    base_labels = {  # Lambdas as values to be lazy, this is done in __init__
            "BEGIN": 0,
            "END": 0,
        }

    def __init__(self, source_code: str):
        self.__src_code = source_code
        self.__processed_code = source_code.strip()

        self.__finished_processing = False
        self.__labels = {  # Lambdas as values to be lazy
            "BEGIN": 0,
            "END": lambda: self.__lines_of_code(),
        }

        self.__processed_line_number_to_src = {i: i for i in range(source_code.count("\n")+1)}
        self.__compile()

    def __compile(self):
        self._remove_comments()
        self.__collect_and_remove_labels()
        #self.__create_warnings()
        self.__replace_constants()
        self.__replace_labels()
        self.__decimal_to_binary()
        self.__replace_instruction_codes_and_registers()
        self._to_hex()
        #self._pad_with_zeros()

        self.__finished_processing = True

    def __create_warnings(self):
        for (i, line) in enumerate(self.__processed_lines()):

            if len(line.strip().split(" ")) != 3:
                self.__warn(i, "There is an incorrect number of words on this line, All rows should have 3 words!")

    def __warn(self, index: int, message: str):
        def get_line() -> str:
            source_line = self.processed_line_number_to_src(index)
            print(self.__processed_line_number_to_src)
            print(source_line, index, self.__processed_lines()[index])
            return self.__src_code.split('\n')[source_line]

        warning = bcolors.WARNING
        warning += f"""WARNING ON LINE {bcolors.UNDERLINE}{index}{bcolors.ENDC}{bcolors.WARNING}: {message}
             LINE: {bcolors.ENDC}{bcolors.UNDERLINE}"{get_line()}"{bcolors.ENDC}
        """
        warning += bcolors.ENDC
        print(warning)

    def __lines_of_code(self) -> int:
        return len(self.__processed_lines())

    def _remove_comments(self):
        # Remove totally blank rows.
        new = []
        current_index = 0
        for (i, line) in enumerate(self.__processed_lines()):
            _line = re.sub("(//).*", "", line)
            if _line != "":
                new.append(_line)
                self.__processed_line_number_to_src[current_index] = self.__processed_line_number_to_src[i]
                current_index += 1

        self.__processed_code = "\n".join(new)

    def __processed_lines(self) -> list[str]:
        return [l for l in self.__processed_code.split("\n") if len(l) > 0]

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
                self.__processed_line_number_to_src[len(new)] = self.__processed_line_number_to_src[i+found]
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
        def f(line: str) -> str:
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
        self.__processed_code = self.__processed_code.replace("b", "")
        def fu(line: str) -> str:
            if line:  # Shouldn't be needed
                print(line)
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

    def processed_line_number_to_src(self, index: int):
        return self.__processed_line_number_to_src[index]

    def __replace_constants(self):

        for const in re.findall("(CONST\s*(\w+)\s*=\s*(\d+))" , self.__processed_code):
            # CONST x 500 on a line gives "x 500"

            self.__processed_code = self.__processed_code.replace(const[0], "")

            assert const[1] not in cfg.instruction_dict and const[1] not in cfg.register_dict

            self.__processed_code = self.__processed_code.replace(const[1], const[2])