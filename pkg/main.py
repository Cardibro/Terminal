import sys
import os
import zipfile
from pathlib import Path
import shutil

script_dir = Path(__file__).resolve().parent.parent
main_module = sys.modules["__main__"]

def run(attributes, flags):
    if "-help" in flags:
        print("Use `pkg install {/path/to/package}` to install a package")
        print("Use `pkg remove {package_name}` to remove a package")
        print("Use `pkg -help` to repeat help with packages")
        return True
    
    if attributes.get("install") is not None:
        install_package(attributes.get("install"))
        return True

    if attributes.get("remove") is not None:
        remove_package(attributes.get("remove"))
        return True

    print("Please use `pkg -help` for help with packages")

def install_package(file_path):
    try:
        package_name = os.path.splitext(os.path.basename(file_path))[0]
        
        with zipfile.ZipFile(file_path,'r') as zip_ref:
                

                if main_module.confirmation("Are you sure you want to install '" + package_name + "'?"):
                    os.mkdir(package_name)
                    zip_ref.extractall(path = script_dir / package_name)

                    print(f"Package '{package_name}' successfully installed")
                else:
                    print(f"Package '{package_name}' was not installed")
    except FileNotFoundError:
        print("File path not found")
    except FileExistsError:
        print("File path does not exist")
    except PermissionError:
        print("No permission")

def remove_package(package_name):
    try:
        if main_module.confirmation("Are you sure you want to remove '" + package_name + "'?"):
            shutil.rmtree(script_dir / package_name)
            print(f"Package '{package_name}' successfully removed")
        else:
            print(f"Package '{package_name}' was not removed")
    except FileNotFoundError:
        print("Package not found")
    except PermissionError:
        print("No permission")