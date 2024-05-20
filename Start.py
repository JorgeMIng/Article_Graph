import os
import sys
from streamlit.web import cli as stcli


if __name__ == '__main__':

    sys.path.append(os.path.dirname(__file__))
    sys.argv = ["streamlit", "run", "app/App.py"]
    
    #remove session saved
    file_path = os.path.join(os.path.dirname(__file__),"app","sessions","session_state.pkl")
    # Check if the file exists before attempting to delete it 
    if os.path.exists(file_path):
        os.remove(file_path)
    
    sys.exit(stcli.main())

    
    
    
    




