#!/usr/bin/env python3

import argparse
import subprocess as subp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of terminal window")
    parser.add_argument("script", help="script filepath")

    args = parser.parse_args()

    subp.run("tmux new-session -d -s " + args.name + "_session >/dev/null && tmux new-window -t " + args.name + " && tmux send-keys -t " + args.name + ":1.0 " + args.script + " Enter", shell=True, check=True)
    subp.run("tmux ls", shell=True, check=True)

if __name__ == "__main__":
    main()

