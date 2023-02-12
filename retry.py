#!/usr/bin/env python3

# criticisms 
#   - use argparse
#   - subprocess.run
#   - cwd to change directory

# retry.py -> higher order (and possibly dangerous) program that takes a terminal command and re-runs it until it terminates sucessfully.
# I thought program of this while trying to push a docker image on the train, the wifi was terrible and the command would fail from network timeout.
# I knew this was the only issue, so I would just have to keep re-running it until the wifi was consistent.

import argparse
import subprocess as subp
import sys
from time import sleep
from typing import Tuple 

class ArgsBox:
    # written into by argparse
    command: str
    w: str
    b: str

    def get_command(self) -> str:
        return self.command
    
    # throws an exception when argument isnt an int
    def get_wait_time(self) -> int:
        return int(self.w)
    
    # throws exception when argument isnt of the right format
    def get_backoff(self) -> Tuple[int, int]:
        [factor, limit] = self.b.split(":")
        return [int(factor), int(limit)]
    
def backoff(wait, fact, lim) -> int:
    wait *= fact
    if (wait > lim): return lim
    return wait

def main():
    args_box = ArgsBox()
    parser = argparse.ArgumentParser(
                    prog = 'retry',
                    description = 'Retries a given command until the command is successful',
                    epilog = '')
    
    parser.add_argument("command")
    parser.add_argument("--w", "-wait_time", default=1, required=False) # seconds
    parser.add_argument("--b", "-backoff",   default="1:1", required=False) # factor:limit

    parser.parse_args(args=sys.argv[1:], namespace=args_box)

    #print(args_box.__dict__)

    attempt: int = 0
    backoff_fact, backoff_lim = args_box.get_backoff()
    wait_time: int = args_box.get_wait_time()
    
    cp: subp.CompletedProcess = subp.CompletedProcess(args=args_box.get_command(), returncode=1)
    while(cp.returncode != 0):
        print("attempt:", attempt)
        cp = subp.run(args_box.get_command(), shell=True)

        attempt += 1

        print("waiting:", str(wait_time) + "s")
        if(cp.returncode != 0): sleep(int(wait_time))

        wait_time = backoff(wait_time, backoff_fact, backoff_lim)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("retry: exiting")
        exit(0)
    except Exception as e:
        print("retry:", str(type(e))[8:-2]+":", e.args[0])
        exit(1)