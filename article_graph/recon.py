import pandas as pd
from reconciler import reconcile
from SPARQLWrapper import SPARQLWrapper, JSON

PERSON_WIKIDATA_ID = "Q5"

def get_extended_author_info(names: list[str]):
    # 1 Llamar a reconciler
    df = pd.DataFrame({ "Authors": names })

    result = reconcile(df["Authors"], type_id=PERSON_WIKIDATA_ID).loc

    reconciled_data = {}

    for i in range(len(names)):
        reconciled_data[names[i]] = {
            "match": result[i]['match'],
            "score": result[i]['score'],
            "id": result[i]['id'],
        }

    # Evaluate if the reconciliation is ok
    # match == True || score > 0.7

    # 2 Query a Wikidata con los valores que necesitamos

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    for name, values in reconciled_data.items():
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
        reconciled_data[name]['gender'] = result
    
    # 3 Devolver los datos
    return reconciled_data

print(get_extended_author_info(["Jacob Devlin", "Barack Obama", "Marie Curie"]))

