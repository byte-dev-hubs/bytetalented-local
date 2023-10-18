<|toggle|theme|>

<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>




<|Need any help?|button|on_action={lambda s: s.assign('dialog_help', True)}|id=help_button|>

<|{dialog_help}|dialog|title=Walkthough|on_action=validate_help|labels=Go!|id=dialog_help|width=100%|

<|container|
## Page 1: Data Visualization
Upon registering with a new account (name & password), the first page is displayed.

The primary chart depicts future demand for finished products A (FPA) 
and B (FPB) over the next 11 months, with the current month marked as month 0.


Just above the chart, by clicking "Expand here," you can access an expandable 
Taipy front-end containing initial production data at time 0 (current month): 
stock & production levels, incoming raw material orders, and demand, all presented in a table.



## Page 2: Scenario Manager

Create, configure, and optimize production scenarios.
This is the application's main page, where users can create new scenarios, 
adjust scenario parameters (on the 'Scenario Configuration' side of the page), 
and re-submit scenarios for re-optimization based on modified parameters.
Initially, no scenario is available, and the Year/Month corresponds to the current month.

### Creating your first scenario

The purpose of the model is to generate a production plan (level of production 
for both products) for the the next 11 months in order to:

- Meet the demand for the finished product
- Respect the Capacity Constraints
- Minimize 2 cost functions:

    - Back ordering costs: the costs of not meeting the demand on time
    - Stock costs: costs of storing raw and finished products.

It is worth noting that these 2 cost functions are kind of opposite:
if I have a lot of stock, I should easily meet the demand. Conversely,
a low inventory may put the demand in jeopardy.
When creating a first scenario, two key indicators , "Back Order Cost"
and "Stock Cost," appear above an empty main chart (no plan generated yet).


Click on "New Scenario" to launch the optimization algorithm, which 
quickly finds the optimal production levels, respecting the capacity 
constraints and optimizing costs. 
Results can be displayed as time series or pie charts, and different 
graphs can be selected by choosing the data to display (costs, productions, etc.).


### Modifying the Parameters
On the right-hand side of this panel, you can modify various parameters categorized into three sections:

- **Capacity Constraints**: Modify capacity values for different products (finished and raw).
- **Objectives Weights**: Emphasize minimizing a specific cost (stock or backordering).
- **Initial Parameters**: Modify other parameters like Initial Stock and Unit Cost.
By "Playing" with these parameters, you can create several scenarios.



## Page 3: Compare Scenarios
To Compare two scenarios, select them then click on the "compare scenario" button. 
You can select different comparison metrics  such as costs, purchases, and production levels, etc.


## Page 4: Compare Cycles

This demo also introduces the concept of ‘Cycles". 
In this manufacturing context, the cycle is monthly. 
This implies that scenarios are created each month. 
Only one of the generated scenarios will be chosen as the 
‘official scenario', this scenario is referred as the "Primary" scenario. 

This demo already contains many scenarios generated from the 
previous months. The "Evolution of costs" bar chart displays 
the performance for every single "primary' scenario generated 
every month for the past few years. Compare monthly stock and 
backorder costs from January 2021 to the present month using stacked bar charts.


## Page 5: Datasources

Access and display various tables associated with 
a selected scenario. Conveniently download data tables in CSV format.
|>
|>