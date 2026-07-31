from pathlib import Path
import importlib.util
import zipfile
import sys
import os

script_dir = Path(__file__).resolve().parent

def load_package(package_name):
    spec = importlib.util.spec_from_file_location(package_name, script_dir / package_name / "main.py")
    package = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = package
    spec.loader.exec_module(package)
    return package

def install_package(file_path):
    package_name = os.path.splitext(os.path.basename(file_path))[0]
    os.mkdir(package_name)
    try:
        with zipfile.ZipFile(file_path,'r') as zip_ref:
                zip_ref.extractall(path = script_dir / package_name)
    except:
        print("File path not found")
        os.rmdir(package_name)

def remove_package(package_name):
    os.rmdir(script_dir / package_name)

while True:
    inp = input(str(script_dir) + " >")

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
        print("Command "+input_package+" not found!")
    

#pkg install /home/carter/PythonProjects/.terminal_packages/test.zip
