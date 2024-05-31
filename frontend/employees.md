## Employees

<|layout|columns=3 3 3|class_name=align-columns-center|
<|Add +|button|on_action=on_btn_add_employee_clicked|class_name=margin|>
|>

<|{employee_data}|table|properties=employee_properties|on_action=on_btn_employee_view_clicked|>

<|dialog|open={show_add_employee_dialog}|page=addemployee|labels=Add;Cancel|close_label=Cancel|on_action=on_add_employee_finish|title=Add Employee|>
<|dialog|open={show_employee_dialog}|title=Employee Info|page=employeeinfo|labels=Cancel;|close_label=Close|width=50%|on_action=on_show_employee_close|>