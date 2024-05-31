from taipy.gui import Markdown, notify
from model.candidate import Candidate
from utils.getInfoFromImg import extract_info_from_image
from utils.uploadfile import upload_file
import pandas as pd

show_add_cand_dialog = False
show_cand_dialog = False
candidate_name = ""
candidate_email = ""
candidate_phone = ""
candidate_position = ""
candidate_photos = [""]
candidate_names = [""]
candidate_emails = [""]
candidate_phones = [""]
candidate_positions = [""]
candidate_list = None

candidate_data = pd.DataFrame({
    "No":[],
    "name": [],
    "email": [],
    "phone": [],
    "position": [],
    # "Action":[]
})
selected_candidate = {
    "image":"",
    "id":0,
    "name":"",
    "email":"",
    "phone":"",
    "position":"",
}

def on_show_cand_close(state):
    state.show_cand_dialog = False

def on_add_candidate_finish(state, action, payload):
    if payload['args'][0] == 0:
        do_add_candidate(state)
        state.show_add_cand_dialog = False
    else:
        state.show_add_cand_dialog = False
        
def on_btn_add_candidate_clicked(state):
    state.show_add_cand_dialog = True

def on_btn_cand_view_clicked(state, var_name, payload):
    currentIndex = payload['index']
    state.selected_candidate.image = './uploads/' + state.candidate_list.loc[currentIndex]['photo_name']
    state.selected_candidate.id = state.candidate_list.loc[currentIndex]['id']
    state.selected_candidate.name = state.candidate_list.loc[currentIndex]['name']
    state.selected_candidate.email = state.candidate_list.loc[currentIndex]['email']
    state.selected_candidate.phone = state.candidate_list.loc[currentIndex]['phone']
    state.selected_candidate.position = state.candidate_list.loc[currentIndex]['position']
    state.show_cand_dialog = True
    return 

def on_btn_upload_cand_clicked(state, action, payload):
    state.candidate_names.clear()
    state.candidate_emails.clear()
    state.candidate_phones.clear()
    state.candidate_positions.clear()
    
    if isinstance(state.candidate_photos, str):
        state.candidate_photos = [state.candidate_photos]
    elif isinstance(state.candidate_photos, list):
        state.candidate_photos = state.candidate_photos
    else:
        return
    
    for photo in state.candidate_photos:
        info = extract_info_from_image(photo)
        state.candidate_names.append(info['name'] if info['name'] is not None else " ")
        state.candidate_emails.append(info['email'] if info['email'] is not None else " ")
        state.candidate_phones.append(info['phone'] if info['phone'] is not None else " ")
        state.candidate_positions.append("  ")
        
    state.candidate_name = state.candidate_names[0]
    state.candidate_email = state.candidate_emails[0]
    state.candidate_phone = state.candidate_phones[0]


def load_candidate_list(state):
    state.candidate_list = pd.DataFrame(Candidate.getCandidates(), columns=["id", "name", "email", "phone", "position", "photo_name"])
    state.candidate_list["No"] = range(1, len(state.candidate_list) + 1)
    # state.candidate_list['Action'] = state.candidate_list['id'].apply(lambda x: f'<|button|label="view"|on_action=on_btn_cand_view_clicked|args={x}|>')
    state.candidate_data = state.candidate_list[["No", "name", "email", "phone", "position"]]
    

def do_add_candidate(state):
    state.candidate_names[0] = state.candidate_name
    state.candidate_emails[0] = state.candidate_email
    state.candidate_phones[0] = state.candidate_phone
    state.candidate_positions[0] = state.candidate_position
    
    success_count = 0
    
    for photo, name, email, phone, position in zip(state.candidate_photos, state.candidate_names, state.candidate_emails, state.candidate_phones, state.candidate_positions):
        
        photo_hash_name = upload_file(photo)
        _candidate = Candidate(name, email, phone, position, photo_hash_name)
        
        if _candidate.insert_new_candidate():
            success_count += 1

    notify(state, "S", message=f"Added {success_count} candidates") 
    load_candidate_list(state)
    state.show_add_cand_dialog = False

def do_edit_candidate(state, var_name, payload):
    currentIndex = payload["index"] # row index
    index = int(state.candidate_list.loc[currentIndex]['id'])
    col = payload["col"] # column name
    user_value = payload["user_value"] # new value as entered by the
    
    if Candidate.editById(index, col, user_value):
        old_value = state.candidate_data.loc[currentIndex, col]
        new_candidate_data = state.candidate_data.copy()
        new_candidate_data.loc[currentIndex, col] = user_value
        state.candidate_list.loc[currentIndex,col] = user_value
        state.candidate_data = new_candidate_data
        
        notify(state, "I", f"Edited value from '{old_value}' to '{user_value}'. (index '{index}', column '{col}')")
        
    else:
        notify(state,"E", "Email already exists in the database. Please enter a different email.")
        
def do_delete_candidate(state, var_name, payload):
    currentIndex= payload['index']
    index = int(state.candidate_list.loc[payload['index']]['id'])
    
    if Candidate.deleteById(index):
        state.candidate_data = state.candidate_data.drop(index=currentIndex)
        state.candidate_list = state.candidate_list.drop(index=currentIndex)
        
        notify(state, "S", f"Deleted row at index '{index}'")
    else:
        notify(state, "W", "You do not have permission to delete this row")
    
candidate_properties = {
    "class_name": "rows-bordered",
    "filter": True,
    "on_edit": do_edit_candidate,
    "on_delete": do_delete_candidate,
    "editable[No]": False,
    "columns": {
        "No": {"title": "No"},
        "name": {"title": "Name"},
        "email": {"title": "Email"},
        "phone": {"title": "Phone Number"},
        "position": {"title": "Position"},
        # "Action": {"title": "Action", "html":True}
    }
    #"editable[Action]": False,
    # "group_by[Action]" : True,
    # "apply[Action]": lambda x: f'<|button|label="Delete"|on_action=delete_row|args=[{x}]|>',
}