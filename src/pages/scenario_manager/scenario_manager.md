<|container|
# **Scenario**{: .color-primary } Manager

<|layout|columns=8 4 auto|
    <layout_scenario|
        <|layout|columns=1 1 3|
Year <|{sm_selected_year}|selector|lov={sm_year_selector}|dropdown|on_change=change_sm_month_selector|>

Month <|{sm_selected_month}|selector|lov={sm_month_selector}|dropdown|on_change=change_scenario_selector|>

**Scenario** <|{selected_scenario}|selector|lov={scenario_selector}|dropdown|adapter=adapt_scenarios|width=18rem|class_name=success|>
        |>
    |layout_scenario>


Graph <|{sm_graph_selected}|selector|lov={sm_graph_selector}|dropdown|>

<toggle_chart|
Pie/Line chart

<|{sm_show_pie}|toggle|lov={sm_choice_chart}|value_by_id|active={not 'Product ' in sm_graph_selected}|>
|toggle_chart>
|>

---

<|layout|columns=9 3|gap=1.5rem|

<|part|render={len(scenario_selector)>0}|
<|layout|columns=1 1|gap=1rem|
    <|part|class_name=card mb1 p2 text_center|
<|{str(int(sum_costs_of_BO/1000))+' K'}|indicator|value={sum_costs_of_BO}|min=50_000|max=1_000|width=93%|>
**Back Order Cost**
    |>

    <|part|class_name=card mb1 p2 text_center|
<|{str(int(sum_costs_of_stock/1000))+' K'}|indicator|value={sum_costs_of_stock}|min=100_000|max=25_000|width=93%|>   
**Stock Cost**
    |>
|>


<|{pie_results.loc[['Stock FPA Cost', 'Stock FPB Cost', 'Stock RP1 Cost', 'Stock RP2 Cost', 'Purchase RP1 Cost', 'Purchase RP2 Cost', 'BO FPA Cost', 'BO FPB Cost']]}|chart|type=pie|values=values|labels=labels|render={sm_show_pie=='pie' and sm_graph_selected=='Costs'}|>

<|{sm_results}|chart|x=index|y[1]=Stock FPA Cost|y[2]=Stock FPB Cost|y[3]=Stock RP1 Cost|y[4]=Stock RP2 Cost|y[5]=Purchase RP1 Cost|y[6]=Purchase RP2 Cost|y[7]=BO FPA Cost|y[8]=BO FPB Cost|y[9]=Total Cost|render={sm_show_pie=='chart' and sm_graph_selected=='Costs'}|>

