<|layout|columns=2 2|
<|part|
<|{selected_employee.id_card_front}|image|height=300px|width=100%|class_name=id_card_img|>
|>
<|part|
<|{selected_employee.id_card_back}|image|height=300px|width=100%|class_name=id_card_img|>
|>
|>

<|layout|columns=1|class_name=justify-end selfie_button_lay|
<|button|label= |on_action=go_selfie_video|class_name=selfie_button|>
|>

<|layout|columns=1 1 1|
<|layout|columns=1 7|class_name=align-columns-center employee_info_item |
<|layout|columns=1|
<|/assets/img/user.png|image|width=25px|>
|>
<|layout|columns=1|
<|text|value={selected_employee.name}|class_name=h6 text-right mb10px|>
|>
|>
<|layout|columns=1 7|class_name=align-columns-center employee_info_item|
<|layout|columns=1|
<|/assets/img/calendar.png|image|width=25px|>
|>
<|layout|columns=1|
<|text|value={selected_employee.dob}|class_name=h6 text-right mb10px|>
|>
|>
<|layout|columns=1 7|class_name=align-columns-center employee_info_item|
<|layout|columns=1|
<|/assets/img/email.png|image|width=25px|>
|>
<|layout|columns=1|
<|text|value={selected_employee.email}|class_name=h6 text-right mb10px|>
|>
|>
<|layout|columns=1 7|class_name=align-columns-center employee_info_item|
<|layout|columns=1|
<|/assets/img/phone.png|image|width=25px|>
|>
<|layout|columns=1|
<|text|value={selected_employee.phone}|class_name=h6 text-right mb10px|>
|>
|>
<|layout|columns=1 7|class_name=align-columns-center employee_info_item|
<|layout|columns=1|
<|/assets/img/address.png|image|width=25px|>
|>
<|layout|columns=1|
<|text|value={selected_employee.address}|class_name=h6 text-right mb10px|>
|>
|>
<|layout|columns=1 7|class_name=align-columns-center employee_info_item|
<|layout|columns=1|
<|/assets/img/flag.png|image|width=25px|>
|>
<|layout|columns=1|
<|text|value={selected_employee.status}|class_name=h6 text-right mb10px|>
|>
|>
|>
<|layout|columns=1 1 1|class_name=align-columns-center|
<|layout|>
<|layout|>
|>