import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("Welcome to the configuration of the development environment for Mish.")
print("Type the full command you would like to excecute:")
command = input("> ")
print("Type the directory to excecute in:")
dir = input("> ")
print("Now you can run your script from the scripts folder without any issues!")

# write to command file
file = open(root + "/shell/command.data", "w") # open file in write mode
file.write(command) # write command

# write to dir file
file = open(root + "/shell/dir.data", "w") # open file in write mode
file.write(dir) # write dir
file.close() # close file