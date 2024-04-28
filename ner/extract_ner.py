
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
def extract_projects(file):
    
    acno = extract_element_soup(file,None,"div","acknowledgement")
    texts =""
    if len(acno)>0:
        for elements in acno:
            texts = texts + " "+ elements.text
       
    return re.findall(r'\b#?[A-Z\d-]+(?:-\d+){3,}\b', texts),re.findall(r'(\b[A-Z\d&-]+\b)\s*(?:award[s]?|grant)\s*#?[A-Z\d-]+(?:-\d+){3,}\b',texts)

def extract_projects_complex(file):
    acno = extract_element_soup(file,None,"div","acknowledgement")
    texts =""
    if len(acno)>0:
        for elements in acno:
            texts = texts + " "+ elements.text

# Definimos un patrón para buscar nombres y sus respectivos identificadores con #
    patron_awards = r'([A-Z\d&-]+)\s*awards\s*((?:#?[A-Z\d-]+(?:-\d+){3,}(?:\s*and\s*#?[A-Z\d-]+(?:-\d+){3,})*)+)\b'

    # Definimos un patrón para buscar nombres y sus respectivos identificadores con grant
    patron_grant = r'([A-Z\d&-]+)\s*grant\s*((?:#?[A-Z\d-]+(?:-\d+){3,}))\b'

    # Encontramos todas las coincidencias con awards
    resultados_awards = re.findall(patron_awards, texts)

    # Encontramos todas las coincidencias con grant
    resultados_grant = re.findall(patron_grant, texts)

    # Creamos una lista de tuplas para almacenar los resultados
    resultado_final = []

    # Función para agregar resultados a la lista final
    def agregar_resultados(resultados):
        for match in resultados:
            nombre = match[0]
            identificadores = match[1].split(' and ')
            for identificador in identificadores:
                resultado_final.append((identificador, nombre))

    # Agregamos los resultados de awards
    agregar_resultados(resultados_awards)

    # Agregamos los resultados de grant
    for match in resultados_grant:
        nombre = match[0]
        identificador = match[1]
        resultado_final.append((identificador, nombre))

    return resultado_final

def get_all_ners(files,pipe):
    all_orgs=[]
    for idx,file in enumerate(files):
        ners = extract_ners(file,pipe)
        if len(ners)>0:
            for ner in ners:
                ner["paper_id"]=idx
        all_orgs.extend(ners)
    return all_orgs


def get_all_project_ids(files):
    all_projects=[]
    for idx,file in enumerate(files):
        project_ids,project_name = extract_projects(file)
        projects=[]
        if len(project_ids)>0:
            for project_id in project_ids:
                projects.append({"project_id":project_id,"paper_id":idx})
            all_projects.extend(projects)
    return all_projects


def get_all_project_experimental(files):
    all_projects_complex=[]
    for idx,file in enumerate(files):
        projects=[]
        
        projects_data = extract_projects_complex(file)
        if len(projects_data)>0:
            
            for project_data in projects_data :
                try:
                    projects.append({"project_id":project_data[0],"name":project_data[1],"paper_id":idx})
                except Exception:
                    pass
            all_projects_complex.extend(projects)
    return all_projects_complex