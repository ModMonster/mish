import os
import importlib.util

# is easygui installed?
if ((spec := importlib.util.find_spec("easygui")) is not None):
    import easygui
    useGui = True
else:
    useGui = False

# Clear screen
if (os.name == "nt"):
    cls = lambda: os.system('cls')
else:
    cls = lambda: os.system('clear') 

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


shellContents = """import os

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

version = "1.2.0"

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
os.remove(root + "/shell/dir.data")"""

mashContents = """import os
import urllib.request
import urllib.error
import requests

class bcolors:
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'

mashURL = "https://modmonster.github.io/mash/" # change this to use a custom mash repository

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
helpInstalled = os.path.isdir(root + "/help")

error = False

def BaseInstall(script):
    # install the script
    targetURL = mashURL + script + "/" + script + ".py"
    print("Getting script file from " + targetURL)

    request = requests.get(targetURL)
    open(root + "/scripts/" + script + ".py", "wb").write(request.content)

    # install the help
    if (helpInstalled):
        targetURL = mashURL + script + "/" + script + ".txt"
        print("Getting help file from " + targetURL)

        request = requests.get(targetURL)
        open(root + "/help/" + script + ".txt", "wb").write(request.content)

def Install(script):
    global error
    print("Searching for package " + script)
    try:
        sizePage = urllib.request.urlopen(mashURL + script + "/info.txt")
    except urllib.error.HTTPError:
        print(bcolors.FAIL + "Specified package " + script + " does not exist in the Mash repositories." + bcolors.ENDC)
        error = True
    if (not error):
        # get size of packages
        size = sizePage.read()
        size = size.decode("utf-8")
        size = size.split("\\n")

        print("Package " + script + " version " + size[2] + " is selected for this installation.")

        # do we want help?
        if (helpInstalled):
            print(size[0] + " of disk space will be used for this install. Continue?")
        else:
            print(size[1] + " of disk space will be used for this install. Continue?")

        if (input("(y/n) > ") == "y"):
            BaseInstall(script)
        else:
            print("Aborting...")

def Exists(name):
    # package ends in /?
    if (name[-1] == "/"):
        return False

    try:
        sizePage = urllib.request.urlopen(mashURL + name + "/info.txt")
    except urllib.error.HTTPError:
        return False
    return True

def CheckUpdates():
    # find version of files
    localVersion = []
    onlineVersion = []
    scripts = []
    for script in os.listdir(root + "/scripts"):
        # find version of local files
        currentScript = open(root + "/scripts/" + script)
        versionLine = currentScript.readlines()[0]
        
        # is this file in mish?
        if (versionLine[0] == "#"):
            versionLine = versionLine.replace("# ", "")
            version = int(versionLine.replace(".", ""))
            localVersion += [version]

            # find version of online files
            scriptName = script.replace(".py", "")
            onlineScript = urllib.request.urlopen(mashURL + scriptName + "/info.txt")

            # decode
            onlineScriptLines = onlineScript.read()
            onlineScriptLines = onlineScriptLines.decode("utf-8")
            onlineScriptLines = onlineScriptLines.split("\\n")

            version = int(onlineScriptLines[2].replace(".", ""))
            onlineVersion += [version]
            
            scripts += [script.replace(".py", "")]
    currentScript.close()

    # check for updates
    updates = []

    for script in scripts:
        # set index
        index = scripts.index(script)

        # needs update?
        if (onlineVersion[index] > localVersion[index]):
            updates += [script]
    
    return updates

# commands
if (os.path.exists(root + "/shell/command.data")):

    file = open(root + "/shell/command.data", "r") # open file in read mode
    commands = file.read() # read commands
    args = commands.split(" ") # save args
    file.close()

    # read command
    if (len(args) >= 2):
        if (args[1] == "install"):
            if (len(args) >= 3):
                # install
                Install(args[2])
            else:
                print("You need to specify a package to install.")
        elif (args[1] == "remove"):
            # uninstall
            if (len(args) >= 3):
                scriptFile = root + "/scripts/" + args[2] + ".py"
                helpFile = root + "/help/" + args[2] + ".txt"

                # is package installed?
                if (os.path.isfile(scriptFile)):
                    # CALCULATE SIZE

                    size = os.path.getsize(scriptFile)
                    if (helpInstalled):
                        size += os.path.getsize(helpFile)
                    
                    if (size >= 1000000000):
                        strSize = str((size / 1000000000)) + " GB"
                    elif (size >= 1000000):
                        strSize = str((size / 1000000)) + " MB"
                    elif (size >= 1000):
                        strSize = str((size / 1000)) + " KB"
                    else:
                        strSize = str(size) + " B"

                    print(strSize + " of disk space will be freed. Continue?")
                    if (input("(y/n) > ") == "y"):
                        # UNINSTALL
                        print("Uninstalling script file")
                        os.remove(root + "/scripts/" + args[2] + ".py")
                        
                        if (helpInstalled):
                            print("Uninstalling help file")
                            os.remove(root + "/help/" + args[2] + ".txt")
                    else:
                        print("Aborting.")
                else:
                    print("Specified package " + args[2] + " is not installed.")
            else:
                print("You need to specify a package to remove.")
        elif (args[1] == "update"):
            print("Checking for updates...")
            updates = CheckUpdates()

            # do the updates
            if (len(updates) > 0):
                print("Updates are available for " + str(len(updates)) + " scripts.")
                for script in updates:
                    BaseInstall(script)
            else:
                print("Everything is up to date!")
        else:
            print("Usage: mash <install/remove> <package>")
            print("Type help mash for more information.")
    else:
        print("Usage: mash <install/remove> <package>")
        print("Type help mash for more information.")"""

