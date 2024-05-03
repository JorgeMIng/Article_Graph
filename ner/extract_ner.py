
from pdf_analyzer.api.extract.elements import extract_element_soup




def case_final_ner(org_viejo,orgs,type_ent):
    org_viejo["type"]=type_ent
    if org_viejo["score"] >0.6 and (org_viejo["name"] not in [dict["name"] for dict in orgs]):
        orgs.append(org_viejo)
    org_temp=dict()
    org_temp["name"]=""
    org_temp["score"]=0
    return org_temp


def extract_ners(file,pipe):
    
    acno = extract_element_soup(file,None,"div","acknowledgement")
    ners=[]
    if len(acno)>0:
        for elements in acno:
            ners.extend(pipe(elements.text))



    org_parser=False
    misc_parser=False
    continue_parser=True

    org_temp=""
    org_temp=dict()
    org_temp["name"]=""
    org_temp["score"]=0
    org_temp["type"]=""
    orgs=[]
    pos_anterior=0
    for ner in ners:
        
        
        
        if org_parser and continue_parser and (ner["entity"]=='B-ORG') and ner["start"]!=pos_anterior:
            org_temp=case_final_ner(org_temp,orgs,"ORG")
            org_parser=False
            continue_parser=True
        if misc_parser and continue_parser and (ner["entity"]=='B-MISC') and ner["start"]!=pos_anterior:
            org_temp=case_final_ner(org_temp,orgs,"MISC")
            org_parser=False
            continue_parser=True 
            
        if org_parser and not continue_parser and (ner["entity"]!='I-ORG'):
            org_temp=case_final_ner(org_temp,orgs,"ORG")
            org_parser=False
            continue_parser=True   
        
            
        if misc_parser and not continue_parser and (ner["entity"]!='I-MISC'):
            org_temp=case_final_ner(org_temp,orgs,"MISC")
            misc_parser=False
            continue_parser=True
        
    
        
        if ner["entity"]=='B-ORG' and not org_parser:
            org_parser=True
            org_temp["name"]=ner["word"]
            org_temp["score"]=ner["score"]
            pos_anterior=ner["end"]
            continue
        
        if ner["entity"]=='B-ORG' and org_parser and continue_parser:
            
            org_temp["name"]=org_temp["name"]+ner["word"].replace("#", "")
            org_temp["score"]=org_temp["score"]*ner["score"]
            
            continue
        
        
        if ner["entity"]=='B-MISC' and not misc_parser:
            misc_parser=True
            
            org_temp["name"]=ner["word"]
            org_temp["score"]=ner["score"]
            pos_anterior=ner["end"]
            continue
        
        if ner["entity"]=='B-MISC' and misc_parser and continue_parser:
            
            org_temp["name"]=org_temp["name"]+ner["word"].replace("#", "")
            org_temp["score"]=org_temp["score"]*ner["score"]
            continue
        
        
        if ner["entity"]=='I-ORG' and org_parser:
            
            
            addit=""
            if pos_anterior+1 <= ner["start"]:
                addit=addit +" "
            continue_parser=False
            org_temp["name"]=org_temp["name"]+addit+ner["word"].replace("#", "")
            org_temp["score"]=org_temp["score"]*ner["score"]
            pos_anterior=ner["end"]
            continue
        

        if ner["entity"]=='I-MISC' and misc_parser:
            
            
            addit=""
            if pos_anterior+1 <= ner["start"]:
                addit=addit +" "
            continue_parser=False
            org_temp["name"]=org_temp["name"]+addit+ner["word"].replace("#", "")
            org_temp["score"]=org_temp["score"]*ner["score"]
            pos_anterior=ner["end"]
            continue
        
        
        if org_parser:
            
            org_temp=case_final_ner(org_temp,orgs,"ORG")
            misc_parser=False
            continue_parser=True
        
    
        if misc_parser:
            org_temp=case_final_ner(org_temp,orgs,"MISC")
            misc_parser=False
            continue_parser=True
            
        org_parser=False
        misc_parser=False
        continue_parser=True

    if org_parser:
        
        org_temp=case_final_ner(org_temp,orgs,"ORG")
        misc_parser=False
        continue_parser=True
        
    
    if misc_parser:
        org_temp=case_final_ner(org_temp,orgs,"MISC")
        misc_parser=False
        continue_parser=True   
    return orgs 



import re
def extract_award_identifiers(text):
    
    regex_patterns = {
        "NIH": r'(?:#)?\b[1-9][A-Z\d]{3}[A-Z]{2}\d{6}(?:-[AS]?\d+)?\b',
        "DOD": r'(?:#)?\b[A-Z\d]{6}-\d{2}-[123]-\d{4}\b',
        "NASA": r'(?:#)?\b(?:80|NN)[A-Z]+\d{2}[A-Z\d]+\b',
        "Education": r'(?:#)?\b[A-Z]+\d+[A-Z]\d{2}[A-Z\d]+\b'
    }

    
    all_identifiers = []

    
    for pattern in regex_patterns.values():
        identifiers = re.findall(pattern, text)
        all_identifiers.extend(identifiers)

   
    unique_identifiers = list(set(all_identifiers))

    return unique_identifiers

def get_projects_names(text):
   
    identifiers = extract_award_identifiers(text)
    
    
    names_and_codes = []

    
    for identifier in identifiers:
       
        match = re.search(rf'(\w+)\s+(?:grant|grants|award|awards|code|codes)\s+{re.escape(identifier)}', text, re.IGNORECASE)
        if match:
            names_and_codes.append(match.group(1))

    return names_and_codes

def extract_projects(file):
    
    acno = extract_element_soup(file,None,"div","acknowledgement")
    texts =""
    if len(acno)>0:
        for elements in acno:
            texts = texts + " "+ elements.text
       
    return extract_award_identifiers(texts),get_projects_names(texts)



def add_new_org(all_orgs,ner,seen_names):
    
    if ner["name"] in seen_names:
        pos =seen_names.index(ner["name"].lower())
        ner["org_id"]=all_orgs[pos]["org_id"]
        return all_orgs,ner,seen_names
    else:
        ner["org_id"]=len(all_orgs)
        new_ner=ner.copy()
        new_ner.pop("score", None)
        all_orgs.append(new_ner)
        seen_names.append(ner["name"].lower())

def get_all_ners(files,pipe):
    all_orgs_relation=[]
    all_orgs=[]
    seen_names = []
    for idx,file in enumerate(files):
        ners = extract_ners(file,pipe)
        if len(ners)>0:
            for ner in ners:
                add_new_org(all_orgs,ner,seen_names)
                ner["paper_id"]=idx
        all_orgs_relation.extend(ners)
    return all_orgs_relation,all_orgs


def add_new_project(all_projects,project,seen_names):
    
    if project["project_name"] in seen_names:
        pos =seen_names.index(project["project_name"].lower())
        project["project_id"]=all_projects[pos]["project_id"]
        return all_projects,project,seen_names
    else:
        project["project_id"]=len(all_projects)
        new_project=project.copy()
        all_projects.append(new_project)
        seen_names.append(project["project_name"].lower())


def get_all_projects(files):
    all_projects=[]
    seen_names = []
    all_projects_relation=[]
    for idx,file in enumerate(files):
        project_ids,project_name = extract_projects(file)
        projects_file=[]
        if len(project_ids)>0:
            for project_id in project_ids:
                project={"project_name":project_name[0],"project_federal_id":project_id}
                add_new_project(all_projects,project,seen_names)
                project["paper_id"]=idx
                projects_file.append(project)
            all_projects_relation.extend(projects_file)
    return all_projects,all_projects_relation


