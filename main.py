import sys
import os
import importlib.util
from pathlib import Path
import term_function

COLOR = '\033[92m'
RESET = '\033[0m'

script_dir = Path(__file__).resolve().parent

def load_package(package_name):
    spec = importlib.util.spec_from_file_location(package_name, script_dir / package_name / "main.py")
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

def exit_terminal():
    print(f"\n> {COLOR}Exiting...{RESET} <")
    exit()

while True:
    try:
        inp = input(f"{COLOR}"+str(script_dir) + f"{RESET} > ")
    except KeyboardInterrupt:
        exit_terminal()

    input_components = inp.split(" ")

    input_package = input_components[0]

    if os.path.exists(script_dir / input_package):
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
        if term_function.commands.get(input_package):
            term_function.commands.get(input_package)()
        else:
            print("Command '"+input_package+"' not found!")
            print("Use 'help' for help")
    

#pkg install /home/carter/PythonProjects/.terminal_packages/test.zip