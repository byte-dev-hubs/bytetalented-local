import taipy as tp
from taipy.gui import Icon


import datetime as dt
import os
import hashlib
import json



login = ''
password = ''
dialog_login = False
dialog_new_account = False
new_account = False

all_scenarios = tp.get_scenarios()

users = {}

with open('login/login.json', 'w') as f:
    json.dump(users, f)

dialog_user = True
user_selector = [('Create new user',Icon('/images/new_account.png','Create new user'))]
user_in_session = ''
selected_user = None

salt = os.urandom(32)

def actualize_users_list(state):
    with open('login/login.json', "r") as f:
        state.users = json.load(f)
    state.user_selector = [(user, Icon('images/user.png', user)) for user in state.users.keys()]
    
    state.user_selector += [('Create new user', Icon('images/new_account.png', 'Create new user'))]


def open_dialog_user(state):
    state.login = ''
    state.dialog_user = True


def encode(password):
    key = str(hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    ))
    return key


def test_password(users, login, new_password):
    old_key = users[login]['password']

    new_key = str(hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        new_password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    ))

    return old_key == new_key




login_md = """
<|part|id=part_login|
Welcome, <|{login}|button|on_action=open_dialog_user|id=login_button|> !
|>

<|{dialog_user}|dialog|width=20%|title=Set account|id=dialog_user|on_action=exit_login|
<|{selected_user}|selector|lov={user_selector}|on_change=on_change_user_selector|id=user_selector|width=100%|value_by_id|>
|>

<|{dialog_login}|dialog|on_action=validate_login|title=Login|labels=Cancel; Login|id=dialog_user|width=20%|

<|{selected_user}|selector|lov={[(login, Icon('/images/user.png', login))]}|id=user_selected|width=100%|value_by_id|>

Password

<|{password}|input|password|>
|>



<|{dialog_new_account}|dialog|title=Register|on_action=validate_login|labels=Cancel; Register|id=dialog_user|width=20%|
Username <|{login}|input|>

Password <|{password}|input|password=True|>
|>
"""