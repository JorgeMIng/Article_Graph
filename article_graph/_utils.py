"""
Utility functions for the article graph.
"""

from datetime import datetime


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
