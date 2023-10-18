from taipy.gui import notify, navigate, Icon
import taipy as tp
import datetime as dt

# User id
state_id = None

# Metrics for scenario manager and comparison
sum_costs = 0
sum_costs_of_stock = 0
sum_costs_of_BO = 0
sum_costs_of_BO = 0

# Navigation
page = "Data Visualization"

menu_lov = [("Data-Visualization", Icon('images/icons/visualize.svg', 'Data Visualization')),
            ("Scenario-Manager", Icon('images/icons/scenario.svg', 'Scenario Manager')),
            ("Compare-Scenarios", Icon('images/icons/compare.svg', 'Compare Scenarios')),
            ("Compare-Cycles", Icon('images/icons/cycle.svg', 'Compare Cycles')),
            ('Databases', Icon('images/icons/data_base.svg', 'Databases'))]


def menu_fct(state, var_name: str, var_value):
    """Functions that is called when there is a change in the menu control

    Args:
        state (_type_): the state object of Taipy
        var_name (str): the changed variable name
        var_value (_type_): the changed variable value
    """

    # change the value of the state.page variable in order to render the
    # correct page
    state.page = var_value['args'][0]
    navigate(state, to=state.page)


    # security on the 'All' option of sm_graph_selected that can be selected
    # only on the 'Databases' page
    if state.page != 'Databases' and state.sm_graph_selected == 'All':
        state.sm_graph_selected = 'Costs'


# Functions for scenarios
def adapt_scenarios(scenario):
    return 'Primary ' + scenario.name if scenario.is_primary else scenario.name


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
    """
    This function is called when the user changes the year selector. It updates the selector shown on the GUI
    for the month selector and is calling the same function for the scenario selector.
    

    Args:
        state (State): all the GUI variables
    """
    state.sm_month_selector = list(state.sm_tree_dict[state.sm_selected_year].keys())

    if state.sm_selected_month not in state.sm_month_selector:
        state.sm_selected_month = state.sm_month_selector[0]

    change_scenario_selector(state)


def change_scenario_selector(state):
    """
    This function is called when the user changes the month selector. It updates the selector shown on the GUI
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
    else:
        state.sm_show_config_scenario = True

def update_scenario_selector(state):
    """
    This function will update the scenario selectors. It will be used when
    we create a new scenario. If there is a scenario that is created, we will
    add its (id,name) in this list.

    Args:
        scenarios (list): a list of tuples (scenario,properties)
    """
    state.scenario_selector = [s for s in tp.get_scenarios() if 'user' in s.properties and\
                                                                 state.state_id == s.properties['user']]
    state.scenario_selector_two = state.scenario_selector.copy()
    sm_tree_dict[state.sm_selected_year][state.sm_selected_month] = state.scenario_selector

scenario_selector = []
selected_scenario = None

scenario_selector_two = []
selected_scenario_two = None

# Initialization of scenario tree
sm_tree_dict = {}

sm_current_month = dt.date.today().strftime('%b')
sm_current_year = dt.date.today().strftime('%Y')

sm_selected_year = sm_current_year
sm_selected_month = sm_current_month

sm_tree_dict, sm_year_selector, sm_month_selector = create_time_selectors()


# Help
dialog_help = False

def restore_state(state):
    state.cs_show_comparison = False
    update_scenario_selector(state)
    notify(state, 'info', 'Restoring your session')


def validate_help(state, action, payload):
    state.dialog_help = False
