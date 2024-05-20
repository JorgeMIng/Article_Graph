
#uses streamlit session state


from SPARQLWrapper import SPARQLWrapper, JSON

def get_uri(session_state):
    return session_state.protocol_value+'://'+session_state.domain_value+':'+str(session_state.port_value)+"/"+session_state.dataset_name_value+"/query"


class FusekiConection():
    
    def __init__(self,session_state):
        self.uri=get_uri(session_state)
        self.sparql = SPARQLWrapper(self.uri)
        self.sparql.setReturnFormat(JSON)
        
        
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