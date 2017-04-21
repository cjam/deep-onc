'''
This module manages retrieving the ONC token from a file that can be ignored by git.
This token can be retreived from: http://dmas.uvic.ca/Profile -> Web Services API
'''
import os
TOKEN_FILE_NAME = ".onc-token"
TOKEN_FILE_PATH = os.path.join("./", TOKEN_FILE_NAME)

class TokenMissingException(Exception):
    '''
    Raised when a token cannot be located.
    '''
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Could not retrieve ONC Token from {} file,"\
            "run python {} to save one".format(TOKEN_FILE_NAME, __file__)


def __get_token():
    saved_token = None
    if os.path.isfile(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, mode="r") as token_file:
            saved_token = token_file.readline()

    if not saved_token:
        raise TokenMissingException()

    return saved_token


def save_token():
    '''Saves a token to the onc token file'''
    saved_token = None
    while not saved_token:
        saved_token = input('Enter your ONC token: ')
    with open(TOKEN_FILE_PATH, mode="w") as token_file:
        token_file.write(saved_token)
        print("Token written to '{}', you should add this extension to your .gitignore".format(
            TOKEN_FILE_PATH))
    return saved_token


if __name__ == "__main__":
    save_token()
else:
    token = __get_token()