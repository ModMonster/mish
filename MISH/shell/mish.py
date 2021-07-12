import os

# is windows?
if (os.name == "nt"):
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

version = "1.2.1"

# initial variables
command = ""
dir = "/home"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# delete session data in case of force quit
if (os.path.exists(root + "/shell/command.data")):
    os.remove(root + "/shell/command.data")
if (os.path.exists(root + "/shell/dir.data")):
    os.remove(root + "/shell/dir.data")

# import mash
if (os.path.isfile(root + "/shell/mash.py")):
    import mash
    
    # make config file if it doesnt exist
    if (not os.path.isfile(root + "/shell/mash.conf")):
        mashconfFile = open(root + "/shell/mash.conf", "w")
        mashconfFile.write("false")
        mashconfFile.close()

    # read config file
    mashconfFile = open(root + "/shell/mash.conf", "r")
    mashconf = mashconfFile.readlines()
    mashconfFile.close()

    # check for updates
    updates = []
    if (mashconf[0] == "true"):
        updates = mash.CheckUpdates()

# starting message
print(bcolors.HEADER + f"Mod's Interactive Shell v{version}")
# make sure mash exists
if (os.path.exists(root + "/shell/mash.py")):
    if (len(updates) > 0):
        # display updates available
        if (len(updates) == 1):
            print("There is " + str(len(updates)) + " update available")
        else:
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
                print("Unknown command. Type help for help.") # error message
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