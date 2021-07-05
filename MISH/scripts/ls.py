# 1.0.0
import os

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

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file = open(root + "/shell/command.data", "r") # open file in read mode
commands = file.read() # read commands
args = commands.split(" ") # save args
file = open(root + "/shell/dir.data", "r") # open file in read mode
dir = file.read() # read dir
file.close() # close file

newDir = ""

if (len(args) >= 2):
    # remove last "/"
    if ((args[1][-1] == "/") & (args[1][0] != "/")):
        args[1] = args[1][:-1]

    # should be absolute?
    if (args[1][0] == "/"):
        newDir = args[1]
    else:
        # in root?
        if (dir == "/"):
            newDir = dir + args[1]
        else:
            newDir = dir + "/" + args[1]

    # dot fixes
    newDir = os.path.abspath(root + newDir) # get rid of ..
    newDir = newDir.replace(root, "", 1) # remove root path
    newDir = newDir.replace("\\", "/") # replace \ with /

    # fix "nodir"
    if (newDir == ""):
        newDir = "/"
else:
    newDir = dir

# does folder path exist?
if (os.path.isdir(root + newDir)):
    # list it!
    fileList = (os.listdir(root + newDir))
    for file in fileList:
        if (os.path.isdir(root + newDir + file)):
            print(bcolors.OKGREEN + file + bcolors.ENDC)
        else:
            print(bcolors.OKBLUE + file + bcolors.ENDC)
else:
    # is destination a file?
    if (os.path.isfile(root + newDir)):
        print("Specified path is a file.")
    else:
        print("Specified path doesn't exist.")