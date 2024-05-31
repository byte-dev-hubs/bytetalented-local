<|layout|columns=1|
<|layout|columns=7 4 1|class_name=align-columns-center|
<|layout|columns=1|
# Byte**Talented**{: .color-primary} International - CRM
|>
<|layout|columns=1|
<|part|render={not signed_in}|
<|layout|columns=2 1 1|class_name=align-columns-center|
<|part|
#
|>
<|part|
<|Sign In|button|on_action=on_btn_signin_clicked|class_name=fullwidth|>
|>
<|part|
<|Sign Up|button|on_action=on_btn_signup_clicked|class_name=fullwidth|>
|>
|>
|>
<|part|render={signed_in}|
<|layout|columns=3 1|class_name=align-columns-center|
<|layout|columns=1|class_name=taipy-align-items-center|
<|part|
### Welcome ### {: .h3 .m0 .pr1 .text-right}
|>
<|part|class_name=taipy-justify-content-end|
<|{email}|text|class_name=text-right pr1 text-fullwidth|>
|>
|>
<|Sign Out|button|class_name=fullwidth|on_action=on_btn_signout_clicked|>
|>
|>
|>
<|toggle|theme|class_name=nolabel|>
|>
|>
<|dialog|title=Sign In|open={show_signin_dialog}|page=signin|labels=SignIn;Cancel|close_label=Cancel|on_action=on_signin_finish|>
<|dialog|title=Sign Up|open={show_signup_dialog}|page=signup|labels=Signup;Cancel|close_label=Cancel|on_action=on_signup_finish|>

<|menu|lov={[("dashboard", "Dashboard"), ("employees", "Employees"), ("bidlog", "Bid Log"), ("supportcandidates", "Support Candidate"), ("project", "Project"),("timeweather", "Time and Weather")]}|on_action=on_menu_clicked|>