from taipy.gui import notify
import re

from model.user import User

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def on_signup_finish(state, id, payload):
    id = payload["args"][0]

    if id == 0:
        do_signup(state)
    else:
        state.show_signup_dialog = False
    return

def do_signup(state):
    if not is_valid_email(state.email):
        notify(state, "W", "Please enter a valid email address.")
        return
    
    if state.password != state.password_confirm:
        notify(state, "W", "Passwords do not match. Please try again.")
        return
    
    new_user = User(state.email, state.password)
    
    if User.sign_up(new_user):
        notify(state, "S", "Welcome to ByteTalented, Your account has been successfully created.")
        state.show_signup_dialog = False
        state.show_signin_dialog = True
        return
    
    else:
        notify(state, "W", "Email address already in use. Please use a different email address or try logging in.")
        return

    return