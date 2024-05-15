from SPARQLWrapper import SPARQLWrapper, JSON
from recon import recon_generic
PERSON_WIKIDATA_ID = "Q5"

def get_extended_author_info(names: list[str]):
    # 1 Llamar a reconciler
    reconciled_data = recon_generic(names,PERSON_WIKIDATA_ID)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    for idx,values in enumerate(reconciled_data):
        id = values['id']
        
        # wdt:P31 (instance_of)
        sparql.setQuery(f"""
            SELECT ?gender
            WHERE
            {{
                wd:{id} wdt:P21 ?gender .
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
            }}
        """)
        result = sparql.query().convert()['results']['bindings'][0]['gender']['value']
        reconciled_data[idx]['gender'] = result
    
    # 3 Devolver los datos
    return reconciled_data