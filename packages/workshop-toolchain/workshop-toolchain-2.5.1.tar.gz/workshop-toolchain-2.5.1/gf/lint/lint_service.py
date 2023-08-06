from external.local.file_operator import get_extension
from external.local.file_operator import does_exist
from external.local.user_presenter import show_lint_result
from os import system
import sys


def prepare_to_lint(filename):
    does_exist(filename)


def lint(command):
    return system(command)


def start(filename):
    lint_commands = {
        "py": "pycodestyle",
        "js": "jslint"
    }
    prepare_to_lint(filename)
    result = lint(lint_commands[get_extension(filename)] + " " + filename)
    show_lint_result(result)
