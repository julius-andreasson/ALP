import func as f

### Execution ###
path = f.get_path()     # Get path
alp = f.read_alp(path)  # Read file from path
code = f.compile(alp)   # Compile
f.write_code(path, code)# Write to file
f.print_info(alp, code) # Print compilation info