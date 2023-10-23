from pages.compare_cycles_md import *
import taipy as tp
import os
import pandas as pd
from taipy.gui import Gui


if __name__ == "__main__":
    tp.Core().run()

    if len(tp.get_scenarios())==0:
        cc_create_scenarios_for_cycle()


from pages.compare_scenario_md import *
from pages.databases_md import *
from pages.data_visualization_md import *
from pages.shared import *
from pages.scenario_manager.scenario_manager_md import *


def create_chart(sm_results: pd.DataFrame, var: str):
    """Functions that create/update the chart table visible in the "Databases" page. This
    function is used in the "on_change" function to change the chart when the graph selected is changed.

    Args:
        sm_results (pd.DataFrame): the results database that comes from the state
        var (str): the string that has to be found in the columns that are going to be used to create the chart table

    Returns:
        pd.DataFrame: the chart with the proper columns
    """
    if var == 'Cost':
        columns = ['index'] + [col for col in sm_results.columns if var in col]
    else:
        columns = ['index'] + [col for col in sm_results.columns if var in col and 'Cost' not in col]

    chart = sm_results[columns]
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
        state.chart = create_chart(state.sm_results, str_to_select_chart)

        # If we are on the 'Databases' page, we have to create a temp CSV file
        if state.page == 'Databases':
            state.d_chart_csv_path = PATH_TO_TABLE
            state.chart.to_csv(state.d_chart_csv_path, sep=',')


def on_init(state):
    state.state_id = str(os.urandom(32))
    update_scenario_selector(state)


pages = {"/": Markdown('pages/shared.md'),
         "Data-Visualization":da_data_visualisation_md,
         "Scenario-Manager":sm_scenario_manager_md,
         "Compare-Scenarios":cs_compare_scenario_md,
         "Compare-Cycles":cc_compare_cycles_md,
         'Databases':da_databases_md
         }

if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(title="Production planning")
