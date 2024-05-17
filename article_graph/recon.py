"""
This module includes utilities for reconciling data with Wikidata
entities and retrieving extra information.
"""

import pandas as pd
from reconciler import reconcile
from SPARQLWrapper import SPARQLWrapper, JSON

ORG_WIKIDATA_ID = "Q43229"


def get_extended_org_info(name: str):
    """
    Retrieve extended information from a organization given its name.
    """
    df = pd.DataFrame({"Org": [name]})
    result = reconcile(df["Org"], type_id=ORG_WIKIDATA_ID).loc
    reconciled_data = {}

    if result[0]['match'] is True or result[0]['score'] > 0.7:
        reconciled_data = {
            "match": result[0]['match'],
            "score": result[0]['score'],
            "wikidata_id": result[0]['id'],
        }
    else:
        reconciled_data = None

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    if reconciled_data is None:
        return None

    wikidata_id = reconciled_data['wikidata_id']

    sparql.setQuery(f"""
        SELECT ?icon ?location
        WHERE
        {{
            wd:{wikidata_id}   wdt:P154 ?icon ;
                                wdt:P159 ?location .
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
        }}
    """)

    bindings = sparql.query().convert()['results']['bindings']

    if len(bindings) > 0:
        for k, v in bindings[0].items():
            reconciled_data[k] = v['value']

    del reconciled_data['match']
    del reconciled_data['score']

    return reconciled_data


def recon_generic(names: list[str], reconcile_id):
    df = pd.DataFrame({"Names": names})

    results = reconcile(df["Names"], type_id=reconcile_id)

    return [{"name": result['name'], "match": result['match'], "score": result['score'], "id": result['id']} for index, result in results.iterrows()]
