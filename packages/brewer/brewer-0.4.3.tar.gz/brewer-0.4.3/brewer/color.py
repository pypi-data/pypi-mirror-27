HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def red(string):
    print(FAIL + string + END)
    return True

def pink(string):
    print(HEADER + string + END)
    return True

def blue(string):
    print(OKBLUE + string + END)
    return True

def green(string):
    print(OKGREEN + string + END)
    return True

def yellow(string):
    print(WARNING + string + END)
    return True

def bold(string):
    print(BOLD + string + END)
    return True

def underline(string):
    print(UNDERLINE + string + END)
    return True


if __name__ == '__main__':
    print("Default")
    red("Red")
    pink("Pink")
    blue("Blue")
    green("Green")
    yellow("Yellow")
    bold("Bold")
    underline("Underline")
