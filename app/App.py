import os
from pathlib import Path
import sys
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.add_vertical_space import add_vertical_space
import json
import webbrowser

from session_persistance import load_session_state,save_session_state

from omegaconf import OmegaConf
from query_fuseki import FusekiConection

def cargar_path_modelo():
    """
    Configura la ruta para recoger informacion del modelo.
    """
    #sys.path.append(os.path.dirname(__file__))
    pass

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

    c3, c4 = st.columns([0.4, 0.7])

    with c3:
        st.markdown("""
            ## Guide
            
            Example guide

        """)

    with c4:
        cargar_animacion_lottie()

    # Sección "Novedades y Actualizaciones"
    st.markdown("""
        ## Novedades y Actualizaciones
    """)
    
    with st.expander("Última Versión"):
        st.write("""
        **Versión 1.0.0**
        
        - Sparql endpoint managment (set endpoint to do sql queries)
        - Visualization of graph store in the endpoint
        - Map visualization of organizations
        """)
    

    # Botón de GitHub con un estilo más bonito
    if st.button("🚀 Visitar el Repositorio en GitHub", key="github_button"):
        st.write("Redirigiendo a GitHub...")
        webbrowser.open("https://github.com/JorgeMIng/Article_Graph")
     


def cargar_animacion_lottie():
    """
    Carga y muestra la animacion Lottie.
    """
    path = "app/images/animated/graph_2.json"
    with open(path, "r") as file:
        url_loan = json.load(file)


    add_vertical_space(6)
    st_lottie(url_loan,
                reverse=False,
                height=500,
                width=500,
                speed=1,
                loop=True,
                quality='high',
                key='test'
                )

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
    cargar_path_modelo()
    cargar_pagina()
    cargar_estado_session()
    cargar_css()
    cargar_logo_y_titulo()
    cargar_pie_pagina()
    save_session_state()
    

if __name__ == "__main__":
    main()