<|{pie_results.loc[['Monthly Purchase RP1', 'Monthly Purchase RP2']]}|chart|type=pie|values=values|labels=labels|render={sm_show_pie=='pie' and sm_graph_selected=='Purchases'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Purchase RP1|y[2]=Monthly Purchase RP2|render={sm_show_pie=='chart' and sm_graph_selected=='Purchases'}|>

<|{pie_results.loc[['Monthly Production FPA', 'Max Capacity FPA', 'Monthly Production FPB', 'Max Capacity FPB']]}|chart|type=pie|values=values|labels=labels|render={sm_show_pie=='pie' and sm_graph_selected=='Productions'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Production FPA|y[2]=Max Capacity FPA|line[2]=dash|y[3]=Monthly Production FPB|y[4]=Max Capacity FPB|line[4]=dash|render={sm_show_pie=='chart' and sm_graph_selected=='Productions'}|>

<|{pie_results.loc[['Monthly Stock FPA', 'Monthly Stock FPB', 'Monthly Stock RP1', 'Monthly Stock RP2']]}|chart|type=pie|values=values|labels=labels|render={sm_show_pie=='pie' and sm_graph_selected=='Stocks'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Stock FPA|y[2]=Monthly Stock FPB|y[3]=Monthly Stock RP1|y[4]=Monthly Stock RP2|render={sm_show_pie=='chart' and sm_graph_selected=='Stocks'}|>

<|{pie_results.loc[['Monthly BO FPA', 'Monthly BO FPB']]}|chart|type=pie|values=values|labels=labels|render={sm_show_pie=='pie' and sm_graph_selected=='Back Order'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly BO FPA|y[2]=Monthly BO FPB|render={sm_show_pie=='chart' and sm_graph_selected=='Back Order'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Production FPA|y[2]=Monthly Stock FPA|y[3]=Monthly BO FPA|y[4]=Max Capacity FPA|line[4]=dash|y[5]=Demand FPA|render={sm_graph_selected=='Product FPA'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Production FPB|y[2]=Monthly Stock FPB|y[3]=Monthly BO FPB|y[4]=Max Capacity FPB|line[4]=dash|y[5]=Demand FPB|render={sm_graph_selected=='Product FPB'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Stock RP1|y[2]=Monthly Purchase RP1|render={sm_graph_selected=='Product RP1'}|>

<|{sm_results}|chart|x=index|y[1]=Monthly Stock RP2|y[2]=Monthly Purchase RP2|render={sm_graph_selected=='Product RP2'}|>
|>

<no_scenario|part|render={len(scenario_selector)==0}|
#### No scenario created for the current month #### {: .mt0 .color_secondary }
|no_scenario>
 

<|mt2|
<|{sm_param_selected}|selector|lov={sm_param_selector}|class_name=fullwidth|>


<|part|render={sm_param_selected == 'Capacity Constraints'}|

<|{sm_product_param}|toggle|lov={sm_choice_product_param}|value_by_id|class_name=mb1 text_center|>


<|part|render={sm_product_param == 'product_FPA'}|
Max Capacity FPA : *<|{fixed_variables.Max_Capacity_FPA}|>*
<|{fixed_variables.Max_Capacity_FPA}|slider|min=332|max=1567|active={sm_show_config_scenario}|>

Max Capacity of FPA and FPB : *<|{fixed_variables.Max_Capacity_of_FPA_and_FPB}|>*
<|{fixed_variables.Max_Capacity_of_FPA_and_FPB}|slider|min=598|max=2821|active={sm_show_config_scenario}|>
|>

<|part|render={sm_product_param == 'product_FPB'}|
Max Capacity FPB : *<|{fixed_variables.Max_Capacity_FPB}|>*
<|{fixed_variables.Max_Capacity_FPB}|slider|min=332|max=1567|active={sm_show_config_scenario}|>

Max Capacity of FPA and FPB : *<|{fixed_variables.Max_Capacity_of_FPA_and_FPB}|>*
<|{fixed_variables.Max_Capacity_of_FPA_and_FPB}|slider|min=598|max=2821|active={sm_show_config_scenario}|>
|>
<|part|render={sm_product_param == 'product_RPone'}|

Max Stock RP1 : *<|{fixed_variables.Max_Stock_RPone}|>*
<|{fixed_variables.Max_Stock_RPone}|slider|min=28|max=132|active={sm_show_config_scenario}|>
|>
<|part|render={sm_product_param == 'product_RPtwo'}|

Max Stock RP2 : *<|{fixed_variables.Max_Stock_RPtwo}|>*
<|{fixed_variables.Max_Stock_RPtwo}|slider|min=21|max=99|active={sm_show_config_scenario}|>
|>
|>

<|part|render={sm_param_selected == 'Objective Weights'}|
Weight of Stock : *<|{fixed_variables.Weight_of_Stock}|>*
<|{fixed_variables.Weight_of_Stock}|slider|min=35|max=165|active={sm_show_config_scenario}|>

Weight of Back Order : *<|{fixed_variables.Weight_of_Back_Order}|>*
<|{fixed_variables.Weight_of_Back_Order}|slider|min=35|max=165|active={sm_show_config_scenario}|>
|>

<|part|render={sm_param_selected == 'Initial Parameters'}|
<|{sm_product_param}|toggle|lov={sm_choice_product_param}|value_by_id|class_name=mb1 text_center|>


<|part|render={sm_product_param == 'product_FPA'}|
Unit Cost - FPA Back Order : *<|{fixed_variables.cost_FPA_Back_Order}|>*
<|{fixed_variables.cost_FPA_Back_Order}|slider|min=70|max=330|active={sm_show_config_scenario}|>

Unit Cost - FPA Stock : *<|{fixed_variables.cost_FPA_Stock}|>*
<|{fixed_variables.cost_FPA_Stock}|slider|min=15|max=74|active={sm_show_config_scenario}|>

Initial Back Order FPA : *<|{fixed_variables.Initial_Back_Order_FPA}|>*
<|{fixed_variables.Initial_Back_Order_FPA}|slider|min=0|max=50|active={sm_show_config_scenario}|>

Initial Stock FPA : *<|{fixed_variables.Initial_Stock_FPA}|>*
<|{fixed_variables.Initial_Stock_FPA}|slider|min=10|max=49|active={sm_show_config_scenario}|>

Initial Production FPA : *<|{fixed_variables.Initial_Production_FPA}|>*
<|{fixed_variables.Initial_Production_FPA}|slider|min=297|max=1402|active={sm_show_config_scenario}|>
|>

<|part|render={sm_product_param == 'product_FPB'}|
Unit Cost - FPB Back Order : *<|{fixed_variables.cost_FPB_Back_Order}|>*
<|{fixed_variables.cost_FPB_Back_Order}|slider|min=87|max=412|active={sm_show_config_scenario}|>

Unit Cost - FPB Stock : *<|{fixed_variables.cost_FPB_Stock}|>*
<|{fixed_variables.cost_FPB_Stock}|slider|min=14|max=66|active={sm_show_config_scenario}|>

Initial Back Order FPB : *<|{fixed_variables.Initial_Back_Order_FPB}|>*
<|{fixed_variables.Initial_Back_Order_FPB}|slider|min=8|max=41|active={sm_show_config_scenario}|>

Initial Stock FPB : *<|{fixed_variables.Initial_Stock_FPB}|>*
<|{fixed_variables.Initial_Stock_FPB}|slider|min=0|max=50|active={sm_show_config_scenario}|>

Initial Production FPB : *<|{fixed_variables.Initial_Production_FPB}|>*
<|{fixed_variables.Initial_Production_FPB}|slider|min=280|max=1320|active={sm_show_config_scenario}|>
|>

<|part|render={sm_product_param == 'product_RPone'}|
Initial Stock RP1 : *<|{fixed_variables.Initial_Stock_RPone}|>*
<|{fixed_variables.Initial_Stock_RPone}|slider|min=10|max=49|active={sm_show_config_scenario}|>

Unit Cost - RP1 Stock : *<|{fixed_variables.cost_RPone_Stock}|>*
<|{fixed_variables.cost_RPone_Stock}|slider|min=10|max=49|active={sm_show_config_scenario}|>

Unit Cost - RP1 Purchase : *<|{fixed_variables.cost_RPone_Purchase}|>*
<|{fixed_variables.cost_RPone_Purchase}|slider|min=35|max=165|active={sm_show_config_scenario}|>

Initial Purchase RP1 : *<|{fixed_variables.Initial_Purchase_RPone}|>*
<|{fixed_variables.Initial_Purchase_RPone}|slider|min=12|max=57|active={sm_show_config_scenario}|>
|>

<|part|render={sm_product_param == 'product_RPtwo'}|
Initial Stock RP2 : *<|{fixed_variables.Initial_Stock_RPtwo}|>*
<|{fixed_variables.Initial_Stock_RPtwo}|slider|min=14|max=66|active={sm_show_config_scenario}|>

Unit Cost - RP2 Stock : *<|{fixed_variables.cost_RPtwo_Stock}|>*
<|{fixed_variables.cost_RPtwo_Stock}|slider|min=21|max=99|active={sm_show_config_scenario}|>

Unit Cost - RP2 Purchase : *<|{fixed_variables.cost_RPtwo_Purchase}|>*
<|{fixed_variables.cost_RPtwo_Purchase}|slider|min=52|max=247|active={sm_show_config_scenario}|>

Initial Purchase RP2 : *<|{fixed_variables.Initial_Purchase_RPtwo}|>*
<|{fixed_variables.Initial_Purchase_RPtwo}|slider|min=14|max=66|active={sm_show_config_scenario}|>
|>
|>


<|Delete|button|on_action=delete_scenario_fct|active={len(scenario_selector)>0 and sm_show_config_scenario}|class_name=fullwidth error mb_half|>
<|Make Primary|button|on_action=make_primary|active={len(scenario_selector)>0 and not selected_scenario.is_primary and sm_show_config_scenario}|class_name=fullwidth secondary mb_half|>
<|Re-optimize|button|on_action=submit_scenario|active={len(scenario_selector)>0 and sm_show_config_scenario}|class_name=fullwidth secondary mb_half|>
<|New scenario|button|on_action=create_new_scenario||active={sm_show_config_scenario}|class_name=fullwidth plain mb_half|>
|>
|>

|>
