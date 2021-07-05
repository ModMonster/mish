import os

os.system("color")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

version = "1.0.0"

# initial variables
command = ""
dir = "/home"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# import mash
if (os.path.isfile(root + "/shell/mash.py")):
    import mash

updates = mash.CheckUpdates()

# starting message
print(bcolors.HEADER + f"Mod's Interactive Shell v{version}")
if (len(updates) > 0):
    print("There are " + str(len(updates)) + " updates available")
print("Type help for help." + bcolors.ENDC)

def UpdateFiles():
    # write to command file
    file = open(root + "/shell/command.data", "w") # open file in write mode
    file.write(command) # write command

    # write to dir file
    file = open(root + "/shell/dir.data", "w") # open file in write mode
    file.write(dir) # write dir
    file.close() # close file

def LoadFiles():
    global dir
    file = open(root + "/shell/dir.data", "r") # open file in read mode
    dir = file.read() # read dir 
    file.close() # close file

# run commands
while (command != "exit"):
    command = input(bcolors.OKCYAN + f"{dir} > " + bcolors.ENDC) # get command input

    UpdateFiles()

    # parse command
    args = command.split(" ")

    # does command exist?
    if (os.path.isfile(root + "/scripts/" + args[0] + ".py")):
        exec(open(root + "/scripts/" + args[0] + ".py").read())
    else:
        if (args[0] == "mash"):
            if (os.path.exists(root + "/shell/mash.py")):
                exec(open(root + "/shell/mash.py").read())
        else: 
            if (command != "exit"):
                print("Unknown command. Type help for help.") # error message
                if (os.path.isfile(root + "/shell/mash.py")):
                    if (mash.Exists(args[0])):
                        print("Command exists within the Mash repositories. Install it?")
                        if (input("(y/n) > ") == "y"):
                            mash.Install(args[0])
    LoadFiles()

# delete session data
os.remove(root + "/shell/command.data")
os.remove(root + "/shell/dir.data")