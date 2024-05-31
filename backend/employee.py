from taipy.gui import notify
from model.employee import Employee
from utils.uploadfile import upload_file
import pandas as pd


show_add_employee_dialog = False
show_employee_dialog = False
employee_name = ""
employee_dob = ""
employee_email = ""
employee_phone = ""
employee_address = ""
employee_status = ""
employee_id_card = ""
employee_id_card_back = ""
employee_selfie = ""
employee_list = None
employee_data = pd.DataFrame({
    "No":[],
    "name": [],
    "dob": [],
    "email": [],
    "phone": [],
    "address": [],
    "status": [],
})
selected_employee = {
    "id":0,
    "name":"",
    "dob":"",
    "email":"",
    "phone":"",
    "address":"",
    "id_front_name":"",
    "id_back_name":"",
    "selfie_name":"",
    "status":"",
}

def on_add_employee_finish(state, action, payload):
    if payload['args'][0] == 0:
        do_add_employee(state)
    else:
        state.show_add_employee_dialog = False
        
def on_btn_add_employee_clicked(state):
    state.show_add_employee_dialog = True

def load_employee_list(state):
    state.employee_list = pd.DataFrame(Employee.getEmployees(), columns=["id", "name", "dob", "email", "phone", "address", "id_front_name","id_back_name", "selfie_name", "status"])
    state.employee_list['No'] = range(1, len(state.employee_list) + 1)
    new_employee_data = state.employee_list[["No", "name", "dob", "email", "phone", "address", "status"]]
    state.employee_data = new_employee_data.copy()
    
def do_edit_employee(state, action, payload):
    currentIndex = payload["index"] # row index
    index = int(state.employee_list.loc[currentIndex]['id'])
    col = payload["col"] # column name
    value = payload["value"] # new value cast to the column type
    user_value = payload["user_value"] # new value as entered by the 
    
    if Employee.editById(index, col, user_value):
        old_value = state.employee_data.loc[currentIndex, col]
        new_employee_data = state.employee_data.copy()
        new_employee_data.loc[currentIndex, col] = user_value
        state.employee_list.loc[currentIndex,col] = user_value
        state.employee_data = new_employee_data
        state.employee_list.loc[currentIndex, col] = user_value
        notify(state, "I", f"Edited value from '{old_value}' to '{user_value}'. (index '{index}', column '{col}')")
        
    else:
        notify(state,"W", "Email already exist")
        
        
def do_delete_employee(state, var_name, payload):
    currentIndex= payload['index']
    index = int(state.employee_list.loc[payload['index']]['id'])
    Employee.deleteById(index)
    state.employee_data = state.employee_data.drop(index=currentIndex)
    notify(state, message='Success')
    
def do_add_employee(state):
    
    if state.employee_name == "":
        notify(state, "W", "Please enter the employee's name")
        return
    if state.employee_dob == "":
        notify(state, "W", "Please choose employee's birthday")
        return
    if state.employee_email == "":
        notify(state, "W", "Please enter the employee's email")
        return
    if state.employee_phone == "":
        notify(state, "W", "Please enter the employee's phone number")
        return
    if state.employee_address == "":
        notify(state, "W", "Please enter the employee's address")
        return
    if state.employee_id_card == "":
        notify(state, "W", "Please upload the employee's ID front image")
        return
    if state.employee_id_card_back == "":
        notify(state, "W", "Please upload the emplyee's ID back image")
        return
    if state.employee_selfie == "":
        notify(state, "W", "Please upload the employee's Selfie")
        return
    if state.employee_status == "":
        notify(state, "W", "Please enter the employee status")
        return
    
    _employee = Employee(
        state.employee_name, 
        state.employee_dob, 
        state.employee_email, 
        state.employee_phone, 
        state.employee_address, 
        upload_file(state.employee_id_card), 
        upload_file(state.employee_id_card_back), 
        upload_file(state.employee_selfie), 
        state.employee_status)
    
    if _employee.insert_new_employee():
        load_employee_list(state)
        notify(state,"S", message='Employee added successfully!')
    else:
        notify(state,"W", "Email already exist")
    
    state.show_add_employee_dialog = False
def on_btn_employee_view_clicked(state, var_name, payload):
    currentIndex = payload['index']
    state.selected_employee.id_card_front = '/uploads/' + state.employee_list.loc[currentIndex]['id_front_name']
    state.selected_employee.id_card_back = '/uploads/' + state.employee_list.loc[currentIndex]['id_back_name']
    state.selected_employee.selfie = '/uploads/' + state.employee_list.loc[currentIndex]['selfie_name']
    state.selected_employee.id = state.employee_list.loc[currentIndex]['id']
    state.selected_employee.name = state.employee_list.loc[currentIndex]['name']
    state.selected_employee.dob = state.employee_list.loc[currentIndex]['dob']
    state.selected_employee.email = state.employee_list.loc[currentIndex]['email']
    state.selected_employee.phone = state.employee_list.loc[currentIndex]['phone']
    state.selected_employee.address = state.employee_list.loc[currentIndex]['address']
    state.selected_employee.status = state.employee_list.loc[currentIndex]['status']
    state.show_employee_dialog = True

def on_show_employee_close(state, action, payload):
    state.show_employee_dialog = False

def go_selfie_video(state, action, payload):
    state.gui._navigate(state.selected_employee.selfie)

employee_properties = {
    "class_name": "rows-bordered",
    "filter": True,
    "on_edit": do_edit_employee,
    "on_delete": do_delete_employee,
    "editable[No]": False,
    "columns" : {
        "No": {"title": "No"},
        "name": {"title": "Name"},
        "dob": {"title": "Birthday"},
        "email": {"title": "Email"},
        "phone": {"title": "Phone Number"},
        "address": {"title": "Address"},
        "status": {"title": "Status"},
    }
}