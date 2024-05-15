

from pdf_analyzer.api.extract.elements import extract_element_soup

def get_paper_metadata(file):
    title = extract_element_soup(file,"teiHeader.fileDesc.titleStmt.title",None,None).text
    date=extract_element_soup(file,"teiHeader.fileDesc.publicationStmt.date",None,None)
    
    
    if len(date)==0:
        date=extract_element_soup(file,"teiHeader.fileDesc.sourceDesc.biblStruct.monogr.imprint.date",None,None)
    if len(date)==0:
        date=None

    abstract = extract_element_soup(file,None,"abstract")
    abstract_text=""
    for element_text in abstract:
                abstract_text = abstract_text + " " + element_text.text
                
    paper_element={"title":title,"abstract":abstract_text,"release_date":date}
    return paper_element

def get_all_paper_metadata(files):
    all_papers=[]
    for idx,paper in enumerate(files):
        metadata_paper = get_paper_metadata(paper)
        metadata_paper["paper_id"]=idx
        all_papers.append(metadata_paper)
    return all_papers