# basic packages of python to handle data
from login.login import *
import pandas as pd
from assets.mui_theme import *

# importation of Taipy core
import taipy as tp

# Backend import of my python code | to create scenario, we need the original pipeline_cfg and scenario_cfg
# fixed_variables_default is used as the default values for the fixed variables
from config.config import fixed_variables_default, scenario_cfg, pipeline_cfg
from taipy import Config


# importation of useful functions for Taipy frontend
from taipy.gui import Gui, Markdown, notify, Icon, invoke_long_callback, navigate

# Frontend import of my python code | importation of the pages : compare_scenario_md page, scenario_manager_md page, databases_md page
# the * is used because sometimes we need the functions and/or variables
# in this code too
from pages.compare_cycles_md import *
from pages.compare_scenario_md import *
from pages.databases_md import *
from pages.data_visualization_md import *

# import to create the temporary file
import pathlib


# this path is used to create a temporary file that will allow us to
# download a table in the Datasouces page
tempdir = pathlib.Path(".tmp")
tempdir.mkdir(exist_ok=True)
PATH_TO_TABLE = str(tempdir / "table.csv")

Config.configure_global_app(clean_entities_enabled=True)
tp.clean_all_entities()

tp.Core().run()

cc_create_scenarios_for_cycle()

from pages.scenario_manager_md import *


###############################################################################
# Login
###############################################################################


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
    scenarios = [s for s in tp.get_scenarios(
    ) if 'user' in s.properties and state.login == s.properties['user']]
    state.scenario_counter = len(scenarios)
    state.cs_show_comparaison = False
    state.password = ''
    update_scenario_selector(state, scenarios)

    if state.dialog_new_account:
        state.selected_scenario = None
        notify(state, 'info', 'Creating a new session')
        state.dialog_new_account = False
    else:
        if state.scenario_counter != 0:
            state.selected_scenario = state.scenario_selector[0][0]

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

                json.dump(users, open('login/login.json', 'w'))
                reinitialize_state_after_login(state)

                state.user_selector = [
                    (state.login,
                     Icon(
                         'images/user.png',
                         state.login))] + state.user_selector
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


###############################################################################
# main_md
###############################################################################

# this is the main markdown page. We have here the other pages that are included in the main page.
# scenario_manager_md, compare_scenario_md, databases_md will be visible depending on the page variable.
# this is the purpose of the 'render' parameter.
menu_lov = [
    ("Data-Visualization",
     Icon(
         'images/icons/visualize.svg',
         'Data Visualization')),
    ("Scenario-Manager",
     Icon(
         'images/icons/scenario.svg',
         'Scenario Manager')),
    ("Compare-Scenarios",
     Icon(
         'images/icons/compare.svg',
         'Compare Scenarios')),
    ("Compare-Cycles",
     Icon(
         'images/icons/cycle.svg',
         'Compare Cycles')),
    ('Databases',
     Icon(
         'images/icons/data_base.svg',
         'Databases'))]


root_md = login_md + """
<|toggle|theme|>

<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|id=menu_id|>
"""
pages = {"/":root_md,
         "Data-Visualization":da_data_visualisation_md,
         "Scenario-Manager":sm_scenario_manager_md,
         "Compare-Scenarios":cs_compare_scenario_md,
         "Compare-Cycles":cc_compare_cycles_md,
         'Databases':da_databases_md
         }


###############################################################################
# important functions to create/submit/handle scenarios
###############################################################################

def update_scenario_selector(state, scenarios: list):
    """
    This function will update the scenario selectors. It will be used when
    we create a new scenario. If there is a scenario that is created, we will
    add its (id,name) in this list.

    Args:
        scenarios (list): a list of tuples (scenario,properties)
    """

    state.scenario_selector = [(s.id, s.name) if not s.is_primary else (
        s.id, Icon('images/icons/flag.svg', s.name)) for s in scenarios]
    state.scenario_counter = len(state.scenario_selector)
    state.scenario_selector_two = state.scenario_selector.copy()

    sm_tree_dict[state.sm_selected_year][state.sm_selected_month] = state.scenario_selector


