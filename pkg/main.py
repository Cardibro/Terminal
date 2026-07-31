import sys

def run(attributes, flags, main):
    if attributes.install != None:
        main_module = sys.modules['__main__']
        main_module.install_package(attributes.install)
    else:
        print("Please use `pkg help` for help on installing packages")