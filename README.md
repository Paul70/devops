# devops - Python Module for C++ Project Configuration Management

## Introduction

Devops is a python wrapper module around conan package and build tool manager.
It allows you to script your conan commands and C++ project setup by writing a 
devopsfile.py - just in a similar manner as you are used to it from conan itself.

It offers you the flexibility to adapt your conan and build tool setup by easily setting
- the compiler you want to use
- adds cmake exextuable directly from your conan cache to your build settings
- automatically crates a CMakeUserPresets.json to fully setup your IDE by simply loading the CMakeLists.txt

## Getting Started in 10 Minutes

- Prerequisite: already using conan and having a conanfile.py
- Just add this project as a git submodule to the same location as your top level CMakeLists.txt.
- write the DevopsUserPresets.json where you specify your special settings
- write devopsfile.json like in the example (which will follow soon)
- execute the command
    
        $ python3 devopsfile.py prepare 

will follow soon with more Details and an example project - since this is work in porgress and I also have a full time job - please be a littel patient or just lool at the code, it is actually straigt forward;)

