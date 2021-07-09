import os
import urllib.request
import urllib.error
import requests

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
        size = size.split("\n")

        print("Package " + script + " version " + size[2] + " is selected for this installation.")

        # do we want help?
        if (helpInstalled):
            print(size[0] + " of disk space will be used for this install. Continue?")
        else:
            print(size[1] + " of disk space will be used for this install. Continue?")

        # autocontinue?
        if (yes):
            print("(y/n) > y")
            BaseInstall(script)
        else:
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
            onlineScriptLines = onlineScriptLines.split("\n")

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
        if (len(args) >= 4):
            yes = args[3] == "yes" or args[3] == "y" # always answer yes?
        else:
            yes = False

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

                    # autocontinue?
                    if (yes):
                        print("(y/n) > y")
                        # UNINSTALL
                        print("Uninstalling script file")
                        os.remove(root + "/scripts/" + args[2] + ".py")
                        
                        if (helpInstalled):
                            print("Uninstalling help file")
                            os.remove(root + "/help/" + args[2] + ".txt")
                    else:
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
        print("Type help mash for more information.")