import subprocess

def cmd_clear():
    subprocess.run("clear")

def cmd_help():
    print("Use `clear` to clear the terminal")
    print("Use `exit` to exit the terminal")
    print("Use `help` to repeat help")

def cmd_exit():
    exit()

commands = {
    "clear": cmd_clear,
    "help": cmd_help,
    "exit": cmd_exit
}