"""
Utility functions for the article graph.
"""

from datetime import datetime
from pdf_analyzer.api.extract.elements import extract_element_soup


def xml_date_to_xsd_date(date: str) -> str | None:
    """
    Convert an XML date to an XSD date.
    """
    # Try 2 formats
    formats = ['%d %b %Y', '%Y-%m-%d']
    for fmt in formats:
        try:
            return datetime.strptime(date.strip(), fmt).strftime('%Y-%m-%d')
        except ValueError:
            pass
    return None

def get_abstract(file):
    
    soup_abstract = extract_element_soup(file,None,"abstract")
    soup_text=""
    for element_text in soup_abstract:
        soup_text = soup_text + " " + element_text.text
    return soup_text
