from external.local import user_presenter
from gf.config import config_service
from gf.verify import verify_service
from gf.start import start_service
from gf.open import open_service
from gf.rate import rate_service
from external.local.json_handler import get_lang
from external.web import url_handler
from sys import argv
from gf.lint import lint_service


def run():
    try:
        task_check(argv[1])()
    except KeyboardInterrupt:
        user_presenter.keyboard_interrupted()
    except (IndexError, KeyError):
        user_presenter.help_message()


def filename_maker(filename):
    try:
        if filename.startswith("./"):
            return filename.split("./")[1]
    except IndexError:
        return filename


def task_check(task_name):
    return {
        "config": config_start,
        "verify": verify_start,
        "start": start,
        "rate": rate_start,
        "help": help_message,
        "-h": help_message,
        "unsafe-open": unsafe_open_start,
        "version": version_show,
        "-v": version_show,
        "lint": lint,
        "open": open_start
    }[task_name]


def open_start():
    open_service.open_start()


def help_message():
    user_presenter.help_message()


def config_start():
    config_service.start()


def verify_start():
    verify_service.start(argv[2])


def start():
    start_service.main(url_handler.make_full_workshop_url(argv[2]))


def rate_start():
    rate_service.start(argv[2])


def unsafe_open_start():
    open_service.unsafe_opener()


def version_show():
    user_presenter.get_version_number()


def lint():
    lint_service.start(filename_maker(argv[2]))
