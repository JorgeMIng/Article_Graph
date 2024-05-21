import os
from pathlib import Path
import sys
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.add_vertical_space import add_vertical_space
import json
import webbrowser
from omegaconf import OmegaConf
from query_fuseki import FusekiConection,get_uri,get_url_short,url_ok

from session_persistance import load_session_state,save_session_state


protocols=["None","http","https"]


def cargar_pagina():
    """
    Configura el disenio de la pagina de Streamlit.
    """
    st.set_page_config(
        layout="wide", page_title="Article Graph Tool", page_icon="app/images/logo_top.png"
    )
    
def get_default_value(key):
    config = OmegaConf.load('app/config/server.yaml')
    return config[key]

def cargar_estado_session():
    """
    Inicializa el estado de sesion de Streamlit.
    """
    
        
    load_session_state()
 
        
    if 'protocol_value' not in st.session_state:
        st.session_state["protocol_value"]=get_default_value("protocol")
    if 'domain_value' not in st.session_state:
        st.session_state["domain_value"]=get_default_value("domain")
    if 'port_value' not in st.session_state:
        st.session_state["port_value"]=get_default_value("port")
    if 'dataset_name_value' not in st.session_state:
        st.session_state["dataset_name_value"]=get_default_value("dataset_name")
    if 'fuseki_wrapper' not in st.session_state:
        try:
            st.session_state["fuseki_wrapper"] = FusekiConection(st.session_state)
        except Exception:
            st.error("Server is not offline")
            st.session_state["fuseki_wrapper"] = None
def cargar_css():
    """
    Carga y aplica el archivo de estilo CSS personalizado.
    """
    css_file_path = "app/config/estiloMain.css"
    css_file_content = open(css_file_path, "r").read()
    st.markdown(css_file_content, unsafe_allow_html=True)

def cargar_logo_y_titulo():
    """
    Muestra el logo y el titulo del proyecto.
    """
    c1, c2 = st.columns([0.1, 0.9])

    with c1:
        st.image('app/images/logo.png', width=110)

    with c2:
        st.caption("")
        new_title = '<p style="color:#00629b;text-align: center; font-size: 70px;">Article Graph Tool</p>'
        st.markdown(new_title, unsafe_allow_html=True)

    if "protocol" not in st.session_state:
        st.session_state.protocol=st.session_state["protocol_value"]
        
    if "domain" not in st.session_state:
        st.session_state.domain=st.session_state["domain_value"]
        
    if "port" not in st.session_state:
        st.session_state.port=st.session_state["port_value"]
    if "dataset_name" not in st.session_state:
        st.session_state.dataset_name=st.session_state["dataset_name_value"]
    
            
        
    index_select = protocols.index(st.session_state.protocol_value)
    
    protocol = st.selectbox("Select protocol to use",protocols,key="protocol",index=index_select, help="Select which protocol the api will use for conecting the triple store. For example if your tripler store uses the dir \"https://hello.com:3030\\dataset\\query\" you select https.", placeholder="Choose an option")

    domain = st.text_input("Select protocol to use",key="domain",help="Select which domain the api will use for conecting the triple store. For example if your triple store uses the dir \"https://hello.com:3030\\dataset\\query\" you write hello.com")
    
    port = st.number_input("Select port to use  (0 == None port)",key="port",min_value= 0, max_value = 65535,help= "Select which port the api will use for conecting the triple store. For example if your triple store uses the dir \"https://hello.com:3030\\dataset\\query\" you chose 3030, use port 0 for None port")

    dataset_name = st.text_input("Select dataset to use",key="dataset_name",help="Select which dataset (yena-fuseki) the api will use for conecting the triple store. For example if your triple store uses the dir \"https://hello.com:3030\\dataset\\query\" you write \"dataset\"")
    
    change = st.button("Change Settings")
    
    if change:
    
        st.session_state.port_value=port
        st.session_state.domain_value=domain
        st.session_state.protocol_value=protocol
        st.session_state.dataset_name_value=dataset_name
   
        new_uri=get_uri(st.session_state)
        try:
            cmp = url_ok(get_url_short(st.session_state))
        except Exception:
            cmp=False
            
        if not cmp:
            st.error("Server is offline change uri")
            st.session_state.fuseki_wrapper=None
            st.cache_data.clear()
            
        elif st.session_state!=None and cmp:
            try:
                st.session_state.fuseki_wrapper = FusekiConection(st.session_state)
            except Exception:
                st.session_state.fuseki_wrapper=None
            st.cache_data.clear()
        elif st.session_state.fuseki_wrapper.uri !=new_uri:
            st.session_state.fuseki_wrapper.change_endpoint_str(new_uri)
            st.cache_data.clear()
        new_title = '<p style="color:#00629b;text-align: center; font-size: 40px;">Settings changed</p>'
        st.markdown(new_title, unsafe_allow_html=True)
    new_uri=get_uri(st.session_state)    
    if st.session_state.fuseki_wrapper!=None:
        new_title = '<p style="color:#00629b;text-align: center; font-size: 20px;">Endpoint URL is '+st.session_state.fuseki_wrapper.uri+'</p>'
    else:
        new_title = '<p style="color:#00629b;text-align: center; font-size: 20px;">Error URL '+get_uri(st.session_state)+' is offline</p>'

    st.markdown(new_title, unsafe_allow_html=True)
    
    # Botón de GitHub con un estilo más bonito
    if st.button("🚀 Visitar el Repositorio en GitHub", key="github_button"):
        st.write("Redirigiendo a GitHub...")
        webbrowser.open("https://github.com/JorgeMIng/Article Graph")
        # Para que se quite el texto de Redirigiendo... 




def cargar_pie_pagina():
    """
    Carga el pie de página.
    """
    st.markdown(
        """
        <style>
            .footer {
                padding: 10px;
                background-color: #f4f4f4;
                color: #333;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="footer">© 2024 Article Graph Tool. Apache 2.0 License.</div>', unsafe_allow_html=True)


def main():
    """
    Funcion principal que ejecuta la aplicacion.
    """
    cargar_pagina()
    cargar_estado_session()
    cargar_css()
    cargar_logo_y_titulo()
    cargar_pie_pagina()
    save_session_state()
    

if __name__ == "__main__":
    main()