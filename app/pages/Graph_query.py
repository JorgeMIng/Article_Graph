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

types_search_list=["Specific ID","All Instances","Full Graph"]
nodes_types=["Organization","Paper","Person"]
nodes_types_query=["Organization","paper","person"]

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
    if "type_search_v" not in st.session_state:
        st.session_state["type_search_v"]=types_search_list[0]
    if "node_type_v" not in st.session_state:
        st.session_state["node_type_v"]=nodes_types[0]
    if "id_node_v" not in st.session_state:
        st.session_state["id_node_v"]=0
        
    if "limit_v" not in st.session_state:
        st.session_state["limit_v"]=2000
    
    
    
    
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



def side_bar():
    
    
    if "id_node" not in st.session_state:
        st.session_state["id_node"]=st.session_state["id_node_v"]
        
    if "type_search" not in st.session_state :
        st.session_state["type_search"]=st.session_state["type_search_v"]
    
    if "node_type" not in st.session_state:
        st.session_state["node_type"]=st.session_state["node_type_v"]
        
    if "limit_slider" not in st.session_state:
        st.session_state["limit_slider"]=st.session_state["limit_v"]
        
    node_index = nodes_types.index(st.session_state.node_type_v)
    search_index = types_search_list.index(st.session_state.type_search)
        
    
    type_search= st.selectbox("Type of search",types_search_list,index=search_index,key="type_search",help="Select if the search will use a specific id of a type of node,all the nodes of that type or the full graph")
    if type_search !="Full Graph":
        st.selectbox("Type of Node",nodes_types,key="node_type" ,index=node_index,help="Select which node type will be use to search")
        if type_search=="Specific ID":
            st.number_input("Node id",key="id_node",min_value=0,help="Node id use for the intial node of the search")
            
    st.number_input("Limit nodes",key="limit_slider",min_value=0,step=100,value=st.session_state.limit_v,help="Limit on the amount of triples to extract from the graph")
    
    
    button_query = st.button("Execute Query",key="button_query")
    
    
    
    st.session_state["limit_v"]=st.session_state["limit_slider"]
    st.session_state["type_search_v"]=st.session_state["type_search"]
    st.session_state["node_type_v"]=st.session_state["node_type"]
    st.session_state["id_node_v"]=st.session_state["id_node"]
    
    




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
    if st.session_state["button_query"]:
        with st.spinner('Executing SPARQL query'):
            result=execute_queries_graph(st.session_state.type_search_v,st.session_state.node_type_v,st.session_state.id_node_v,st.session_state.limit_v)
        if result!=None:
            with st.spinner('Drawing_graph'):
                draw_graph(result)
        else:
            st.error("There is no data")
    else:
        st.warning("Press button to launch query")
    
    
    

    # Botón de GitHub con un estilo más bonito
    if st.button("🚀 Visitar el Repositorio en GitHub", key="github_button"):
        st.write("Redirigiendo a GitHub...")
        webbrowser.open("https://github.com/JorgeMIng/Article_Graph")


def execute_queries_graph(type_search,node_type,id_node,limit):
    result=None
    if type_search =="Full Graph":
       result = full_graph_query(limit)
    if result!=None and type_search=="Specific ID":
        result= query_node_specific(id_node,nodes_types_query[nodes_types.index(node_type)],limit)
    if result!=None and type_search=="All Instances":
        result = query_node_type(node_type,limit)

    if result==None:
        st.cache_data.clear()   
        
    return result
@st.cache_data
def full_graph_query(limit):
   
    
    query=f"""
    SELECT ?sub ?pred ?obj
    WHERE {{
        ?sub ?pred ?obj
    }}
    LIMIT {limit}
    """

    fuseki=st.session_state["fuseki_wrapper"]
    if fuseki==None:
        st.error("Server in settings is offline")
        return None

    result =fuseki.execute_query(query)
            
            
    return result

@st.cache_data
def query_node_type(limit,node_type):
       
    
    query=f"""
    SELECT ?sub ?pred ?obj
    WHERE {{
    {{
        <http://open_science.com/{node_type}> a ?obj1 .
        BIND(<http://open_science.com/{node_type}> AS ?sub1)
        
    }}
    }}
    UNION
    {{
        ?sub1 a <http://open_science.com/{node_type}#1> .
        BIND(<http://open_science.com/{node_type}> AS ?obj1)
    }}
    # Get all relationships starting from the previously found subjects
    {{
        ?sub1 ?pred ?obj .
        BIND(?sub1 AS ?sub)
        FILTER (?pred != rdf:type)
    }}
    UNION
    # Get all relationships starting from the previously found objects
    {{
        ?obj1 ?pred ?obj .
        BIND(?obj1 AS ?sub)
        FILTER (?pred != rdf:type)
    }}
    LIMIT {limit}
    """

    fuseki=st.session_state["fuseki_wrapper"]
    if fuseki==None:
        st.error("Server in settings is offline")
        return None

    result =fuseki.execute_query(query)
            
            
    return result
     
@st.cache_data
def query_node_specific(node_id,node_type,limit):
    
    if node_type=="paper":
        addition="""UNION
        # Get all keyword relationships
    {{
        ?sub ?pred ?obj .
        FILTER (?pred = <http://open_science.com/keyword>)
    }}"""
    
    
    query=f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?sub ?pred ?obj
WHERE {{
    {{
        <http://open_science.com/{node_type}#{node_id}> ?pred1 ?obj1 .
        BIND(<http://open_science.com/{node_type}#{panode_id}> AS ?sub1)
        
    }}
    UNION
    {{
        ?sub1 ?pred2 <http://open_science.com/{node_type}#1> .
        BIND(<http://open_science.com/{node_type}#{node_id}> AS ?obj1)
    }}

    # Get all relationships starting from the previously found subjects
    {{
        ?sub1 ?pred ?obj .
        BIND(?sub1 AS ?sub)
        FILTER (?pred != rdf:type)
    }}
    UNION
    # Get all relationships starting from the previously found objects
    {{
        ?obj1 ?pred ?obj .
        BIND(?obj1 AS ?sub)
        FILTER (?pred != rdf:type)
    }}
    # Addition
    {addition}
    
}}
LIMIT {limit}


    """

    fuseki=st.session_state["fuseki_wrapper"]
    if fuseki==None:
        st.error("Server in settings is offline")
        return None
    
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
    with st.sidebar:
        side_bar()
    
    
    cargar_logo_y_titulo()
    cargar_pie_pagina()
    save_session_state()
    

if __name__ == "__main__":
    main()