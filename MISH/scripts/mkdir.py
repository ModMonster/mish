# 1.0.0
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file = open(root + "/shell/command.data", "r") # open file in read mode
commands = file.read() # read commands
args = commands.split(" ") # save args
file = open(root + "/shell/dir.data", "r") # open file in read mode
dir = file.read() # read dir
file.close() # close file

newDir = ""

if (len(args) >= 2):
    if (args[1] != ""):
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
        
        # does folder path exist?
        if (os.path.isdir(root + os.path.dirname(newDir))):
            # make it!
            os.mkdir(root + newDir)
        else:
            print("Specified path doesn't exist.")
    else:
        print("You need to specify the name of the directory you want to make.")
else:
    print("You need to specify the name of the directory you want to make.")