cdContents = """# 1.0.0
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
        newDir = newDir.replace("\\\\", "/") # replace \ with /

        # fix "nodir"
        if (newDir == ""):
            newDir = "/"

        # is destination a directory?
        if (os.path.isdir(root + newDir)):
            # actually change the directory
            file = open(root + "/shell/dir.data", "w") # open file in write mode
            file.write(newDir)
            file.close()
        else:
            # is destination a file?
            if (os.path.isfile(root + newDir)):
                print("Specified path is a file.")
            else:
                print("Specified path doesn't exist.")
    else:
        print("You need to specify a directory to change to.")
else:
    print("You need to specify a directory to change to.")"""

lsContents = """# 1.0.0
import os

class bcolors:
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'

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
    newDir = newDir.replace("\\\\", "/") # replace \ with /

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
        print("Specified path doesn't exist.")"""

mkdirContents = """# 1.0.0
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
        newDir = newDir.replace("\\\\", "/") # replace \ with /

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
    print("You need to specify the name of the directory you want to make.")"""

rmContents = """# 1.0.0
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
        newDir = newDir.replace("\\\\", "/") # replace \ with /

        # fix "nodir"
        if (newDir == ""):
            newDir = "/"
        
        if (os.path.exists(root + newDir)):
            print("Are you sure you want to remove " + newDir + "?")
            if (input("(y/n) > ") == "y"):
                if (os.path.isdir(root + newDir)):
                    if (len(os.listdir(root + newDir)) == 0):
                        os.removedirs(root + newDir)
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
    print("You need to specify what you want to remove.")"""

execContents = """# 1.1.0
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

        # is destination a directory?
        if (os.path.exists(root + newDir)):
            if (os.name == "nt"):
                os.system("start " + root + newDir)
            else:
                os.system("gedit " + root + newDir)
        else:
            print("Specified file doesn't exist.")
    else:
        print("You need to specify something to excecute.")
else:
    print("You need to specify something to excecute.")"""

newContents = """# 1.0.0
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
        newDir = newDir.replace("\\\\", "/") # replace \ with /

        # fix "nodir"
        if (newDir == ""):
            newDir = "/"
        
        if (os.path.isdir(os.path.dirname(root + newDir))):
            if (not os.path.exists(root + newDir)):
                newFile = open(root + newDir, "w")
                newFile.close()
            else:
                print("File or directory already exists.")
        else:
            print("Parent directory of file is a file.")
    else:
        print("You need to specify a name for the new file.")
else:
    print("You need to specify a name for the new file.")"""

helpContents = """import os

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
    print("Type exit to exit Mish")"""

cdHelpContents = """cd - Changes current directory.
Usage: cd <directory>

Changes the currently active directory to whatever you type. You can use a relative path or an absolute path.

EXAMPLES
    cd /home
        Changes directory to the home directory, which is in the root of the filesystem.
    cd /home/Documents
        Changes directory to the Documents directory, which is in the home directory, which is in the root of the filesystem.
    cd Documents
        Changes directory to the Documents directory inside of the current directory.
    cd ..
        Changes directory to the parent directory of the current directory."""

lsHelpContents = """ls - Lists files.
Usage: ls <directory>

Lists the files in the directory with the name of whatever you type. You can use a relative path or an absolute path.

EXAMPLES
    ls example
        Lists the files in a directory named example in the current directory.
    ls example/hello
        Lists the files in a directory named hello within the directory example within the current directory.
    ls /example
        Lists the files in a directory named example within the root of the filesystem.
    ls ../example
        Lists the files in a directory named example within the parent directory of the current directory."""

mkdirHelpContents = """mkdir - Makes a directory.
Usage: mkdir <directory>

Makes a directory with the name of whatever you type. You can use a relative path or an absolute path.

EXAMPLES
    mkdir example
        Makes a directory named example in the current directory.
    mkdir example/hello
        Makes a directory named hello within the directory example within the current directory.
    mkdir /example
        Makes a directory named example within the root of the filesystem.
    mkdir ../example
        Makes a directory named example within the parent directory of the current directory."""

