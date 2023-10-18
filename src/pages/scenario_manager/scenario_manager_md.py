from pages.shared import update_scenario_selector

from taipy.gui import notify, invoke_long_callback, Markdown
import taipy as tp
from config.config import scenario_cfg
import datetime as dt
import pandas as pd

from config.config import fixed_variables_default
from taipy.gui import Icon
import pandas as pd

# Toggle for setting charts
sm_choice_chart = [("pie", Icon("images/icons/pie_chart.svg", "pie")),
                    ("chart", Icon("images/icons/bar_chart.svg", "chart"))]
sm_show_pie = sm_choice_chart[1][0]

sm_results = pd.DataFrame({"Monthly Production FPA":[],
                          "Monthly Stock FPA": [],
                          "Monthly BO FPA": [],
                          "Max Capacity FPA": [],
                          
                          "Monthly Production FPB": [],
                          "Monthly Stock FPB": [],
                          "Monthly BO FPB": [],
                          "Max Capacity FPB": [],
                          
                          "Monthly Stock RP1":[],
                          "Monthly Stock RP2":[],
                          
                          "Monthly Purchase RP1":[],
                          "Monthly Purchase RP2":[],
                          
                          "Demand FPA": [],
                          "Demand FPB": [],
                          
                          'Stock FPA Cost': [],
                          'Stock FPB Cost': [],
                          
                          'Stock RP1 Cost': [],
                          'Stock RP2 Cost': [],
                          
                          'Purchase RP1 Cost': [],
                          'Purchase RP2 Cost': [],
                          
                          "BO FPA Cost":[],
                          "BO FPB Cost":[],
                          
                          "Total Cost": [],
                          "index": []})


pie_results = pd.DataFrame(
        {
            "values": [1] * len(list(sm_results.columns)),
            "labels": list(sm_results.columns)
        }, index=list(sm_results.columns)
        )


chart = sm_results[['index',
                    'Purchase RP1 Cost',
                    'Stock RP1 Cost',
                    'Stock RP2 Cost',
                    'Purchase RP2 Cost',
                    'Stock FPA Cost',
                    'Stock FPB Cost',
                    'BO FPA Cost',
                    'BO FPB Cost',
                    'Total Cost']]

sm_param_selector = ['Capacity Constraints','Objective Weights','Initial Parameters']
sm_param_selected = sm_param_selector[0]


# Toggle for choosing the sliders
sm_choice_product_param = [("product_RPone", Icon("images/P1.png", "product_RPone")),
                    ("product_RPtwo", Icon("images/P2.png", "product_RPtwo")),
                    ("product_FPA", Icon("images/PA.png", "product_FPA")),
                    ("product_FPB", Icon("images/PB.png", "product_FPB"))]
sm_product_param = 'Else'


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


fixed_variables = fixed_variables_default


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

    name = f"{dt.datetime.now().strftime('%d-%b-%Y')} Nb : {len(state.scenario_selector)}"
    scenario = tp.create_scenario(scenario_cfg, name=name)
    scenario.properties['user'] = state.state_id

    # update the scenario selector
    update_scenario_selector(state)
    state.selected_scenario = scenario

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

    # setting the scenario with the right parameters
    old_fixed_variables = state.selected_scenario.fixed_variables.read()
    if old_fixed_variables != state.fixed_variables._dict:
        state.selected_scenario.fixed_variables.write(state.fixed_variables._dict)
        
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
    state.sm_results = state.selected_scenario.results.read()
    state.pie_results = pd.DataFrame(
        {
            "values": state.sm_results.sum(axis=0),
            "labels": list(state.sm_results.columns)
        })

    state.sum_costs = state.sm_results['Total Cost'].sum()

    bool_costs_of_stock = [c for c in state.sm_results.columns if 'Cost' in c and\
                                                                  'Total' not in c and\
                                                                  'Stock' in c]
    state.sum_costs_of_stock = int(state.sm_results[bool_costs_of_stock].sum(axis=1)\
                                                                        .sum(axis=0))

    bool_costs_of_BO = [c for c in state.sm_results.columns if 'Cost' in c and\
                                                                'Total' not in c and\
                                                                'BO' in c]
    state.sum_costs_of_BO = int(state.sm_results[bool_costs_of_BO].sum(axis=1)\
                                                                  .sum(axis=0))


sm_scenario_manager_md = Markdown('pages/scenario_manager/scenario_manager.md')
