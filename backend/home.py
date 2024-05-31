from taipy.gui import State, Markdown, navigate
from datetime import datetime, timedelta
from backend.signin import *
from backend.signup import *
from backend.bidlog import *
from backend.supportcandidates import *
from backend.employee import *
from backend.timeweather import *
from utils.checksignin import check_login

show_signin_dialog = False
show_signup_dialog = False

email = ""
password = ""
password_confirm = ""

pages = {
    "/": Markdown("frontend/home.md"),
    "dashboard": Markdown("frontend/dashboard.md"),
    "employees": Markdown("frontend/employees.md"),
    "bidlog": Markdown("frontend/bidlog.md"),
    "supportcandidates": Markdown("frontend/supportcandidates.md"),
    "project": Markdown("frontend/project.md"),
    "timeweather": Markdown("frontend/timeweather.md"),
    "signin": Markdown("frontend/dialog/signin.md"),
    "signup": Markdown("frontend/dialog/signup.md"),
    'addbid': Markdown('frontend/dialog/addbid.md'),
    'addcandidate': Markdown('frontend/dialog/addcandidate.md'),
    'addemployee': Markdown('frontend/dialog/addemployee.md'),
    "addtimezone": Markdown('frontend/dialog/addtimezone.md'),
    'candinfo': Markdown('frontend/dialog/candinfo.md'),
    'employeeinfo': Markdown('frontend/dialog/employeeinfo.md'),
}

def on_btn_signin_clicked(state):
    state.show_signin_dialog = True
    return

def on_btn_signup_clicked(state):
    state.show_signup_dialog = True
    return

def on_btn_signout_clicked(state):
    state.signed_in = False
    return

def on_menu_clicked(state, action, payload):
    cheked_sign = check_login(state)
    
    if payload['args'][0] != 'dashboard':
        
        if cheked_sign == None:
            notify(state, "W", "Please sign in first.")
            return
        
        elif cheked_sign == False:
            notify(state, "W", "Your session has expired. Please sign in again.")
            return
        
    if (cheked_sign == None or check_login == False) and  payload['args'][0] != 'dashboard':
        return
    
    page = payload["args"][0]
    navigate(state, page)
    
    if page == 'bidlog':
        load_bid_list(state)
    if page == 'supportcandidates' and state.signed_in:
        load_candidate_list(state)
    if page == 'employees' and state.signed_in:
        load_employee_list(state)
    if page == 'timeweather' and state.signed_in:
        load_time_weather(state)
        if not state.timer_flag:
            state.timer_flag = True
            start_timer(state)
    return

def on_navigate(state, page):
    if state.signed_in and page != 'dashboard' and page != 'signin' and page != 'signup':
        check_login(state)
    return page