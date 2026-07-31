import sys

def run(attributes, flags):
    if attributes.get("install") is not None:
        main_module = sys.modules['__main__']
        main_module.install_package(attributes.get("install"))
        return True

    if attributes.get("remove") is not None:
        main_module = sys.modules['__main__']
        main_module.remove_package(attributes.get("remove"))
        return True

    print("Please use `pkg help` for help with packages")