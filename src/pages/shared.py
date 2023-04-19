from taipy.gui import Icon, notify 
import taipy as tp
from login.login import *
import json
import datetime as dt

def adapt_scenarios(scenario):
    return 'Primary '+scenario.name if scenario.is_primary else scenario.name


def create_sm_tree_dict(scenarios, sm_tree_dict: dict = None):
    """This function creates a tree dict from a list of scenarios. The levels of the tree are:
    year/month/scenario

    Args:
        scenarios (list): a list of scenarios
        sm_tree_dict (dict, optional): the tree gathering all the scenarios. Defaults to None.

    Returns:
        tree: the tree created to classify the scenarios
    """
    print("Creating tree dict...")
    if sm_tree_dict is None:
        # Initialize the tree dict if it is not already initialized
        sm_tree_dict = {}

    # Add all the scenarios that are in the list
    for scenario in scenarios:
        # Create a name for the cycle
        date = scenario.creation_date
        year = f"{date.strftime('%Y')}"
        period = f"{date.strftime('%b')}"

        # Add the cycle if it was not already added
        if year not in sm_tree_dict:
            sm_tree_dict[year] = {}
        if period not in sm_tree_dict[year]:
            sm_tree_dict[year][period] = []

        sm_tree_dict[year][period] += [scenario]

    return sm_tree_dict



def create_time_selectors():
    """This function creates the time selectors that will be displayed on the GUI and it is also creating 
    the tree dict gathering all the scenarios.

    Returns:
        dict: the tree dict gathering all the scenarios
        list: the list of years
        list: the list of months
    """
    all_scenarios_ordered = sorted(tp.get_scenarios(), key=lambda x: x.creation_date.timestamp())

    sm_tree_dict = create_sm_tree_dict(all_scenarios_ordered)

    if sm_current_year not in list(sm_tree_dict.keys()):
        sm_tree_dict[sm_current_year] = {}
    if sm_current_month not in sm_tree_dict[sm_current_year]:
        sm_tree_dict[sm_current_year][sm_current_month] = []

    sm_year_selector = list(sm_tree_dict.keys())
    sm_month_selector = list(sm_tree_dict[sm_selected_year].keys())

    return sm_tree_dict, sm_year_selector, sm_month_selector


def change_sm_month_selector(state):
    """This function is called when the user changes the year selector. It updates the selector shown on the GUI
    for the month selector and is calling the same function for the scenario selector.
    

    Args:
        state (State): all the GUI variables
    """
    state.sm_month_selector = list(state.sm_tree_dict[state.sm_selected_year].keys())

    if state.sm_selected_month not in state.sm_month_selector:
        state.sm_selected_month = state.sm_month_selector[0]

    change_scenario_selector(state)


def change_scenario_selector(state):
    """This function is called when the user changes the month selector. It updates the selector shown on the GUI
    for the scenario selector.
    

    Args:
        state (State): all the GUI variables
    """
    state.scenario_selector = list(state.sm_tree_dict[state.sm_selected_year][state.sm_selected_month])
    state.scenario_selector_two = state.scenario_selector.copy()
    if len(state.scenario_selector) > 0:
        state.selected_scenario = state.scenario_selector[0]

    if (state.sm_selected_month != sm_current_month or\
            state.sm_selected_year != sm_current_year) and\
            state.sm_show_config_scenario:

        state.sm_show_config_scenario = False
        notify(state, "info", "This scenario is historical, you can't modify it")

def update_scenario_selector(state):
    """
    This function will update the scenario selectors. It will be used when
    we create a new scenario. If there is a scenario that is created, we will
    add its (id,name) in this list.

    Args:
        scenarios (list): a list of tuples (scenario,properties)
    """

    state.scenario_selector = [s for s in tp.get_scenarios() if 'user' in s.properties and\
                                                                 state.login == s.properties['user']]
    state.scenario_selector_two = state.scenario_selector.copy()
    sm_tree_dict[state.sm_selected_year][state.sm_selected_month] = state.scenario_selector



sm_tree_dict = {}

sm_current_month = dt.date.today().strftime('%b')
sm_current_year = dt.date.today().strftime('%Y')

sm_selected_year = sm_current_year
sm_selected_month = sm_current_month

sm_tree_dict, sm_year_selector, sm_month_selector = create_time_selectors()

###############################################################################
# Login
###############################################################################
def exit_login(state):
    global user_selector
    if state.selected_user in [user[0] for user in user_selector]:
        state.login = state.selected_user

        if state.selected_user in state.user_in_session:
            state.dialog_user = False

            reinitialize_state_after_login(state)
    else:
        notify(state, "Warning", "You must login first!")

def on_change_user_selector(state):
    global user_selector
    if state.selected_user == 'Create new user':
        state.login = ''
        state.dialog_new_account = True
    elif state.selected_user in [user[0] for user in user_selector]:
        state.login = state.selected_user

        if state.selected_user in state.user_in_session:
            state.dialog_user = False

            reinitialize_state_after_login(state)
        else:
            state.dialog_login = True

    else:
        notify(state, "Warning", "Unexpected error")


def reinitialize_state_after_login(state):
    state.cs_show_comparaison = False
    state.password = ''
    update_scenario_selector(state)

    if state.dialog_new_account:
        state.selected_scenario = ""
        notify(state, 'info', 'Creating a new session')
        state.dialog_new_account = False
    else:
        if len(state.scenario_selector) != 0:
            state.selected_scenario = state.scenario_selector[0]

        notify(state, 'info', 'Restoring your session')


def validate_login(state, id, action, payload):
    global user_selector, users

    # if the button pressed is "Cancel"
    if payload['args'][0] != 1:
        state.dialog_login = False
        state.dialog_new_account = False
    else:
        if state.dialog_new_account:
            if state.login in [user[0] for user in user_selector]:
                notify(state, 'error', 'This user already exists')
            elif state.login == '':
                notify(state, "Warning", "Please enter a valid login")
            elif state.login != '' and len(state.password) > 0:
                state.dialog_login = False
                state.dialog_new_account = False
                state.dialog_user = False

                users[state.login] = {}
                users[state.login]["password"] = encode(state.password)
                users[state.login]["last_visit"] = str(dt.datetime.now())

                with open('login/login.json', 'w') as f:
                    json.dump(users, f)
                reinitialize_state_after_login(state)

                state.user_selector = [(state.login ,Icon('images/user.png', state.login))] + state.user_selector
                user_selector = state.user_selector
                state.selected_user = state.login

                state.user_in_session += state.selected_user
        elif state.login in [user[0] for user in user_selector]:
            if test_password(users, state.login, state.password):
                state.dialog_login = False
                state.dialog_new_account = False
                state.dialog_user = False
                state.user_in_session += state.selected_user

                reinitialize_state_after_login(state)
            else:
                notify(state, "Warning", "Wrong password")

        else:
            notify(state, "Warning", "Unexpected error")