rmHelpContents = """rm - Removes files and directories.
Usage: rm <path>

Removes whatever file or directory you type. You can use a relative path or an absolute path.

EXAMPLES
    rm example
        Removes example from within the current directory.
    rm example/hello
        Removes hello from within the directory example within the current directory.
    rm /example
        Removes example from within the root of the filesystem.
    mkdir ../example
        Removes example from within the parent directory of the current directory."""

execHelpContents = """exec - Excecutes files.
Usage: exec <file>

Excecutes the current file in the default application depending on the file type. If the specified path is a folder, it will open in the file manager.

EXAMPLES
    exec /home
        Opens the file manager in the home directory, which is in the root of the filesystem.
    exec /home/text.txt
        Opens text.txt, which is in the home directory, which is in the root of the filesystem.
    exec example.txt
        Opens example.txt, which is inside of the current directory.
    exec ..
        Opens the file manager in the parent directory of the current directory."""

newHelpContents = """new - Adds new files.
Usage: new <file>

Makes a new file with the name of whatever you type.

EXAMPLES
    make /example.txt
        Makes a file named example.txt in the root of the filesystem.
    make /home/example.txt
        Makes a file named example.txt in the home directory, which is in the root of the filesystem.
    make example.txt
        Makes a file named example.txt inside of the current directory.
    cd ../example.txt
        Makes a file named example.txt in the parent directory of the current directory."""

mishHelpContents = """Welcome to Mod's Interactive Shell, aka Mish.
Mish is a modular shell written in Python. It is very easy to make your own commands to run to increase your productivity and help you complete monotonous tasks quickly.

THE FILESYSTEM
    Mish's filesystem is made up of a directories which are all located inside the root directory. The root directory is known as "/".
    The current directory is displayed to the left of the typing prompt arrow.
    You can use the "cd" command to change which directory you are currently in.

    Here is a breakdown of the default directories found on the root of the filesystem.

    HELP
        Stores all of the text that shows up when you type "help <command>" within plain text files. Within "mish.txt" is the text you are reading now!
    HOME
        Stores all of the user files. It's the directory that you get sent to when starting Mish and is empty by default.
    SCRIPTS
        Stores all of the scripts that act as commands within the shell. These scripts are written in Python. If you are going to tinker with them, you should make a backup first so that you don't accidentally mess them up.
    SHELL
        Stores the core files of Mish. These shouldn't be tampered with unless you know what you're doing.

MAKING YOUR OWN COMMANDS
    It's easy to make your own command in Mish, assuming you have some experience with Python. The commands are known as scripts and are located in the scripts folder. You can make a new command by making a new file in the scripts folder with the name of your command and the .py extension. Then, you can just code what you want your script to do in Python.
    If you want to access the current directory or see what arguments your command was run with, you can read the files "dir.data" and "command.data" inside the shell folder.
    If you want your script to work with Mash, the first line should contain the commented out version number. For example: # 1.0.0 (note there is a space between # and number)
    Once you've made something cool, you can make a file within the help folder to print when the user wants help with your command. Make a new file with the name of the script and the extension ".txt" and write whatever the user might need to know when using your command.
    That's pretty much everything! Have fun writing your own commands!"""

mashHelpContents = """mash - Installs programs.
Mod's Amazing Script Handler, aka Mash is an easy way to download scripts from the internet.

SYNTAX
    mash install <package>
        Downloads and installs the specified package from the web.
    mash remove <package>
        Removes the specified package from the /scripts folder.
    mash update (package)
        Updates all installed packages. Optionally, you can specify a package and it will be the only one updated.
    mash list <installed/available)
        Lists all installed packages, or all packages available in the Mash repository.

MAKING YOUR OWN MASH REPOSITORY
    If you want to host your own Mish commands to be installed through Mash, it's fairly easy.
    The first thing to do is esablish some sort of web hosting for your scripts.
    You need to then upload a folder containing three files:
    
    package.py
        This contains all of the code for your script. It will be placed in the scripts folder. Rename it to whatever your script is called.
    package.txt
        This is the help file for your script. It will be placed in the help folder, if the user chose to install help when installing Mish. Rename it to whatever your script is called.
    info.txt
        This is the only file that doesn't actually get downloaded.
        You need to put three different pieces of information on three different lines.

        LINE 1
            Size of your script + your help file.
        LINE 2
            Size of just your script.
        LINE 3
            Version of your script. This is used for updating to check if your script's version is higher than the current version.
        
        For example, you might end up with:

        2.54 KB
        1.98 KB
        1.0.0

    Once you have these three files, put them on to your server in a folder with the same name as your package. Here's what it looks like for the cd command.

    cd (folder)
    | - cd.py (script file)
    | - cd.txt (help file)
    | - info.txt (info file)

    Lastly, you need to change the variable "mashURL" within the Mash script to point towards your server. You should point it towards the folder containing all of the package folders.
    
    That's it! You should now be able to install various packages from your own server!"""