def make_primary(state):
    tp.set_primary(tp.get(state.selected_scenario))
    scenarios = [s for s in tp.get_scenarios(
    ) if 'user' in s.properties and state.login == s.properties['user']]
    update_scenario_selector(state, scenarios)
    state.selected_scenario_is_primary = True


def delete_scenario_fct(state):
    if tp.get(state.selected_scenario).is_primary:
        notify(
            state,
            "warning",
            "You can't delete the primary scenario of the month")
    else:
        tp.delete(state.selected_scenario)
        scenarios = [s for s in tp.get_scenarios(
        ) if 'user' in s.properties and state.login == s.properties['user']]
        update_scenario_selector(state, scenarios)

        if state.scenario_counter != 0:
            state.selected_scenario = state.scenario_selector[0][0]


def create_new_scenario(state):
    """
    This function is used whan the 'create' button is pressed in the scenario_manager_md page.
    See the scenario_manager_md page for more information. It will configure another scenario,
    create it and submit it.

    Args:
        state (_type_): the state object of Taipy
    """

    # update the scenario counter
    state.scenario_counter += 1

    print("Creating scenario...")
    name = dt.datetime.now().strftime('%d-%b-%Y') + " Nb : " + \
        str(state.scenario_counter)
    scenario = tp.create_scenario(scenario_cfg, name=name)
    scenario.properties['user'] = state.login

    # get all the scenarios and their properties
    print("Getting properties...")
    scenarios = [s for s in tp.get_scenarios(
    ) if 'user' in s.properties and state.login == s.properties['user']]

    # change the scenario that is selected. The new scenario is the one that
    # is selected
    state.selected_scenario = scenario.id

    # update the scenario selector
    print("Updating scenario selector...")
    update_scenario_selector(state, scenarios)

    # submit this scenario
    print("Submitting it...")
    submit_scenario(state)


def catch_error_in_submit(state):
    """
    This function is used to catch the error that can occur when we submit a scenario. When an
    error is catched, a notification will appear and variables wil be changed to avoid any error.
    The errors comes from the solution of the Cplex model where infeasible or unbounded problems
    can happen if the fixed variables are wrongly set.

    Args:
        state (_type_): the state object of Taipy
    """

    # if our initial production is higher that our max capacity of production
    if state.fixed_variables["Initial_Production_FPA"] > state.fixed_variables["Max_Capacity_FPA"]:
        state.fixed_variables["Initial_Production_FPA"] = state.fixed_variables["Max_Capacity_FPA"]
        notify(
            state,
            "warning",
            "Value of initial production FPA is greater than max production A")

    # if our initial production is higher that our max capacity of production
    if state.fixed_variables["Initial_Production_FPB"] > state.fixed_variables["Max_Capacity_FPB"]:
        state.fixed_variables["Initial_Production_FPB"] = state.fixed_variables["Max_Capacity_FPB"]
        notify(
            state,
            "warning",
            "Value of initial production FPB is greater than max production B")

    # if our initial stock is higher that our max capacity of production
    if state.fixed_variables["Initial_Stock_RPone"] > state.fixed_variables["Max_Stock_RPone"]:
        state.fixed_variables["Initial_Stock_RPone"] = state.fixed_variables["Max_Stock_RPone"]
        notify(
            state,
            "warning",
            "Value of initial stock RP1 is greater than max stock 1")

    # if our initial stock is higher that our max capacity of production
    if state.fixed_variables["Initial_Stock_RPtwo"] > state.fixed_variables["Max_Stock_RPtwo"]:
        state.fixed_variables["Initial_Stock_RPtwo"] = state.fixed_variables["Max_Stock_RPtwo"]
        notify(
            state,
            "warning",
            "Value of initial stock RP2 is greater than max stock 2")

    # if our initial productions are higher that our max capacity of
    # productions
    if state.fixed_variables["Initial_Production_FPA"] + \
            state.fixed_variables["Initial_Production_FPB"] > state.fixed_variables["Max_Capacity_of_FPA_and_FPB"]:
                
        state.fixed_variables["Initial_Production_FPA"] = int(state.fixed_variables["Max_Capacity_of_FPA_and_FPB"] / 2)
        state.fixed_variables["Initial_Production_FPB"] = int(state.fixed_variables["Max_Capacity_of_FPA_and_FPB"] / 2)
        
        notify(
            state,
            "warning",
            "Value of initial productions is greater than the max capacities")


