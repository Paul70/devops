import argparse
from .commands import CliCommand

def create_parser():
    
    # check if we have to load a user devopsfile.py under the project root
    #module = CliParser.load_user_devops_file()

    parser = argparse.ArgumentParser(description="Automation tool to manage, configure, \
                                        build and package C++ projects.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Bootstrap command
    parser_bootstrap = subparsers.add_parser(
        "bootstrap", 
        help="Initialize the environment"
    )
    parser_bootstrap.set_defaults(func=CliCommand().cli_bootstrap)
    
    # Prepare command
    parser_prepare = subparsers.add_parser(
        "prepare", 
        help="Prepare the resources"
    )
    parser_prepare.set_defaults(func=CliCommand().cli_prepare)

    # Build command
    parser_build = subparsers.add_parser("build", help="Build the project")
    parser_build.add_argument(
        "-t", 
        "--type", 
        type=str, 
        choices=["debug", "release"],
        help="Specify the build type (choices: debug, release).", 
        default="debug"
    )
    parser_build.set_defaults(func=CliCommand().cli_build)

    return parser



