import util as u

### Execution ###
path = u.get_path()     # Get path
src = u.read_src(path)  # Read file from path
code = u.compile(src)   # Compile
u.write_code(path, code)# Write to file
u.print_info(src, code) # Print compilation info