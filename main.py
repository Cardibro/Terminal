import sys
import os
import zipfile
import importlib.util
from pathlib import Path

script_dir = Path(__file__).resolve().parent

def load_package(file_path, package_name):
    spec = importlib.util.spec_from_file_location(package_name, script_dir / package_name / "main.py")
    package = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = package
    spec.loader.exec_module(package)
    return package

def install_package(file_path, package_name):
    os.mkdir(package_name)
    with zipfile.ZipFile(file_path,'r') as zip_ref:
        zip_ref.extractall(path = script_dir / package_name)

install_package("/home/carter/PythonProjects/.terminal_packages/test.zip", "test_package")

while True:
    inp = input()
    

#test_package = load_package("/home/carter/PythonProjects/.terminal_packages/test/main.py", "test_package")