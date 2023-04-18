from taipy.gui import Icon
import pandas as pd

# Toggle for setting charts
ch_choice_chart = [("pie", Icon("images/icons/pie_chart.svg", "pie")),
                    ("chart", Icon("images/icons/bar_chart.svg", "chart"))]
ch_show_pie = ch_choice_chart[1][0]

ch_results = pd.DataFrame({"Monthly Production FPA":[],
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




ch_chart_md = """
<|part|render={len(scenario_selector)>0}|
<|layout|columns=1 1|columns[mobile]=1|gap=1rem|
    <|part|class_name=card mb1 p2 text_center|
<|{str(int(sum_costs_of_BO/1000))+' K'}|indicator|value={sum_costs_of_BO}|min=50_000|max=1_000|width=93%|>
**Back Order Cost**
    |>

    <|part|class_name=card mb1 p2 text_center|
<|{str(int(sum_costs_of_stock/1000))+' K'}|indicator|value={sum_costs_of_stock}|min=100_000|max=25_000|width=93%|>   
**Stock Cost**
    |>
|>


<|{pie_results.loc[['Stock FPA Cost', 'Stock FPB Cost', 'Stock RP1 Cost', 'Stock RP2 Cost', 'Purchase RP1 Cost', 'Purchase RP2 Cost', 'BO FPA Cost', 'BO FPB Cost']]}|chart|type=pie|values=values|labels=labels|render={ch_show_pie=='pie' and sm_graph_selected=='Costs'}|>
<|{ch_results}|chart|x=index|y[1]=Stock FPA Cost|y[2]=Stock FPB Cost|y[3]=Stock RP1 Cost|y[4]=Stock RP2 Cost|y[5]=Purchase RP1 Cost|y[6]=Purchase RP2 Cost|y[7]=BO FPA Cost|y[8]=BO FPB Cost|y[9]=Total Cost|render={ch_show_pie=='chart' and sm_graph_selected=='Costs'}|>
<|{pie_results.loc[['Monthly Purchase RP1', 'Monthly Purchase RP2']]}|chart|type=pie|values=values|labels=labels|render={ch_show_pie=='pie' and sm_graph_selected=='Purchases'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Purchase RP1|y[2]=Monthly Purchase RP2|render={ch_show_pie=='chart' and sm_graph_selected=='Purchases'}|>
<|{pie_results.loc[['Monthly Production FPA', 'Max Capacity FPA', 'Monthly Production FPB', 'Max Capacity FPB']]}|chart|type=pie|values=values|labels=labels|render={ch_show_pie=='pie' and sm_graph_selected=='Productions'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Production FPA|y[2]=Max Capacity FPA|line[2]=dash|y[3]=Monthly Production FPB|y[4]=Max Capacity FPB|line[4]=dash|render={ch_show_pie=='chart' and sm_graph_selected=='Productions'}|>
<|{pie_results.loc[['Monthly Stock FPA', 'Monthly Stock FPB', 'Monthly Stock RP1', 'Monthly Stock RP2']]}|chart|type=pie|values=values|labels=labels|render={ch_show_pie=='pie' and sm_graph_selected=='Stocks'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Stock FPA|y[2]=Monthly Stock FPB|y[3]=Monthly Stock RP1|y[4]=Monthly Stock RP2|render={ch_show_pie=='chart' and sm_graph_selected=='Stocks'}|>
<|{pie_results.loc[['Monthly BO FPA', 'Monthly BO FPB']]}|chart|type=pie|values=values|labels=labels|render={ch_show_pie=='pie' and sm_graph_selected=='Back Order'}|>  
<|{ch_results}|chart|x=index|y[1]=Monthly BO FPA|y[2]=Monthly BO FPB|render={ch_show_pie=='chart' and sm_graph_selected=='Back Order'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Production FPA|y[2]=Monthly Stock FPA|y[3]=Monthly BO FPA|y[4]=Max Capacity FPA|line[4]=dash|y[5]=Demand FPA|render={sm_graph_selected=='Product FPA'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Production FPB|y[2]=Monthly Stock FPB|y[3]=Monthly BO FPB|y[4]=Max Capacity FPB|line[4]=dash|y[5]=Demand FPB|render={sm_graph_selected=='Product FPB'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Stock RP1|y[2]=Monthly Purchase RP1|render={sm_graph_selected=='Product RP1'}|>
<|{ch_results}|chart|x=index|y[1]=Monthly Stock RP2|y[2]=Monthly Purchase RP2|render={sm_graph_selected=='Product RP2'}|>
|>

<no_scenario|part|render={len(scenario_selector)==0}|
#### No scenario created for the current month #### {: .mt0 .color_secondary }
|no_scenario>
"""




