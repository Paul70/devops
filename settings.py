#! /usr/bin/python3
import platform
import subprocess

from utility import Utility

class Settings():

    def checkOS(self, project, profile, os_list):
        print("\n======== Checking operating system support ========")
        print("devops.py (" + project + "): checkOS()")
        config_dict = Utility.loadProfile(project, profile)
        if not config_dict["os"] in os_list:
            print("devops.py (" + project + "): Project cannot be configured for " + config_dict["os"])
            return False
        if not platform.release() in os_list:
            print("devops.py (" + project + "): Project does not support current host operating system ")
            return False
        return True
        pass