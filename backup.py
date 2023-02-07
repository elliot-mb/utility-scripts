#!/usr/bin/env python3

import subprocess as sp
import sys
from typing import List

# On my laptop I am dualbooting. To deal with backing my "fragmented" system up I use Borg backup. (https://www.borgbackup.org/)
# This alone was not enough so I decided to make this script for minimal-effort backups; hopefully encouraging me to do it more often.

# This script is a notably safer way for me to perform my backups easily. Before this job was done by a 5-line bash script, but 
# because it is an important operation, it necessitated a safer approach. Python was a convenient choice.
# It has extra functionality: backups can be performed on individual Operating Systems/partitions as well as together. For 
# example, if one fails and the script stops, I don't need to wait for both to back up just to back up the one remaining partition.


### The shell script it replaced: ###

# set -e # Exit immediately if a command exits with a non-zero status.
#
# ERROR=$(cd "/media/elliot/Windows" 2>&1) && cd "/media/elliot/Windows" || (echo "Error finding Windows parition: '$ERROR'"; exit 1)
#
# ERROR=$(cd /media/elliot/linux/current-envy 2>&1) && cd /media/elliot/linux/current-envy || (echo "Error in external SSD: '$ERROR'"; exit 1)
# echo "Backup starting inside $(pwd)"
# sudo ./backup || (echo "Error running backup sub-script in /linux"; exit 1)
# ERROR=$(cd /media/elliot/windows/current-envy 2>&1) && cd /media/elliot/windows/current-envy || (echo "Error in external SSD: '$ERROR'"; exit 1)
# echo "Backup starting inside $(pwd)" 
# sudo ./backup || (echo "Error running backup sub-script in /windows: '$ERROR'"; exit 1)


FAIL: int = 1
SUCC: int = 0

def showInfo(s: str) -> None:
    print("[Info]  " + s)

def showError(s: str) -> None:
    print("[Error] " + s)

def check_windows_partitions() -> None:
    ok = sp.call("cd \"/media/elliot/Windows\"", shell=True)
    if ok != 0: 
        showError("Failed to find windows partition at /media/elliot/Windows")
        exit(FAIL)

    ok = sp.call("cd /media/elliot/windows", shell=True)
    if ok != 0:
        showError("Failed to find external drive partition at /media/elliot/windows")
        exit(FAIL)

def check_linux_partitions() -> None:
    ok = sp.call("cd /media/elliot/linux", shell=True)
    if ok != 0:
        showError("Failed to find external drive partition at /media/elliot/linux")
        exit(FAIL)

def run_backup(OS: str) -> None:
    match OS:
        case "linux" | "windows":

            # showInfo("Backup starting in " + str(sp.Popen("pwd", shell=True, stdout=sp.PIPE).stdout.read())[2:-3])
            location: str = "/media/elliot/" + OS + "/current-envy"
            showInfo("Backup starting in " + location)
            ok = sp.call("cd /media/elliot/"+OS+"/current-envy && sudo ./backup", shell=True)
            if ok != 0:
                showError("Backup for " + OS + " finished with a warning or an error")

        case _:
            showError("run_backup was provided invalid os '" + OS + "'")
            exit(FAIL)

def backup(is_windows: bool, is_linux: bool) -> None:

    if is_windows:
        check_windows_partitions()
        run_backup("windows")
    
    if is_linux:
        check_linux_partitions()
        run_backup("linux")

def main() -> None:
    args: List[str] = sys.argv[1:]
    is_windows: bool = False 
    is_linux: bool = False

    match args:
        case ["linux", "windows"] | ["windows", "linux"]:
            showInfo("Set to back up Linux and Windows")
            is_windows, is_linux = True, True

        case ["linux"]:
            showInfo("Set to back up Linux")
            is_linux = True

        case ["windows"]:
            showInfo("Set to back up Windows")
            is_windows = True

        case _:
            showError("Arguments " + str(args) + " are invalid.")
            showInfo("Usage: ./backup [OPERATING SYSTEM 1] [OPERATING SYSTEM 2]")
            showInfo("Operating systems are optional, and can be either 'windows' or 'linux'")
            sys.exit(FAIL)

    showInfo("Are you sure you want to continue? (y/n)")
    inp: str = input("[Input] ").strip()
    match inp:
        case "y":
            backup(is_windows, is_linux)
            showInfo("Backup finished successfully")
        case _:
            showInfo("Backup cancelled")

    sys.exit(SUCC)

if __name__ == "__main__":
    main()