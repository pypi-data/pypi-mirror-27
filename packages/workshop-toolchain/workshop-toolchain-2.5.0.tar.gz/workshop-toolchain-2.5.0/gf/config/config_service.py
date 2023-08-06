from external.local import user_presenter
from external.web import github
from github import BadCredentialsException
from gf.config.credential import Credential
from external.local.json_handler import save_credential


def start():
    credential = Credential()
    prepare_to_start(credential)
    try:
        github.get_token(credential)
        github.find_working_repo(credential)
    except BadCredentialsException as e:
        user_presenter.bad_credential()
    finish(credential)


def prepare_to_start(credential):
    credential.username, credential.password, credential.lang = user_presenter.user_pass_lang()  # nopep8
    user_presenter.start_communicating()


def finish(credential):
    save_credential(credential)
    user_presenter.token_created(credential.token)
