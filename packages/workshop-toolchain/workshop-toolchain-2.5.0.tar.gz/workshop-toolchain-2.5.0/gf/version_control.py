import sys
from gf.settings import VERSION_FILE
from gf.verify.subprocess_adapter import run, is_windows_platform
from gf.verify.command_data import CommandData


def open_file():
    try:
        with open(VERSION_FILE, "r") as file:
            return file.read().split(".")
    except FileNotFoundError:
        print(VERSION_FILE + " not found")


def save_to_file(function):
    try:
        with open(VERSION_FILE, 'w') as file:
            file.write(str(function))
    except FileNotFoundError:
        print(VERSION_FILE + " not found")


def version_update(case):
    data = open_file()
    dictionary = {
        "major": 0,
        "minor": 1,
        "patch": 2
    }
    data[dictionary[case]] = str(int(data[dictionary[case]]) + 1)
    save_to_file(".".join(data))


def get_version():
    try:
        with open(VERSION_FILE, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(VERSION_FILE + " not found")


def version_number():
    call = CommandData('pip search workshop-toolchain')
    result = run(call)
    result = result.stdout.decode("utf-8")
    result_list = result.split("\n")
    for res in result_list:
        if "workshop-toolchain" in res:
            final = res
    return final.capitalize().split("  -")[0]


if __name__ == '__main__':
    try:
        version_update(sys.argv[1])
    except KeyError:
        print("Invalid argument")