# FOLDER SETUP

installDir = ""
badDir = False

while (not os.path.isdir(installDir)):
    cls()
    print(bcolors.HEADER + f"This wizard will install Mish version {version} on your computer." + bcolors.ENDC)
    print("You can press " + bcolors.WARNING + "CTRL+C" + bcolors.ENDC + " any time to abort the installation.")
    
    # use gui?
    if (useGui):
        print("Where would you like to install?")
        installDir = easygui.diropenbox("Select an empty folder to install Mish within.")

        # did we cancel?
        if (installDir == None):
            print("Canceled location picking, aborting.")
            exit()
    else:
        print("Where would you like to install?")
        if (badDir):
            installDir = input(bcolors.OKCYAN + "Selected path is not a directory. Try again" + bcolors.ENDC + " > ")
        else:
            installDir = input(bcolors.OKCYAN + "Type a path to an empty folder" + bcolors.ENDC + " > ")
        badDir = True

cls()

# SCRIPT INSTALLATION

mashSelected = True
commandsSelected = True
helpSelected = True

selection = 3
badNumber = False

done = False

# SELECT SCRIPTS
while (done == False):
    cls()

    print(bcolors.HEADER + "Select the scripts you would like to install." + bcolors.ENDC)
    print("Type a number to select an option that you want to toggle, or 4 to continue.\n")

    print("    [x] Install core Mish files")

    if (mashSelected):
        print(bcolors.OKBLUE + "(1)" + bcolors.ENDC + " [x] Install Mash (Mod's Amazing Script Handler)")
    else:
        print(bcolors.OKBLUE + "(1)" + bcolors.ENDC + " [ ] Install Mash (Mod's Amazing Script Handler)")
    
    if (commandsSelected):
        print(bcolors.OKBLUE + "(2)" + bcolors.ENDC + " [x] Install basic commands")
    else:
        print(bcolors.OKBLUE + "(2)" + bcolors.ENDC + " [ ] Install basic commands")

    if (helpSelected):
        print(bcolors.OKBLUE + "(3)" + bcolors.ENDC + " [x] Install command documentation")
    else:
        print(bcolors.OKBLUE + "(3)" + bcolors.ENDC + " [ ] Install command documentation")


    print("\n" + bcolors.OKBLUE + "(4)" + bcolors.ENDC + " Continue")

    if (badNumber):
        selection = input("Invalid number > ")
    else:
        selection = input("Type a number > ")

    badNumber = False
    if (selection == "1"):
        mashSelected = not mashSelected
    elif (selection == "2"):
        commandsSelected = not commandsSelected
    elif (selection == "3"):
        helpSelected = not helpSelected
    elif (selection == "4"):
        done = True
    else:
        badNumber = True

cls()

# COLOR SETUP



# INSTALL!

def Install(file, data):
    file = open(file, "w")
    file.write(data)
    file.close()

print("Setting up the filesystem...")
os.mkdir(installDir + "/scripts")
os.mkdir(installDir + "/shell")
if (helpSelected):
    os.mkdir(installDir + "/help")
os.mkdir(installDir + "/home")

print("Installing the shell...")
Install(installDir + "/shell/mish.py", shellContents)

if (mashSelected):
    print("Installing Mash...")
    Install(installDir + "/shell/mash.py", mashContents)

if (commandsSelected):
    print("Installing base commands...")
    Install(installDir + "/scripts/cd.py", cdContents)
    Install(installDir + "/scripts/ls.py", lsContents)
    Install(installDir + "/scripts/mkdir.py", mkdirContents)
    Install(installDir + "/scripts/rm.py", rmContents)
    Install(installDir + "/scripts/exec.py", execContents)
    Install(installDir + "/scripts/new.py", newContents)

if (helpSelected):
    print("Installing documentation...")
    Install(installDir + "/scripts/help.py", helpContents)
    Install(installDir + "/help/cd.txt", cdHelpContents)
    Install(installDir + "/help/ls.txt", lsHelpContents)
    Install(installDir + "/help/mkdir.txt", mkdirHelpContents)
    Install(installDir + "/help/rm.txt", rmHelpContents)
    Install(installDir + "/help/mish.txt", mishHelpContents)
    Install(installDir + "/help/exec.txt", execHelpContents)
    Install(installDir + "/help/new.txt", newHelpContents)
    
    if (mashSelected):
        Install(installDir + "/help/mash.txt", mashHelpContents)

print("\nInstall complete! Press enter to exit the installer.")
input()
exit()