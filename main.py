import sys

sys.dont_write_bytecode = True


import os
import importlib.util
from pathlib import Path
import term_function
import shlex

if os.name=="nt":
    os.system("")

COLOR = '\033[92m'
ERROR_COLOR='\033[91m'
WARN_COLOR = '\033[0;33m'
RESET = '\033[0m'

script_dir = Path(__file__).resolve().parent

def load_package(package_name):
    spec = importlib.util.spec_from_file_location(package_name, script_dir / "installed" / package_name / "main.py")
    package = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = package
    spec.loader.exec_module(package)
    return package

def confirmation(question):
    try:
        confirmation = input(question + " (y/n) > ")
    except KeyboardInterrupt:
        exit_terminal()

    if confirmation.lower() == "y" or confirmation.lower() == "yes":
        return True
    else:
        return False

def error(message):
    print(f"{ERROR_COLOR}{message}{RESET}")

def warn(message):
    print(f"{WARN_COLOR}{message}{RESET}")

def exit_terminal():
    term_function.commands.get("exit")()

while True:
    try:
        inp = input(f"{COLOR}"+str(script_dir) + f"{RESET} > ")
    except KeyboardInterrupt:
        exit_terminal()

    input_components = shlex.split(inp)

    input_package = input_components[0]

    if os.path.exists(script_dir / "installed" / input_package):
        if not (input_package in sys.modules):
            load_package(input_package)

        attributes = {}
        flags = []

        attribute = False

        for i in range(len(input_components)):
            if i !=0:
                if input_components[i][0]=="-":
                    flags.append(input_components[i])
                else:
                    if attribute == False:
                        attribute = input_components[i]
                    else:
                        attributes[attribute] = input_components[i]
                        attribute = False

        if attribute is not False:
            print("Command not completed: " + attribute)
        else:
            sys.modules[input_package].run(attributes,flags)
    else:
        if term_function.commands.get(str(input_package).lower()):
            term_function.commands.get(str(input_package).lower())()
        else:
            print("Command '"+input_package+"' not found!")
            print("Use 'help' for help")