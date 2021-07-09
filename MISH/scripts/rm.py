# 1.0.1
import os
import shutil

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
        
        if (os.path.exists(root + newDir)):
            print("Are you sure you want to remove " + newDir + "?")
            if (input("(y/n) > ") == "y"):
                if (os.path.isdir(root + newDir)):
                    if (len(os.listdir(root + newDir)) == 0):
                        os.rmdir(root + newDir)
                    else:    
                        print("Directory is not empty. Continue anyways?")
                        if (input("(y/n) > ") == "y"):
                            shutil.rmtree(root + newDir)
                        else:
                            print("Aborting.")
                else:
                    os.remove(root + newDir)
            else:
                print("Aborting.")
        else:
            print("Specified path doesn't exist.")
    else:
        print("You need to specify what you want to remove.")
else:
    print("You need to specify what you want to remove.")