## Bid Log
<|layout|columns=3 3 3|class_name=align-columns-center|
<|Add +|button|on_action=on_btn_add_bid_clicked|class_name=margin|>
<|{selected_bid_date}|date|on_change=bid_date_changed|class_name=margin|>
|>
<|dialog|open={show_add_bid_dialog}|title=Add Bid|page=addbid|labels=Add;Cancel|close_label=Cancel|on_action=on_add_bid_finish|>
<|{bid_data}|table|properties=bid_table_properties|>