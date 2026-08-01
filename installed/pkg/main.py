import sys
import os
import zipfile
import tempfile
from pathlib import Path
import shutil
import json
import urllib.request

INDEX_URL = "https://raw.githubusercontent.com/cardibro/package-index/main/index.json"

script_dir = Path(__file__).resolve().parent.parent.parent
main_module = sys.modules["__main__"]

RED='\033[91m'
GREEN='\033[92m'
RESET='\033[0m'

def get_package_index():
    try:
        with urllib.request.urlopen(INDEX_URL,timeout=10) as response:
            return json.loads(response.read())
    except urllib.error.URLError as e:
        main_module.error(f"Failed to fetch package index: {e}")
        return None

index_data = get_package_index()
packages_by_name = {pkg["name"]: pkg for pkg in index_data}

def run(attributes, flags):
    if "-help" in flags:
        print("Use `pkg install {/path/to/package}` to install a package")
        print("Use `pkg remove {package_name}` to remove a package")
        return True
    
    if attributes.get("install") is not None:
        install_package(attributes.get("install"))
        return True

    if attributes.get("remove") is not None:
        remove_package(attributes.get("remove"))
        return True

    print("Please use `pkg -help` for help with packages")

def find_dependencies(package_name, deps):
    package_info = packages_by_name.get(package_name)
    if package_info is None:
        main_module.warn(f"Package '{package_name}' not found")
        return False

    for dep in package_info.get("dependencies", []):
        if dep not in deps:
            deps.append(dep)
            find_dependencies(dep, deps)

    return True

def download_repo_zip(owner, repo, branch, destination):
    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = Path(tmp_dir) / "repo.zip"
        urllib.request.urlretrieve(url, zip_path)

        with zipfile.ZipFile(zip_path) as z:
            z.extractall(tmp_dir)

        extracted_items = [p for p in Path(tmp_dir).iterdir() if p.is_dir()]
        
        if not extracted_items:
            raise RuntimeError("No folder found after extracting zip")
        
        extracted_folder = extracted_items[0]

        shutil.copytree(str(extracted_folder), str(destination))

def install_package(package_name):
    package_info = packages_by_name.get(package_name)
    if package_info is None:
        main_module.error(f"Package '{package_name}' not found")
        return False
    else:
        if os.path.exists(script_dir / "installed" /package_name):
            main_module.warn("Package already installed at " + str(script_dir) + "/" + package_name)
            return False
        deps = []
        find_dependencies(package_name, deps)

        if deps is not None:
            main_module.warn(f"'{package_name}' requires {len(deps)} dependenc(ies)!")
            
            for index, dep in enumerate(deps):
                if os.path.exists(script_dir / dep):
                    print(f"{GREEN}Dependency {index+1}: '{dep}' (INSTALLED){RESET}")
                else:
                    main_module.warn(f"Dependency {index+1}: '{dep}'")
        if main_module.confirmation("Are you sure you want to install '" + package_name + "' and it's dependencies? "):
            download_repo_zip(package_info["owner"], package_info["repo"], package_info["branch"], package_info["destination"])

            print(f"Package '{package_name}' successfully installed")
        else:
            print(f"Package '{package_name}' was not installed")

def remove_package(package_name):
    try:
        if main_module.confirmation("Are you sure you want to remove '" + package_name + "'?"):
            shutil.rmtree(script_dir / "installed" / package_name)
            print(f"Package '{package_name}' successfully removed")
        else:
            print(f"Package '{package_name}' was not removed")
    except FileNotFoundError:
        main_module.error("Package not found")
    except PermissionError:
        main_module.error("No permission")