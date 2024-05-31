from taipy.gui import Gui
from backend.home import *
gui = Gui(pages=pages)
gui.run(
    host="0.0.0.0", 
    use_reloader=True, 
    debug=True,
    title="ByteTalented-CRM",)