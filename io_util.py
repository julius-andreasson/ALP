import cfg


### IO methods ###
def read_src(path):
    file = open(path, "r")
    src = file.read()
    file.close()
    return src


def write_code(path, code):
    path = path[:-3]  # Remove alp from end of path.
    path += "hex"
    file = open(path, "w")
    file.write(code)
    file.close()


def get_path():
    if cfg.debug:
        path = cfg.default_path
    else:
        path = input("Input .alp file name:")
    # Add .alp to end of path if it's not already there.
    path = "Files/" + path
    if path[-4] != ".alp":
        path += ".alp"
    return path


def print_info(src, code):
    print("Source code:")
    print("=====================")
    print(src)
    print("=====================")
    print("Compiled code:")
    print("=====================")
    print(code)
    print("=====================")
