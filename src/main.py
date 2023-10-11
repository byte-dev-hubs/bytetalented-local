# Backend import of my python code | to create scenario, we need the original scenario_cfg
# fixed_variables_default is used as the default values for the fixed variables
from config.config import fixed_variables_default
from pages.compare_cycles_md import *
# importation of Taipy core
import taipy as tp

if __name__ == "__main__":
    tp.Core().run()

    if len(tp.get_scenarios())==0:
        cc_create_scenarios_for_cycle()

# basic packages of python to handle data
import pandas as pd

# importation of useful functions for Taipy frontend
from taipy.gui import Gui, Icon, navigate


# Frontend import of my python code | importation of the pages : compare_scenario_md page, scenario_manager_md page, databases_md page
# the * is used because sometimes we need the functions and/or variables
# in this code too
from pages.compare_scenario_md import *
from pages.databases_md import *
from pages.data_visualization_md import *
from pages.shared import *
from pages.scenario_manager_md import *

###############################################################################
# main_md
###############################################################################

# this is the main markdown page. We have here the other pages that are included in the main page.
# scenario_manager_md, compare_scenario_md, databases_md will be visible depending on the page variable.
# this is the purpose of the 'render' parameter.

menu_lov = [("Data-Visualization", Icon('images/icons/visualize.svg', 'Data Visualization')),
            ("Scenario-Manager", Icon('images/icons/scenario.svg', 'Scenario Manager')),
            ("Compare-Scenarios", Icon('images/icons/compare.svg', 'Compare Scenarios')),
            ("Compare-Cycles", Icon('images/icons/cycle.svg', 'Compare Cycles')),
            ('Databases', Icon('images/icons/data_base.svg', 'Databases'))]


root_md = login_md + """
<|toggle|theme|>

<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>
"""

pages = {"/":root_md,
         "Data-Visualization":da_data_visualisation_md,
         "Scenario-Manager":sm_scenario_manager_md,
         "Compare-Scenarios":cs_compare_scenario_md,
         "Compare-Cycles":cc_compare_cycles_md,
         'Databases':da_databases_md
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
    if var_name == "selected_scenario" and var_value:
        if state.selected_scenario.results.is_ready_for_reading:
            # I update all the other useful variables
            update_variables(state)

    if var_name == "dialog_user" or var_name == "dialog_login" or var_name == "dialog_new_account" or var_name == "user_selected":
        actualize_users_list(state)
    
    if var_name == 'sm_graph_selected' or var_name == "selected_scenario":
        # Update the chart table
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

        # If we are on the 'Databases' page, we have to create a temp CSV file
        if state.page == 'Databases':
            state.d_chart_csv_path = PATH_TO_TABLE
            state.chart.to_csv(state.d_chart_csv_path, sep=',')



# The initial page is the "Scenario Manager" page
page = "Data Visualization"


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


##########################################################################
# Creation of state and initial values
##########################################################################

def initialize_variables():
    # initial value of chart
    global scenario, pie_results, sum_costs, sum_costs_of_stock, sum_costs_of_BO,\
           chart, ch_results,\
           scenario_selector, selected_scenario, scenario_selector_two, selected_scenario_two,\
           fixed_variables


    fixed_variables = fixed_variables_default

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

    scenario_selector_two = []
    selected_scenario_two = None

    sm_tree_dict, sm_year_selector, sm_month_selector = create_time_selectors()


if __name__ == "__main__":
    initialize_variables()

    pd.read_csv('data/time_series_demand copy.csv').to_csv('data/time_series_demand.csv')

    gui = Gui(pages=pages)
    gui.run(title="Production planning")
