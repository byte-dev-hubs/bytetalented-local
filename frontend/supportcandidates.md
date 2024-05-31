## Support Candidates

<|layout|columns=3 3 3|class_name=align-columns-center|
<|+ Add|button|on_action=on_btn_add_candidate_clicked|class_name=margin|>
|>
<|{candidate_data}|table|properties=candidate_properties|on_action=on_btn_cand_view_clicked|>

<|dialog|open={show_add_cand_dialog}|page=addcandidate|labels=Add;Cancel|close_label=Cancel|on_action=on_add_candidate_finish|title=Add Support Candidate|>
<|dialog|open={show_cand_dialog}|title=Candidate Info|page=candinfo|labels=Cancel;|close_label=Close|width=40%|on_action=on_show_cand_close|>