def submit_heavy(scenario):
    tp.submit(scenario)

def submit_status(state, status):
    # update all the variables that we want to update (ch_results, pie_results
    # and metrics)
    update_variables(state)


def submit_scenario(state):
    """
    This function will submit the scenario that is selected. It will be used when the 'submit' button is pressed
    or when we create a new scenario. It checks if there is any errors then it will change the parameters of the
    problem and submit the scenario. At the end, we update all the variables that we want to update.

    Args:
        state (_type_): the state object of Taipy

    Returns:
        _type_: _description_
    """

    # see if there are errors in the parameters that will be given to the
    # scenario
    catch_error_in_submit(state)

    # getting the scenario
    scenario = tp.get(state.selected_scenario)

    # setting the scenario with the right parameters
    old_fixed_variables = scenario.fixed_variables.read()
    if old_fixed_variables != state.fixed_variables._dict:
        scenario.fixed_variables.write(state.fixed_variables._dict)
    if state.solver_name != scenario.solver_name.read():
        scenario.solver_name.write(state.solver_name)
    # running the scenario in a long callback and update variables
    invoke_long_callback(state, submit_heavy, [scenario], submit_status)


def update_variables(state):
    """This function is only used in the submit_scenario or when the selected_scenario changes. It will update all the useful variables that we want to update.

    Args:
        state (_type_): the state object of Taipy
    """
    # getting the selected scenario
    scenario = tp.get(state.selected_scenario)

    # read the result
    state.ch_results = scenario.pipelines['pipeline'].results.read()
    state.pie_results = pd.DataFrame(
        {
            "values": state.ch_results.sum(axis=0),
            "labels": list(state.ch_results.columns)
        })

    state.sum_costs = state.ch_results['Total Cost'].sum()

    bool_costs_of_stock = [c for c in state.ch_results.columns if 'Cost' in c and\
                                                                  'Total' not in c and\
                                                                  'Stock' in c]
    state.sum_costs_of_stock = int(state.ch_results[bool_costs_of_stock].sum(axis=1)\
                                                                        .sum(axis=0))

    bool_costs_of_BO = [c for c in state.ch_results.columns if 'Cost' in c and\
                                                                'Total' not in c and\
                                                                'BO' in c]
    state.sum_costs_of_BO = int(state.ch_results[bool_costs_of_BO].sum(axis=1)\
                                                                  .sum(axis=0))


def create_chart(ch_results: pd.DataFrame, var: str):
    """Functions that create/update the chart table visible in the "Databases" page. This
    function is used in the "on_change" function to change the chart when the graph selected is changed.

    Args:
        ch_results (pd.DataFrame): the results database that comes from the state
        var (str): the string that has to be found in the columns that are going to be used to create the chart table

    Returns:
        pd.DataFrame: the chart with the proper columns
    """
    if var == 'Cost':
        columns = ['index'] + [col for col in ch_results.columns if var in col]
    else:
        columns = ['index'] + [col for col in ch_results.columns if var in col and 'Cost' not in col]

    chart = ch_results[columns]
    return chart


