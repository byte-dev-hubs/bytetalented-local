## Time and Weather

<|layout|columns=3 3 3|class_name=align-columns-center|
<|+ Add|button|on_action=on_btn_add_time_zone_clicked|class_name=margin|>
|>

<|layout|columns=1 1 1 1 1|


<|part|render={city_count > 0}|
<|layout|columns=1|class_name=timezone|
<|layout|columns=1|
<|layout|columns=1|class_name=justify-end|
<|button|label= |on_action=remove_timezone|class_name=remove_timezone_btn|id=remove_btn_1|>
|>
<|layout|columns=1|class_name=|>
<|text|value={city_data[0]["time"]}|class_name=time_header h4|>
|>
<|layout|columns=1|
<|text|value={city_data[0]["city"]} |class_name=text-center h5|>
<|text|value={city_data[0]["country"]} |class_name=text-center h5|>
|>

<|layout|columns=1|
<|image|content={weather_icons[0]}|class_name=weather_img|width=100%|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Description:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[0]['weather']['description']}|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Temperature:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[0]['weather']['temperature']}C|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Humidity:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[0]['weather']['humidity']}%|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Wind Speed:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[0]['weather']['wind_speed']} m/s|class_name=text-right h6|>
|>
|>
|>
|>

<|part|render={city_count > 1}|
<|layout|columns=1|class_name=timezone|
<|layout|columns=1|
<|layout|columns=1|class_name=justify-end|
<|button|label= |on_action=remove_timezone|class_name=remove_timezone_btn|id=remove_btn_1|>
|>
<|layout|columns=1|class_name=|>
<|text|value={city_data[1]["time"]}|class_name=time_header h4|>
|>
<|layout|columns=1|
<|text|value={city_data[1]["city"]} |class_name=text-center h5|>
<|text|value={city_data[1]["country"]} |class_name=text-center h5|>
|>

<|layout|columns=1|
<|image|content={weather_icons[1]}|class_name=weather_img|width=100%|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Description:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[1]['weather']['description']}|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Temperature:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[1]['weather']['temperature']}C|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Humidity:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[1]['weather']['humidity']}%|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Wind Speed:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[1]['weather']['wind_speed']} m/s|class_name=text-right h6|>
|>
|>
|>
|>

<|part|render={city_count > 2}|
<|layout|columns=1|class_name=timezone|
<|layout|columns=1|
<|layout|columns=1|class_name=justify-end|
<|button|label= |on_action=remove_timezone|class_name=remove_timezone_btn|id=remove_btn_2|>
|>
<|layout|columns=1|class_name=|>
<|text|value={city_data[2]["time"]}|class_name=time_header h4|>
|>
<|layout|columns=1|
<|text|value={city_data[2]["city"]} |class_name=text-center h5|>
<|text|value={city_data[2]["country"]} |class_name=text-center h5|>
|>

<|layout|columns=1|
<|image|content={weather_icons[2]}|class_name=weather_img|width=100%|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Description:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[2]['weather']['description']}|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Temperature:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[2]['weather']['temperature']}C|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Humidity:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[2]['weather']['humidity']}%|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Wind Speed:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[2]['weather']['wind_speed']} m/s|class_name=text-right h6|>
|>
|>
|>
|>

<|part|render={city_count > 3}|
<|layout|columns=1|class_name=timezone|
<|layout|columns=1|
<|layout|columns=1|class_name=justify-end|
<|button|label= |on_action=remove_timezone|class_name=remove_timezone_btn|id=remove_btn_3|>
|>
<|layout|columns=1|class_name=|>
<|text|value={city_data[3]["time"]}|class_name=time_header h4|>
|>
<|layout|columns=1|
<|text|value={city_data[3]["city"]} |class_name=text-center h5|>
<|text|value={city_data[3]["country"]} |class_name=text-center h5|>
|>

<|layout|columns=1|
<|image|content={weather_icons[3]}|class_name=weather_img|width=100%|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Description:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[3]['weather']['description']}|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Temperature:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[3]['weather']['temperature']}C|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Humidity:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[3]['weather']['humidity']}%|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Wind Speed:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[3]['weather']['wind_speed']} m/s|class_name=text-right h6|>
|>
|>
|>
|>

<|part|render={city_count > 4}|
<|layout|columns=1|class_name=timezone|
<|layout|columns=1|
<|layout|columns=1|class_name=justify-end|
<|button|label= |on_action=remove_timezone|class_name=remove_timezone_btn|id=remove_btn_4|>
|>
<|layout|columns=1|class_name=|>
<|text|value={city_data[4]["time"]}|class_name=time_header h4|>
|>
<|layout|columns=1|
<|text|value={city_data[4]["city"]} |class_name=text-center h5|>
<|text|value={city_data[4]["country"]} |class_name=text-center h5|>
|>

<|layout|columns=1|
<|image|content={weather_icons[4]}|class_name=weather_img|width=100%|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Description:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[4]['weather']['description']}|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Temperature:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[4]['weather']['temperature']}C|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Humidity:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[4]['weather']['humidity']}%|class_name=text-right h6|>
|>
|>
<|layout|columns=4 6|
<|layout|columns=1|
<|text|value=Wind Speed:|class_name=h6|>
|>
<|layout|columns=1|
<|text|value={city_data[4]['weather']['wind_speed']} m/s|class_name=text-right h6|>
|>
|>
|>
|>



|>

<|dialog|open={show_add_time_dialog}|page=addtimezone|labels=Add;Cancel|close_label=Cancel|on_action=on_add_time_finish|title=Add Time Zone|width=30%|>