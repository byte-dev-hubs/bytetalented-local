from taipy. gui import notify
from model.bid import Bid
import pandas as pd
import datetime

applyurl = ""
companyname = ""
position = ""
show_add_bid_dialog = False
selected_bid_date = datetime.date.today()
bid_list = None

bid_data = pd.DataFrame({
    "No":[],
    "apply_url": [],
    "company_name": [],
    "position": [],
})

def on_add_bid_finish(state, id, payload):
    id = payload["args"][0]
    
    if id == 0:
        do_add_bid(state)
    else:
        state.show_add_bid_dialog = False

def on_btn_add_bid_clicked(state):
    state.applyurl = ""
    state.companyname = ""
    state.position = ""
    state.show_add_bid_dialog = True
    
def load_bid_list(state):
    state.bid_list = pd.DataFrame(Bid.getBids(state.selected_bid_date), columns=["id","user_id",  "apply_url", "company_name", "position", "created_at"])
    state.bid_list['No'] = range(1, len(state.bid_list) + 1)
    state.bid_data = state.bid_list[['No', 'apply_url', 'company_name', 'position']]

def do_add_bid(state):
    if state.applyurl == "":
        notify(state, message='Please enter the apply url')
        return
    
    if state.companyname == "":
        notify(state, message='Please enter the company name')
        return
    
    if state.position == "":
        notify(state,"", message='Please enter the position')
        return
    
    bid = Bid(state.user_id, state.applyurl, state.companyname, state.position)
    
    if bid.insert_new_bid():
        notify(state, "S", message='Bid added successfully!')
        state.show_add_bid_dialog = False
        load_bid_list(state)
    else:
        notify(state, "W", message='Bid already exists!')

def do_edit_bid(state, action, payload):
    currentIndex = payload["index"] # row index
    index = int(state.bid_list.loc[currentIndex]['id'])
    col = payload["col"] 
    user_value = payload["user_value"] 
    
    if Bid.editById(index, col, user_value, state.user_id) == False:
        notify(state, message='Site URL already exists')
        return
    
    else:
        old_value = state.bid_data.loc[currentIndex, col]
        new_bids = state.bid_data.copy()
        new_bids.loc[currentIndex, col] = user_value
        state.bid_list.loc[currentIndex, col] = user_value
        state.bid_data = new_bids
        notify(state, "W", f"Edited value from '{old_value}' to '{user_value}'. (index '{index}', column '{col}')")
        return

def do_delete_bid(state, action, payload):
    currentIndex= payload['index']
    index = int(state.bid_list.loc[payload['index']]['id'])
    if Bid.deleteById(index, state.user_id):
        state.bid_data = state.bid_data.drop(index = currentIndex)
        state.bid_list = state.bid_list.drop(index = currentIndex)
        notify(state, "S", f"Deleted row at index '{index}'")
    else:
        notify(state, "W", "You do not have permission to delete   row")

def bid_date_changed(state):
    load_bid_list(state)

bid_table_properties = {
    "class_name": "rows-bordered",
    "filter": True,
    "on_edit": do_edit_bid,
    "on_delete": do_delete_bid,
    "editable[No]": False,
    "columns": {
        "No": {"title": "No"},
        "apply_url": {"title": "Apply URL"},
        "company_name": {"title": "Company Name"},
        "position": {"title": "Position"}
    }
}   