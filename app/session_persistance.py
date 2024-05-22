import os
import pickle

import streamlit as st

keys_important=["protocol_value","port_value","dataset_name_value","domain_value"]

def filter_dict(dict_input,keys_filter):
    return dict((k, dict_input[k]) for k in keys_filter
           if k in dict_input)


def save_session_state():
    try:
        file_path = os.path.join(os.path.dirname(__file__),"app","sessions","session_state.pkl")
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'wb') as f:
            dict_s=filter_dict(st.session_state.to_dict(),keys_important)
            
            print("saving session_state",dict_s)
            print(type(st.session_state))
            pickle.dump(dict_s, f)
    except Exception as e:
        print("Error during saving session state:", e)


def load_session_state():
    file_path = os.path.join(os.path.dirname(__file__),"app","sessions","session_state.pkl")
    print(file_path)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                loaded_state = pickle.load(f)
                print("Loaded session state:", loaded_state)
                
                if loaded_state!=None:
                    for key in loaded_state.keys():
                        st.session_state[key]=loaded_state[key]
                return loaded_state
        except Exception as e:
            print("Error during loading session state:", e)
    else:
        print("session_state.pkl not found")
    return None