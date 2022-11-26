import util as u

### Execution ###
path = u.get_path()     # Get path
alp = u.read_alp(path)  # Read file from path
code = u.compile(alp)   # Compile
u.write_code(path, code)# Write to file
u.print_info(alp, code) # Print compilation info