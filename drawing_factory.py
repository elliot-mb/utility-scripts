#!/usr/bin/env python3

# This script's job is to help me keep my drawings organised. I like to create digital drawings from a template drawing that starts with a certain layer grouping and structure, including colouring layers, a sketch layer etc. I usually manually copy a template into it's own folder inside a "created" directory, so that I can have multiple versions of the same drawing in their own folder. This just gets me started with that, creating a blank copy of the defined template in its own folder in a "created" folder

import argparse
import subprocess

# tries to make a folder and errors if not
def makeFolder(path):
    cp = subprocess.run(["mkdir", path])
    if not cp.returncode == 0:
        raise Exception("No folder '" + path + "' could be created.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of new drawing")
    parser.add_argument("-t", "--template_file", help="path of template drawing", default="template.kra", required=False)
    parser.add_argument("-r", "--repo", help="name of created-drawings repository", default="created", required=False)

    args = parser.parse_args()

    cp = subprocess.run(["test", "-e", args.template_file])
    if not cp.returncode == 0:
        raise Exception("No template file '"+args.template_file+"'.")

    cp = subprocess.run(["test", "-d", args.repo])
    if not cp.returncode == 0:
        print("No repo folder. Creating...")
        makeFolder(args.repo)
    
    makeFolder(args.repo + "/" + args.name)
    cp = subprocess.run(["cp", args.template_file, args.repo+"/"+args.name+"/"+args.name+".kra"])
    if not cp.returncode == 0:
        raise Exception("Could not copy toplevel " +args.template_file+" file to './"+args.repo+"/"+args.name+"/"+args.name+".kra'.")

if __name__ == "__main__":
    main()
