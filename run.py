import compiler
import io_util as io

### Execution ###
path = io.get_path()     # Get path
src = io.read_src(path)  # Read file from path
code = compiler.compile(src)   # Compile
io.write_code(path, code)# Write to file
io.print_info(src, code) # Print compilation info