import os

# Define the variable you want to search for
variable_name = 'weedmark_ext'

# Directory containing the files
directory = r'\Users\sufya\DICELAB_TroughProject'

# check if the variable is commented
def is_comment(line):
    return line.strip().startswith('#')

# Search for the variable in each file
def search_variable_in_files(directory, variable_name):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):  # Consider only Python files
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
                found_lines = [line.strip() for line in lines if variable_name in line and not is_comment(line)]
                if found_lines:
                    print(f"File: {filename}")
                    for found_line in found_lines:
                        print(found_line)

# Call the function with the directory containing the files
search_variable_in_files(directory, variable_name)

