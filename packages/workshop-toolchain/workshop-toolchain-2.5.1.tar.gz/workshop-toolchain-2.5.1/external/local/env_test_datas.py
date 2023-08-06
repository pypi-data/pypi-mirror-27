from gf.settings import C_UNITTEST_HEADER, HAMCREST_FILENAME, JUNIT_FILENAME, JUNIT_URL, HAMCREST_URL, C_UNITTEST_URL  # nopep8


def get_test_env_datas(language):
    return {
        "javascript": [],
        "cs": [],
        "python": [],
        "java": [
            {
                "link": JUNIT_URL,
                "file_name": JUNIT_FILENAME
            },
            {
                "link": HAMCREST_URL,
                "file_name": HAMCREST_FILENAME
            }
        ],
        "c": [
            {
                "link": C_UNITTEST_URL,
                "file_name": C_UNITTEST_HEADER
            }
        ]
    }[language]
