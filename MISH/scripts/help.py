import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file = open(root + "/shell/command.data", "r") # open file in read mode
commands = file.read() # read dir
args = commands.split(" ")
file.close() # close file

if (len(args) >= 2):
    # does required help file exist?
    if (os.path.exists(root + "/help/" + args[1] + ".txt")):
        file = open(root + "/help/" + args[1] + ".txt") # load help file
        print(file.read())
    else:
        # does command exist?
        if (os.path.exists(root + "/scripts/" + args[1] + ".py")):
            print("Requested script exists, but has no help file.")
        else:
            print("Requested script not found.")
else:
    print("Type help <command> to find out information about a specific command.")
    print("Type help mish to get general help about Mish.")
    print("Type exit to exit Mish")