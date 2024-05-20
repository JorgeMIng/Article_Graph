import re
from pdf_analyzer.api.extract.elements import extract_element_soup
from ner.extract_ner import add_new_org


def combine_all_text(texts_soup):
    result_text = ""
    for text_soup in texts_soup:
        result_text = text_soup.text + " " + result_text
    return result_text


def get_name_data(pers_name):
    if not pers_name:
        return None, None, None
    first_name = combine_all_text(pers_name.find_all('forename', type="first"))
    middle_name = combine_all_text(
        pers_name.find_all('forename', type="middle"))
    last_name = combine_all_text(pers_name.find_all('surname'))

    first_name = first_name+" "+middle_name
    full_name = first_name+" "+last_name
    # be sure None objects are None for checking later when graph building
    if first_name == "":
        first_name = None
    if last_name == "":
        last_name = None
    if full_name == "":
        full_name = None

    return first_name, last_name, full_name


def add_new_author(allAuthors, author, seen_names):
    if author["label"].lower() in seen_names:
        pos = seen_names.index(author["label"].lower())
        author["author_id"] = allAuthors[pos]["author_id"]
        author["label"] = allAuthors[pos]["label"]
        return allAuthors, author, seen_names
    else:
        author["author_id"] = len(allAuthors)
        allAuthors.append(author)
        seen_names.append(author["label"].lower())


def getAffiliations(author, allOrgs, seen_names, author_id):
    orgs_relations = []
    seen_names_rel = []
    if author.affiliation is None:
        return []

    for org in author.find_all("orgName"):
        if org.text.lower() in seen_names_rel:
            continue
        seen_names_rel.append(org.text.lower())
        org_dict = {"name": org.text}
        add_new_org(allOrgs, org_dict, seen_names)
        org_rel = org_dict.copy()
        org_rel["author_id"] = author_id
        orgs_relations.append(org_rel)
    return orgs_relations


def get_author_metadata(file, authors_list=[], allOrgs=[]):
    authors = extract_element_soup(file, "teiHeader", "author", None)
    seen_names_author = [d["label"].lower() for d in authors_list]
    seen_names_orgs = [d["name"].lower() for d in allOrgs]
    all_relations = []
    for author in authors:
        first_name, last_name, full_name = get_name_data(author.persName)
        if full_name is None:
            continue
        email = None if not author.email else re.sub(
            r'</?email>', '', str(author.email))
        author_dict = {"name": first_name, "last_name": last_name,
                       "label": full_name, "email": email}
        add_new_author(authors_list, author_dict, seen_names_author)
        orgs_relations = getAffiliations(
            author, allOrgs, seen_names_orgs, author_dict["author_id"])
        all_relations.extend(orgs_relations)
    return authors_list, all_relations, allOrgs


def get_all_author_metadata(files, allOrgs=[]):
    authors_list = []
    relation_author_paper = []
    relation_author_org = []
    for idx, paper in enumerate(files):
        authors_list, relations_org, allOrgs = get_author_metadata(
            paper, authors_list, allOrgs)
        relation_author_org.extend(relations_org)
        for author in authors_list:
            rel_author = {"author_id": author["author_id"], "paper_id": idx}
            relation_author_paper.append(rel_author)
    return authors_list, relation_author_paper, allOrgs, relation_author_org
