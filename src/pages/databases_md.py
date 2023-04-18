d_chart_csv_path = None

da_databases_md = """
<|part|class_name=container|
# Data**sources**{: .color-primary } 

<|layout|columns=3 2 1|columns[mobile]=1|class_name=align_columns_bottom|
<layout_scenario|
<|layout|columns=1 1 3|columns[mobile]=1|class_name=align_columns_bottom|
<year|
Year

<|{sm_selected_year}|selector|lov={sm_year_selector}|dropdown|width=100%|on_change=change_sm_month_selector|>
|year>

<month|
Month

<|{sm_selected_month}|selector|lov={sm_month_selector}|dropdown|width=100%|on_change=change_scenario_selector|>
|month>

<scenario|
Scenario

<|{selected_scenario}|selector|lov={scenario_selector}|dropdown|value_by_id|width=18rem|>
|scenario>
|>
|layout_scenario>

<|
Table

<|{sm_graph_selected}|selector|lov={sm_graph_selector}|dropdown|>
|>

<|{d_chart_csv_path}|file_download|name=table.csv|label=Download table|>
|>

<|part|render={len(scenario_selector)>0}|class_name=mt2|
<|{chart}|table|width=100%|rebuild|>
|>
|>
"""
