# importation of Taipy core
import taipy as tp

# Backend import of my python code | to create scenario, we need the original pipeline_cfg and scenario_cfg
# fixed_variables_default is used as the default values for the fixed variables
from config.config import fixed_variables_default


# importation of useful functions for Taipy frontend
from taipy.gui import Gui, notify, Icon, navigate

from login.login import *



# Frontend import of my python code | importation of the pages : compare_scenario_md page, scenario_manager_md page, databases_md page
# the * is used because sometimes we need the functions and/or variables
# in this code too
from pages.compare_cycles_md import *
from pages.compare_scenario_md import *
from pages.databases_md import *
from pages.data_visualization_md import *
from pages.scenario_manager_md import *


# import to create the temporary file
import pathlib

# this path is used to create a temporary file that will allow us to
# download a table in the Datasouces page
tempdir = pathlib.Path(".tmp")
tempdir.mkdir(exist_ok=True)
PATH_TO_TABLE = str(tempdir / "table.csv")


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
    state.sm_tree_dict, state.sm_year_selector, state.sm_month_selector = create_time_selectors()
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

                with open('login/login.json', 'w') as f:
                    json.dump(users, f)
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
         'images/chart_menu.svg',
         'Data Visualization')),
    ("Scenario-Manager",
     Icon(
         'images/Scenario.svg',
         'Scenario Manager')),
    ("Compare-Scenarios",
     Icon(
         'images/compare.svg',
         'Compare Scenarios')),
    ("Compare-Cycles",
     Icon(
         'images/Cycle.svg',
         'Compare Cycles')),
    ('Databases',
     Icon(
         'images/Datanode.svg',
         'Databases'))]


pages = {
    "/":login_md + "<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|id=menu_id|>",
    "Data-Visualization": da_data_visualisation_md,
    "Scenario-Manager": sm_scenario_manager_md,
    "Compare-Scenarios": cs_compare_scenario_md,
    "Compare-Cycles": cc_compare_cycles_md,
    "Databases": da_databases_md,
}


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
        columns = [
            'index'] + [col for col in ch_results.columns if var in col and 'Cost' not in col]

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
            fixed_temp = tp.get(state.selected_scenario).fixed_variables.read()
            state_fixed_variables = state.fixed_variables._dict.copy()
            for key in state.fixed_variables.keys():
                state_fixed_variables[key] = fixed_temp[key]
            state.fixed_variables = state_fixed_variables
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

        if state.sm_graph_selected == 'Costs':
            str_to_select_chart = 'Cost'
            state.cost_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Purchases':
            str_to_select_chart = 'Purchase'
            state.purchase_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Productions':
            str_to_select_chart = 'Production'
            state.production_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Stocks':
            str_to_select_chart = 'Stock'
            state.stock_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Back Order':
            str_to_select_chart = 'BO'
            state.bo_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Product FPA':
            str_to_select_chart = 'FPA'
            state.fpa_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Product FPB':
            str_to_select_chart = 'FPB'
            state.fpb_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Product RP1':
            str_to_select_chart = 'RP1'
            state.rp1_data = create_chart(state.ch_results, str_to_select_chart)
            
        elif state.sm_graph_selected == 'Product RP2':
            str_to_select_chart = 'RP2'
            state.rp2_data = create_chart(state.ch_results, str_to_select_chart)

        state.chart = create_chart(state.ch_results, str_to_select_chart)
        state.partial_table.update_content(state, da_create_display_table_md(str_to_select_chart.lower() + '_data'))


        # if we are on the 'Databases' page, we have to create an temporary csv
        # file
        if state.page == 'Databases':
            state.d_chart_csv_path = PATH_TO_TABLE
            state.chart.to_csv(state.d_chart_csv_path, sep=',')




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
        navigate(state, state.page)
    except BaseException:
        print("Warning : No args were found")

    # security on the 'All' option of sm_graph_selected that can be selected
    # only on the 'Databases' page
    if state.page != 'Databases' and state.sm_graph_selected == 'All':
        state.sm_graph_selected = 'Costs'

###############################################################################
# Initialization
###############################################################################

def initialize_variables():
    # initial value of chart
    global scenario, pie_results, sum_costs, sum_costs_of_stock, sum_costs_of_BO, scenario_counter,\
        cost_data, stock_data, purchase_data, production_data, fpa_data, fpb_data, bo_data, rp1_data, rp2_data, chart, ch_results,\
        chart, scenario_selector, selected_scenario, selected_scenario_is_primary, scenario_selector_two, selected_scenario_two,\
        fixed_variables, sm_tree_dict, sm_year_selector, sm_month_selector

    cc_create_scenarios_for_cycle()

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

    cost_data = create_chart(ch_results, 'Cost')
    purchase_data = create_chart(ch_results, 'Purchase')
    production_data = create_chart(ch_results, 'Production')
    stock_data = create_chart(ch_results, 'Stock')
    bo_data = create_chart(ch_results, 'BO')
    fpa_data = create_chart(ch_results, 'FPA')
    fpb_data = create_chart(ch_results, 'FPB')
    rp1_data = create_chart(ch_results, 'RP1')
    rp2_data = create_chart(ch_results, 'RP2')

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

    sm_tree_dict, sm_year_selector, sm_month_selector = create_time_selectors()





##########################################################################
# Creation of state and initial values
##########################################################################
if __name__ == "__main__":
    tp.Core().run()

    initialize_variables()

    pd.read_csv('data/time_series_demand copy.csv').to_csv('data/time_series_demand.csv')

    # the initial page is the "Scenario Manager" page
    page = "Data Visualization"

    gui = Gui(pages=pages, css_file='main')
    partial_table = gui.add_partial(da_display_table_md)

    # value of width and height for tables
    width_table = "100%"
    height_table = "100%"

    # value of width and height for charts
    width_chart = "100%"
    height_chart = "60vh"

    gui.run(title="Production planning", dark_mode=False)
