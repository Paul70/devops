#! /usr/bin/python3

import argparse
from build import DevOps

# Command line argument parsing
# Arguments with '-' or '--': optional
# Arguments without '-' or '--': mandatory
parser = argparse.ArgumentParser(description="",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bootstrap", action="store_true", help="Installs all dependencies and writes cmake settings.")
parser.add_argument("--profile", help="Use a specific configuration setup profile.")

args = parser.parse_args()
config = vars(args)
print(config)


devops = DevOps()
if config["bootstrap"] and not config["profile"]:
    devops.bootstrap()
elif config["bootstrap"] and config["profile"]:
    devops.bootstrap(config["profile"])
pass