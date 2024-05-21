"""
This module includes utilities for reconciling data with Wikidata
entities and retrieving extra information.
"""
import pandas as pd
from reconciler import reconcile
from SPARQLWrapper import SPARQLWrapper, JSON
from ._utils import parse_coordinates

__ORG_WIKIDATA_ID = 'Q43229'
__PERSON_WIKIDATA_ID = 'Q5'


def get_organizations_info(names: list[str]) -> dict[str, dict[str, float] | str] | None:
    """
    Retrieve extended information from a organization given its name.
    """
    reconciled_data = reconcile_organizations(names)

    if reconciled_data is None:
        return None

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    for org_info in reconciled_data.values():
        wikidata_id = org_info['wikidata_id']
        sparql.setQuery(f"""SELECT DISTINCT ?coordinates WHERE {{
                optional{{wd:{wikidata_id} wdt:P625 ?coordinates}}.
                optional{{wd:{wikidata_id} wdt:P159 ?sede.
                        ?sede wdt:P625 ?coordinates}}.
 
}}""")

        bindings = sparql.query().convert()['results']['bindings']

        if len(bindings) > 0:
            for k, v in bindings[0].items():
                if k == 'coordinates':
                    v['value'] = parse_coordinates(v['value'])
                org_info[k] = v['value']

    return reconciled_data


def reconcile_persons(names: list[str]):
    """
    Reconcile a list of persons by name.
    """
    return __reconcile_multiple_entities(names, __PERSON_WIKIDATA_ID)


def reconcile_organizations(names: list[str]):
    """
    Reconcile a list of organizations by name.
    """
    return __reconcile_multiple_entities(names, __ORG_WIKIDATA_ID)


def __reconcile_multiple_entities(names: list[str], type_id: str) -> dict[str, str] | None:
    """
    Reconcile with a list of names and type_id.
    """
    df = pd.DataFrame({'Names': names})
    results = reconcile(df['Names'], type_id=type_id).to_dict('records')

    if len(results) <= 0:
        return None

    reconciled_data = {}
    for r in results:
        if r is None:
            continue
        if r['match'] or ('score' in r and r['score'] > 85):
            reconciled_data[r['input_value']] = {'wikidata_id': r['id']}
    return reconciled_data
