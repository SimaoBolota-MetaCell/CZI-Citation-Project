import re
from htmlScraper import *

BIBTEX_AUTHORS_PATTERN = '(?<=author\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_INDIVIDUAL_AUTHOR_PATTERN = "(?:[A-Z][A-Za-z'`-]+,)" + "\\s[A-Z][A-Za-z'`-]+"
BIBTEX_FAMILY_NAME_PATTERN = "(?:[A-Z][A-Za-z'`-]+,)"
BIBTEX_GIVEN_NAMES_PATTERN = "(,\\s[A-Z][A-Za-z'`-]+)"
BIBTEX_YEAR_NUM_PATTERN = '(?<=year\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_YEAR_PATTERN = '(?<=year\\s=\\s)(.*?)(?=,)'
BIBTEX_TITLE_PATTERN = '(?<=title\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_PUBLISHER_PATTERN = '(?<=publisher\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_DOI_PATTERN = '(?<=doi\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_URL_PATTERN = '(?<=URL\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_url_PATTERN = '(?<=url\\s=\\s\{)(.*?)(?=\},)'
BIBTEX_JOURNAL_PATTERN = '(?<=journal\\s=\\s\{)(.*?)(?=\},)'


def get_bibtex_citations(link):

    BIBTEX_PATTERN = '(?<=@)(.*?)(?=\}\s*\})'

    soup = get_html(link )
    snippets = soup.find_all("div", {
                         'class': 'highlight highlight-text-bibtex notranslate position-relative overflow-auto'})
    snippets = str(snippets)

    BibTex_text = strip_tags(snippets)
    BibTex_text = BibTex_text.replace("\xa0", " ")
    BibTex_text = BibTex_text.replace("=", " = ")
    BibTex_text = BibTex_text.replace("]", " }")
    BibTex_text = BibTex_text.replace("{\\~a}", "ã")
    BibTex_text = BibTex_text.replace("{\\'a}", "á")
    BibTex_text = re.sub(' +', ' ', BibTex_text)

    all_bibtex_citations = re.findall(BIBTEX_PATTERN, BibTex_text, flags=re.DOTALL)

    return all_bibtex_citations



def get_bibtex_family_names(individual_citation):
    
    author = re.findall(
            BIBTEX_AUTHORS_PATTERN, individual_citation, flags=re.DOTALL)
    if author:
           author_string = ' '.join(map(str, author))
           individual_author = re.findall(BIBTEX_INDIVIDUAL_AUTHOR_PATTERN , author_string, flags=re.DOTALL)
           individual_author_string = ' '.join(map(str, individual_author))

           family_names = re.findall(BIBTEX_FAMILY_NAME_PATTERN , individual_author_string, flags=re.DOTALL)
           family_names = [w.replace(',', '') for w in family_names]
           return family_names 

def get_bibtex_given_names(individual_citation):
    author = re.findall(
            BIBTEX_AUTHORS_PATTERN, individual_citation, flags=re.DOTALL)
    if author:
           author_string = ' '.join(map(str, author))
           individual_author = re.findall(BIBTEX_INDIVIDUAL_AUTHOR_PATTERN , author_string, flags=re.DOTALL)
           individual_author_string = ' '.join(map(str, individual_author))

           
           given_names =re.findall(BIBTEX_GIVEN_NAMES_PATTERN , individual_author_string, flags=re.DOTALL)
           given_names = [w.replace(', ', '') for w in given_names]

           return given_names

def get_bibtex_year(individual_citation):
    year = re.findall(
            BIBTEX_YEAR_NUM_PATTERN, individual_citation, flags=re.DOTALL)
    if(bool(year)==False):
        
        year = re.findall(
            BIBTEX_YEAR_PATTERN, individual_citation, flags=re.DOTALL)
    if year:
        year = ''.join(map(str, year))
        return year

def get_bibtex_title(individual_citation):
     
     title = re.findall(
            BIBTEX_TITLE_PATTERN, individual_citation, flags=re.DOTALL)
     
     title = ''.join(map(str, title))
     return title

def get_bibtex_publisher(individual_citation):
    
    publisher = re.findall(
            BIBTEX_PUBLISHER_PATTERN, individual_citation, flags=re.DOTALL)
    if (bool(publisher)==False):
        publisher = re.findall(
            '(?<=publisher\\s=\\s\{)(.*?)(?=\{)', individual_citation, flags=re.DOTALL)
    
    publisher = ''.join(map(str, publisher))
    return publisher


def get_bibtex_doi(individual_citation):
     
     doi = re.findall(
            BIBTEX_DOI_PATTERN, individual_citation, flags=re.DOTALL)
     doi = ''.join(map(str, doi))
     return doi



def get_bibtex_url(individual_citation):
    
     url = re.findall(
            BIBTEX_URL_PATTERN, individual_citation, flags=re.DOTALL)
    
     if (bool(url) == False):
         
         url = re.findall(
            BIBTEX_url_PATTERN, individual_citation, flags=re.DOTALL)
     return url

def get_bibtex_journal(individual_citation):
    journal = re.findall(
            BIBTEX_JOURNAL_PATTERN, individual_citation, flags=re.DOTALL)
    return journal






        


