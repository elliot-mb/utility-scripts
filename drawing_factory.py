#!/usr/bin/env python3

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
