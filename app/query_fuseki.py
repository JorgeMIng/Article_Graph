
#uses streamlit session state


from SPARQLWrapper import SPARQLWrapper, JSON
import requests
def get_uri(session_state):
    uri=""
    
    if session_state.protocol_value!="None":
        uri= session_state.protocol_value+'://'
    if session_state.port_value==0:
        uri= uri+session_state.domain_value
    else:
        uri = uri+session_state.domain_value+':'+str(session_state.port_value)
    if session_state.dataset_name_value!="":
        uri= uri+"/"+session_state.dataset_name_value
    return uri

def get_url_short(session_state):
    uri=""
    if session_state.protocol_value!="None":
        uri= session_state.protocol_value+'://'
    if session_state.port_value==0:
        uri= uri+session_state.domain_value
    else:
        uri = uri+session_state.domain_value+':'+str(session_state.port_value)
    return uri

def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200

class FusekiConection():
    
    def __init__(self,session_state):
        self.uri=get_uri(session_state)
        self.sparql = SPARQLWrapper(self.uri)
        self.sparql.setReturnFormat(JSON)
        if not url_ok(get_url_short(session_state)):
            raise ValueError("Server is offline change settings")
        
        
    def execute_query(self,query):
        self.sparql.setQuery(query)
        query_res=self.sparql.query().convert()['results']['bindings']
        if len(query_res)>0:
            return query_res
        return None
    
    
    def change_endpoint(self,session_state):
        self.uri=get_uri(session_state)
        self.sparql.endpoint=self.uri
    
    def change_endpoint_str(self,uri):
        self.sparql.endpoint=uri
        self.uri=uri