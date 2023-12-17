#! /usr/bin/python3

import argparse
from devops import DevOps


class Command():

    def __init__(self) -> None:
        self.devops = DevOps()
        pass

    def action_bootstrap(self, profile = ""):
        self.devops.bootstrap(profile)
        pass



###############################################################################################
#
# Run section 
#
###############################################################################################

# Command line argument parsing
# Arguments with '-' or '--': optional
# Arguments without '-' or '--': mandatory
parser = argparse.ArgumentParser(description="",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bootstrap", action="store_true", help="Installs all dependencies and writes cmake settings.")
parser.add_argument("--profile", help="Use a specific configuration setup profile.")

args = parser.parse_args()
config = vars(args)
#print(config)

runner = Command()
if config["bootstrap"] and not config["profile"]:
    runner.action_bootstrap()
elif config["bootstrap"] and config["profile"]:
    runner.action_bootstrap(config["profile"])
pass