import subprocess
import sys

main_file = sys.modules["__main__"]

def cmd_clear():
    subprocess.run("clear")

def cmd_help():
    print("Use `clear` to clear the terminal")
    print("Use `exit` to exit the terminal")
    print("Use `help` to repeat help")

def cmd_exit():
    print(f"> {main_file.COLOR}Exiting...{main_file.RESET} <")
    exit()

commands = {
    "clear": cmd_clear,
    "help": cmd_help,
    "exit": cmd_exit
}