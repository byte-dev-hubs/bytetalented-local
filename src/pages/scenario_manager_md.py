from pages.annex_scenario_manager.chart_md import ch_chart_md, ch_choice_chart, ch_show_pie, ch_results
from pages.annex_scenario_manager.parameters_md import pa_parameters_md, pa_param_selector, pa_param_selected, pa_choice_product_param, pa_product_param, solver_name, list_of_solvers

from pages.shared import  update_scenario_selector

from taipy.gui import notify, invoke_long_callback
import taipy as tp
from config.config import scenario_cfg
import datetime as dt
import pandas as pd

sm_scenario_manager_md = """
<|container|
# **Scenario**{: .color-primary } Manager

<|layout|columns=8 4 auto auto|columns[mobile]=1|class_name=align_columns_bottom|
    <layout_scenario|
        <|layout|columns=1 1 3|columns[mobile]=1|class_name=align_columns_bottom|
Year <|{sm_selected_year}|selector|lov={sm_year_selector}|dropdown|on_change=change_sm_month_selector|>

Month <|{sm_selected_month}|selector|lov={sm_month_selector}|dropdown|on_change=change_scenario_selector|>

Scenario <|{selected_scenario}|selector|lov={scenario_selector}|dropdown|adapter=adapt_scenarios|width=18rem|>
        |>
    |layout_scenario>

Graph <|{sm_graph_selected}|selector|lov={sm_graph_selector}|dropdown|>

<toggle_chart|
Pie/Line chart

<|{ch_show_pie}|toggle|lov={ch_choice_chart}|value_by_id|active={not 'Product ' in sm_graph_selected}|>
|toggle_chart>

<br/>
<|{'Hide Configuration' if sm_show_config_scenario else 'Show Configuration'}|button|on_action={lambda s: s.assign('sm_show_config_scenario', not s.sm_show_config_scenario)}|active={sm_selected_month == sm_current_month and sm_selected_year == sm_current_year}|>
|>

<|part|render={sm_show_config_scenario}|class_name=mt2|
""" + pa_parameters_md + """
|>

<|part|render={not(sm_show_config_scenario)}|class_name=mt2|
""" + ch_chart_md + """
|>
|>
"""

# Button for configuring scenario
sm_show_config_scenario = True


# Choose the graph to display
sm_graph_selector = [
    'Costs',
    'Purchases',
    'Productions',
    'Stocks',
    'Back Order',
    'Product RP1',
    'Product RP2',
    'Product FPA',
    'Product FPB']
sm_graph_selected = sm_graph_selector[0]




def make_primary(state):
    tp.set_primary(state.selected_scenario)
    update_scenario_selector(state)
    state.selected_scenario = state.selected_scenario


def delete_scenario_fct(state):
    if state.selected_scenario.is_primary:
        notify(
            state,
            "warning",
            "You can't delete the primary scenario of the month")
    else:
        tp.delete(state.selected_scenario.id)
        update_scenario_selector(state)

        if len(state.scenario_selector) != 0:
            state.selected_scenario = state.scenario_selector[0]


def create_new_scenario(state):
    """
    This function is used whan the 'create' button is pressed in the scenario_manager_md page.
    See the scenario_manager_md page for more information. It will configure another scenario,
    create it and submit it.

    Args:
        state (_type_): the state object of Taipy
    """

    print("Creating scenario...")
    name = f"{dt.datetime.now().strftime('%d-%b-%Y')} Nb : {len(state.scenario_selector)}"
    scenario = tp.create_scenario(scenario_cfg, name=name)
    scenario.properties['user'] = state.login

    # update the scenario selector
    print("Updating scenario selector...")
    update_scenario_selector(state)
    state.selected_scenario = scenario

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

    # setting the scenario with the right parameters
    old_fixed_variables = state.selected_scenario.fixed_variables.read()
    if old_fixed_variables != state.fixed_variables._dict:
        state.selected_scenario.fixed_variables.write(state.fixed_variables._dict)
    if state.solver_name != state.selected_scenario.solver_name.read():
        state.selected_scenario.solver_name.write(state.solver_name)
    # running the scenario in a long callback and update variables
    invoke_long_callback(state, submit_heavy, [state.selected_scenario], submit_status)


def update_variables(state):
    """This function is only used in the submit_scenario or when the selected_scenario changes. It will update all the useful variables that we want to update.

    Args:
        state (_type_): the state object of Taipy
    """
    # it will set the sliders to the right values when a scenario is changed
    state.fixed_variables = state.selected_scenario.fixed_variables.read()


    # read the result
    state.ch_results = state.selected_scenario.pipelines['pipeline'].results.read()
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


