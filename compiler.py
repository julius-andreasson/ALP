from pprint import pprint

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

while_loop = """
    IN R1 0
    SUB R1 G1
    BZ R1 #in11a //if 10
    B R1 #in11b //else
"""

if_cond = """IN R1 0
SUB R1 I1
BZ R1 #in11 //if 10
B R1 #out01 //else"""



def compile(block):
    return Compiler.compile(block)


class Compiler:
    base_labels = {  # Lambdas as values to be lazy, this is done in __init__
            "BEGIN": 0,
            "END": 0,
        }

    def __init__(self, source_code: str, labels: dict, lines_before: int = 0, pad=False):
        self.__src_code = source_code
        self.__processed_code = source_code.strip()

        self.__finished_processing = False
        if len(labels) == 0:
            self.__labels = {  # Lambdas as values to be lazy
                "BEGIN": 0,
                "END": lambda: self.__lines_of_code(),
            }
        else:
            self.__labels = labels
        self.label_offset = lines_before

        self.__processed_line_number_to_src = {i: i for i in range(source_code.count("\n")+1)}
        self.__compile(pad)

    def __compile(self, pad: bool):
        self._remove_comments()
        self.__replace_constants()

        self.__replace_if_statement()
        self.__replace_while_statement()
        self.__replace_delay()
        self.__replace_goto()

        self.__replace_minus_minus_plus_plus()
        #print(self.__processed_code)

        self.__collect_and_remove_labels()
        #self.__create_warnings()
        self.__allow_negation_of_binary()
        self.__replace_labels()
        self.__replace_ret()

        self.__decimal_to_binary()
        self.__replace_instruction_codes_and_registers()
        self.__binary_concatenation()
        print(self.__processed_code)
        self._to_hex()
        if pad:
            self._pad_with_zeros()

        self.__finished_processing = True

    @staticmethod
    def compile(code: str):
        return Compiler._compile(Compiler.remove_comments(Compiler.replace_constants(code)), {}, 0)[0]

    @staticmethod
    def _compile(code: str, labels:dict, line_offset=0):
        #print("______________________")
        if "{" in code and "}" in code and False: # THIS DOES NOT CURRENTLY WORK SO IS BLOCKED OFF WITH FALSE
            #print(code)

            start = code.find("{")
            end = code.rfind("}")
            pre = code[:start]
            post = code[end+1:]
            middle = code[start+1:end]
            #print("PRE " + pre)
            #print("POST " +post )
            #print("MIDDLE " + middle)

            if end == -1:
                raise ValueError("There is an unclosed bracket!")
            precode, labels = Compiler(pre, labels, line_offset)._result()
            postcode, labels = Compiler(post, labels, end + line_offset)._result()

            result = list()
            result.append(precode)
            #print(precode)
            middle_code, labels = Compiler._compile(middle, labels, start + line_offset)

            #print(middle_code)
            #print(postcode)

            if middle_code:
                result.append("\n" + middle_code)
            if postcode:
                result.append("\n" + postcode)
            return "".join(result), {}
        else:
            #print("NO BRACKET")
            res, l = Compiler(code, labels, line_offset, pad=True)._result()
            #print("INTERNAL " + res)
            return res, l

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
        self.__processed_code = Compiler.remove_comments(self.__processed_code)

    @staticmethod
    def remove_comments(code: str) -> str:
        # Remove totally blank rows.
        new = []
        current_index = 0
        for (i, line) in enumerate(code.split("\n")):
            _line = re.sub("(//).*", "", line)
            if _line != "":
                new.append(_line)
                #self.__processed_line_number_to_src[current_index] = self.__processed_line_number_to_src[i]
                current_index += 1

        return "\n".join(new)

    def __processed_lines(self) -> list[str]:
        return [l for l in self.__processed_code.split("\n") if len(l) > 0]

    def __collect_and_remove_labels(self):
        new = list()
        found = 0
        for (i, row) in enumerate(self.__processed_lines()):
            if row[0] == "#":
                self.__labels[re.findall("(#[\w\d]+)", row)[0][1:]] = len(new)  # This makes it be the
                found += 1
                # correct row even tho labels are removed
            else:
                if row.strip():
                    new.append(row.strip())
                #self.__processed_line_number_to_src[len(new)] = self.__processed_line_number_to_src[i+found]
        self.__processed_code = "\n".join(new)

    def _result(self):
        assert self.__finished_processing
        return self.__processed_code, self.__labels

    def __replace_labels(self):
        #print("======>", self.__processed_code, "<=======")

        for label, index in sorted(self.__labels.items(), key=lambda item: -len(item[0])): # START WITH THE LARGEST.
            print(label)
            def label_value(label_val):
                if isinstance(label_val, int):
                    return label_val
                else:
                    return label_val()
            #print(label)
            self.__processed_code = re.sub("(#"+label+")", str(label_value(index)), self.__processed_code)
        assert "#" not in self.__processed_code

        #print("======", self.__processed_code, "=======")

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
                print("LINE: " + line +";")
                line = line.replace(" ", "")
                i = int(str(line), 2)  # convert binary string to int
                h = hex(i)[2:]  # convert int to hex and cut off '0x' part.
                h = h.upper()
                while len(h) < 4:
                    h = "0" + h
                return h + ";"
            return ""
        try:
            self.__processed_code = "\n".join(l for l in map(fu, self.__processed_lines()))
        except Exception as e:
            print(self.__processed_code)
            raise e

    def _pad_with_zeros(self):
        self.__processed_code += "\n"
        while self.__processed_code.count("\n") < 64:
            self.__processed_code += cfg.nothing + ";\n"

    def processed_line_number_to_src(self, index: int):
        return self.__processed_line_number_to_src[index]

    def __replace_constants(self):
        self.__processed_code = self.replace_constants(self.__processed_code)

    @staticmethod
    def replace_constants(code: str):
        for const in re.findall("(CONST\s*(\w[\w\d]+)\s*=\s*(!?b?\d+))" , code):
            # CONST x 500 on a line gives "x 500"
            code = code.replace(const[0], "")
            assert const[1] not in cfg.instruction_dict and const[1] not in cfg.register_dict
            code = code.replace(const[1], const[2])

        return "\n".join(l for l in code.split("\n") if l)

    def __binary_concatenation(self):
        for to_concat in re.findall("(b(\d*)\s*&\s*b(\d*))", self.__processed_code):
            self.__processed_code = self.__processed_code.replace(to_concat[0], to_concat[1]+to_concat[2])

    def __allow_negation_of_binary(self):
        def negate(binary: str) -> str:
            return binary.replace("0", "3").replace("1", "0").replace("3", "1")

        for to_concat in re.findall("(!b(\d*))", self.__processed_code):
            self.__processed_code = self.__processed_code.replace(to_concat[0], "b"+negate(to_concat[1]))

    def __replace_if_statement(self):  # if R0 == b10101 {}
        for if_statements in re.findall("(if\s+R(\d+)\s*==\s*(!?b?\d*)\s*\{([\s\S]*?)})", self.__processed_code):
            if_st, reg_nbr, number, code_block = if_statements
            rowNum = self.label_offset + \
                self.__processed_code[:self.__processed_code.find(if_st)].count("\n") # Counts all \n before the if
            code = '\n'.join(r.strip() for r in code_block.split("\n") if r)

            new_format = f"""
            #IFSTATEMENTJUMP{rowNum}
            SUB R{reg_nbr} {number}
            BZ R{reg_nbr} #CODEBLOCKSTART{rowNum}
            B R{reg_nbr} #AFTERCODEBLOCK{rowNum}
            #CODEBLOCKSTART{rowNum}
            {code}
            #AFTERCODEBLOCK{rowNum}
            ADD R{reg_nbr} {number}
            """.strip()
            new_format = "\n".join((l.strip() for l in new_format.split("\n") if l))

            self.__processed_code = self.__processed_code.replace(if_st, new_format)

    def __replace_while_statement(self):  # if R0 == b10101 {}
        found_one = False
        for while_loop in re.findall("(while\s+R(\d+)\s*==\s*(b?\d*)\s*\{([\s\S]*?)})", self.__processed_code):
            whole_thing, reg_nbr, number, code_block = while_loop
            rowNum = self.label_offset + \
                self.__processed_code[:self.__processed_code.find(whole_thing)].count("\n") # Counts all \n before the if
            code = '\n'.join(r.strip() for r in code_block.split("\n") if r)

            new_format = f"""
            #WHILESTATEMENTJUMP{rowNum}
            IN R{reg_nbr} 0
            SUB R{reg_nbr} {number}
            BZ R{reg_nbr} #CODEBLOCKSTART{rowNum}
            B R{reg_nbr} #AFTERCODEBLOCK{rowNum}
            #CODEBLOCKSTART{rowNum}
            {code}
            B R{reg_nbr} #WHILESTATEMENTJUMP{rowNum} 
            #AFTERCODEBLOCK{rowNum}
            """.strip()
            new_format = "\n".join((l.strip() for l in new_format.split("\n") if l))
            self.__processed_code = self.__processed_code.replace(whole_thing, new_format)
            found_one = True
        if found_one:
            self.__replace_while_statement()

    def __replace_goto(self):
        for goto in re.findall("(goto\s+(#[\w\d])+)", self.__processed_code):
            whole, label = goto
            self.__processed_code = self.__processed_code.replace(whole, "B R0 " + label)

    def __replace_ret(self):
        self.__processed_code = self.__processed_code.replace("ret", "RET R0 0")

    def __replace_minus_minus_plus_plus(self):
        for minus in re.findall("((R\d+)\s*--)", self.__processed_code):
            whole, reg = minus
            print(whole, reg, "__________")
            self.__processed_code = self.__processed_code.replace(whole, f"SUB {reg} 1")
        for plus in re.findall("((R\d+)\s*\+\+)", self.__processed_code):
            whole, reg = plus
            print(whole, reg, "++++++++++")
            self.__processed_code = self.__processed_code.replace(whole, f"ADD {reg} 1")

    def __replace_delay(self):
        for delay in re.findall("(delay\((\d+)\)\s+(#[\w\d]+))", self.__processed_code):
            whole, num_clks, label = delay
            num_clks = int(num_clks)
            assert num_clks < 2**cfg.datawidth
            sleep = f"""
            goto #endstd{num_clks}
            {label}
            LD R0 {num_clks}
            #Checkstd{num_clks}
            BZ R0 #endstd{num_clks}
            SUB R0 1
            goto #Checkstd{num_clks}
            RET R0 0
            #endstd{num_clks}
            """.strip()
            sleep = "\n".join(l.strip() for l in sleep.split("\n") if l.strip())
            self.__processed_code = self.__processed_code.replace(whole, sleep)

