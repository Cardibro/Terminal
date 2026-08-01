import sys

main_module = sys.modules["__main__"]

colors = {
    "green": '\033[92m',
    "red": '\033[91m',
    "yellow": '\033[0;33m',
    "blue": '\033[0;34m',
    "purple": '\033[0;35m',
    "cyan": '\033[0;36m',
    "white": "\033[0;37m"

}

def run(attributes, flags):
    if "-help" in flags:
        print("Use `terminal_color setcolor {color}` to set the color")
        print("User `terminal_color -list` to get the full list of colors")
        return True

    if "-list" in flags:
        for key, _ in colors.items():
            print(key)
        return True

    if attributes.get("setcolor") is not None:
        color = str(attributes.get("setcolor")).lower()
        if colors.get(color):
            main_module.COLOR = colors.get(color)
        else:
            print("Please type a valid color")
        return True

    print("Please use `terminal_color -help` for help with terminal colors")