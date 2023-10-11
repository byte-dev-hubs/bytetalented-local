from taipy import Config, Frequency
import json
from algos.algos import *

# This code produces scenario_cfg and configures our graph of execution

###############################################################################
# Data nodes
###############################################################################

# we create our first datanode, the source is csv file
path_to_demand = 'data/time_series_demand.csv'
demand_cfg = Config.configure_data_node(id="demand",
                                storage_type="csv", 
                                path=path_to_demand,
                                has_header=True)

with open('data/fixed_variables_default.json') as f:
    fixed_variables_default = json.load(f)

# creation of our second datanode that will have as a default data our fixed_variables_default
# this is this datanode that we will write on when we submit other values for fixed_variable
fixed_variables_cfg = Config.configure_data_node(id="fixed_variables", default_data = fixed_variables_default)

solver_name_cfg = Config.configure_data_node(id="solver_name", default_data="Default")

# here are the datanodes that keep track of the model : the model_created datanode, the model_solved datanode
model_created_cfg = Config.configure_data_node(id="model_created")
model_solved_cfg = Config.configure_data_node(id="model_solved")

# and this is the datanode that will be used to get our results from the main code
results_cfg = Config.configure_data_node(id="results")

###############################################################################
# Tasks
###############################################################################

# (demand_cfg,fixed_variables_cfg) -> |create_model| -> (model_created_cfg)
create_model_task = Config.configure_task(id="create_model",
                            input=[demand_cfg,fixed_variables_cfg],
                            function=create_model,
                            output=[model_created_cfg])

# (model_created_cfg, solver_name_cfg) -> |solve_model| -> (model_solved_cfg)
solve_model_cfg = Config.configure_task(id="solve_model",
                                    input=[model_created_cfg, solver_name_cfg],
                                    function=solve_model,
                                    output=[model_solved_cfg])

# (model_solved_cfg,fixed_variables_cfg,demand_cfg) -> |create_results| -> (results_cfg)
create_results_cfg = Config.configure_task(id="create_results",
                                       input=[model_solved_cfg,fixed_variables_cfg,demand_cfg],
                                       function=create_results,
                                       output=[results_cfg])


###############################################################################
# Scenario config
###############################################################################

scenario_cfg = Config.configure_scenario(id="scenario",task_configs=[create_model_task,solve_model_cfg,create_results_cfg], frequency=Frequency.MONTHLY)

Config.export("config/config.toml")
