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
        st.session_state["fuseki_wrapper"] = FusekiConection(st.session_state)

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

    with st.spinner('Executing SPARQL query'):
        result=query_filtrada()
    if result!=None:
        #st.write(result)
        with st.spinner('Drawing_graph'):
            draw_graph(result)
    else:
        st.error("There is no data")
    
    
    

    # Botón de GitHub con un estilo más bonito
    if st.button("🚀 Visitar el Repositorio en GitHub", key="github_button"):
        st.write("Redirigiendo a GitHub...")
        webbrowser.open("https://github.com/JorgeMIng/Article_Graph")
     

def query_filtrada(paper=None,org=None,author=None):
    query=f"""
    SELECT * WHERE {{
    ?sub ?pred ?obj .
  
    }}
"""
    fuseki=st.session_state["fuseki_wrapper"]
    
    result =fuseki.execute_query(query)
            
            
    return result
    
import streamlit
from streamlit_agraph import agraph, Node, Edge, Config


def id_sub(value):
    partes = value.split('/')
    return partes[-1]

def id_obj(value):
    partes = value.split('/')
    return partes[-1]

def get_node_sub(sub,nodes_seen,nodes):
    idx=id_sub(sub["value"])
    if idx not in nodes_seen:
        nodes.append(Node(id=idx, label=idx, size=25, shape="circular"))
        nodes_seen.append(idx)

def get_node_obj(obj,nodes_seen,nodes):
    idx=id_obj(obj["value"])
    if idx not in nodes_seen:
        nodes.append(Node(id=idx, label=idx, size=25, shape="circular"))
        nodes_seen.append(idx)

def get_edge_pred(sub,obj,pred):
    id_sub_v=id_sub(sub["value"])
    id_obj_v=id_obj(obj["value"])
    id_pred=id_obj(pred["value"])
    
    return Edge(source=id_sub_v, 
                    label=id_pred, 
                    target=id_obj_v, 
                    # **kwargs
                    ) 
    
@st.cache_data(show_spinner=False)    
def get_nodes_cache(result_query):
    nodes = []
    nodes_seen=[]
    edges = []
    
    
    for triple in result_query:
       get_node_sub(triple["sub"],nodes_seen,nodes)
       get_node_obj(triple["obj"],nodes_seen,nodes)
       edges.append(get_edge_pred(triple["sub"],triple["obj"],triple["pred"]))
    return nodes,edges
    

def draw_graph(result_query):


    nodes,edges=get_nodes_cache(result_query)


    config = Config(width=750,
                    height=950,
                    directed=True, 
                    physics=True, 
                    hierarchical=False,
                    # **kwargs
                    )

    return agraph(nodes=nodes, 
                        edges=edges, 
                        config=config)
    
    
    


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