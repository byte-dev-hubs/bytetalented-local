from taipy.gui import notify, navigate
from datetime import datetime, timedelta

def check_login(state):
    if state.signed_in:
        current_time = datetime.now()
        elapsed_time = current_time - state.signin_date
        
        if elapsed_time > timedelta(hours=1):
            state.signed_in=False
            navigate(state,'dashboard')
            return False
        
        else:
            return True
        
    else:
        navigate(state,'dashboard')
        return None
    