def on_change(state, var_name, var_value):
    """This function is called whener a change in the state variables is done. When a change is seen, operations can be created
    depending on the variable changed

    Args:
        state (State): the state object of Taipy
        var_name (str): the changed variable name
        var_value (obj): the changed variable value
    """
    # if the changed variable is the scenario selected
    if var_name == "selected_scenario" and var_value is not None:
        scenario = tp.get(state.selected_scenario)

        state.selected_scenario_is_primary = scenario.is_primary

        if scenario.results.is_ready_for_reading:
            # it will set the sliders to the right values when a scenario is
            # changed
            state.fixed_variables = tp.get(state.selected_scenario).fixed_variables.read()
            # I update all the other useful variables
            update_variables(state)

    if var_name == "dialog_user" or var_name == "dialog_login" or var_name == "dialog_new_account" or var_name == "user_selected":
        with open('login/login.json', "r") as f:
            state.users = json.load(f)
        state.user_selector = [(user,Icon('images/user.png', user))
                                for user in state.users.keys()]
        
        state.user_selector += [('Create new user', Icon('images/new_account.png', 'Create new user'))]

    # if the graph selected or the scenario is changed and we are on the 'Databases' page
    # or if we go on the Database page, we have to update the chart table
    if (var_name == 'sm_graph_selected' or var_name == "selected_scenario" and state.page =='Databases')\
        or (var_name == 'page' and var_value == 'Databases'):

        str_to_select_chart = None
        chart_mapping = {
            'Costs': 'Cost',
            'Purchases': 'Purchase',
            'Productions': 'Production',
            'Stocks': 'Stock',
            'Back Order': 'BO',
            'Product FPA': 'FPA',
            'Product FPB': 'FPB',
            'Product RP1': 'RP1',
            'Product RP2': 'RP2'
        }

        str_to_select_chart = chart_mapping.get(state.sm_graph_selected)

        state.chart = create_chart(state.ch_results, str_to_select_chart)


        # if we are on the 'Databases' page, we have to create an temporary csv
        # file
        if state.page == 'Databases':
            state.d_chart_csv_path = PATH_TO_TABLE
            state.chart.to_csv(state.d_chart_csv_path, sep=',')


# the initial page is the "Scenario Manager" page
page = "Data Visualization"


def menu_fct(state, var_name: str, fct, var_value):
    """Functions that is called when there is a change in the menu control

    Args:
        state (_type_): the state object of Taipy
        var_name (str): the changed variable name
        var_value (_type_): the changed variable value
    """

    # change the value of the state.page variable in order to render the
    # correct page
    try:
        state.page = var_value['args'][0]
        navigate(state, to=state.page)
    except BaseException:
        print("Warning : No args were found")

    # security on the 'All' option of sm_graph_selected that can be selected
    # only on the 'Databases' page
    if state.page != 'Databases' and state.sm_graph_selected == 'All':
        state.sm_graph_selected = 'Costs'


##########################################################################
# Creation of state and initial values
##########################################################################
gui = Gui(pages=pages, css_file='main')

def initialize_variables():
    # initial value of chart
    global scenario, pie_results, sum_costs, sum_costs_of_stock, sum_costs_of_BO, scenario_counter,\
     chart, ch_results,\
        chart, scenario_selector, selected_scenario, selected_scenario_is_primary, scenario_selector_two, selected_scenario_two,\
        fixed_variables

    fixed_variables = fixed_variables_default

    scenario = None
    pie_results = pd.DataFrame(
        {
            "values": [1] * len(list(ch_results.columns)),
            "labels": list(ch_results.columns)
        }, index=list(ch_results.columns)
        )
    
    sum_costs = 0
    sum_costs_of_stock = 0
    sum_costs_of_BO = 0
    sum_costs_of_BO = 0
    scenario_counter = 0

    chart = ch_results[['index',
                        'Purchase RP1 Cost',
                        'Stock RP1 Cost',
                        'Stock RP2 Cost',
                        'Purchase RP2 Cost',
                        'Stock FPA Cost',
                        'Stock FPB Cost',
                        'BO FPA Cost',
                        'BO FPB Cost',
                        'Total Cost']]

    # selectors that will be displayed on the pages
    scenario_selector = []
    selected_scenario = None

    selected_scenario_is_primary = False

    scenario_selector_two = scenario_selector.copy()
    selected_scenario_two = None


if __name__ == "__main__":
    initialize_variables()

    pd.read_csv('data/time_series_demand copy.csv').to_csv('data/time_series_demand.csv')

    gui.run(title="Production planning", theme=common_theme, light_theme=light_theme, dark_theme=dark_theme)

