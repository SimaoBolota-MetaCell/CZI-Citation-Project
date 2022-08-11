
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re
import yaml


# takes url input and stores HTML of page
html = requests.get(
    'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README.md').text
# html = requests.get('https://github.com/ebouilhol/napari-DeepSpot/blob/main/README.md').text
soup = BeautifulSoup(html, 'html5lib')
print(soup)  # check if page HTML is correct

paragraphs = soup.find_all('p')
paragraphs = str(paragraphs)
# print(paragraphs) # check if right elements

snippets = soup.find_all("div", {
                         'class': 'highlight highlight-text-bibtex notranslate position-relative overflow-auto'})
snippets = str(snippets)
# print(snippets)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


APA_text = strip_tags(paragraphs)  # strip HTML
APA_text = APA_text.replace("\xa0", " ")  # for stray strings
# print(APA_text)


BibTex_text = strip_tags(snippets)
BibTex_text = BibTex_text.replace("\xa0", " ")
BibTex_text = BibTex_text.replace("=", " = ")
BibTex_text = BibTex_text.replace("{\\~a}", "ã")
BibTex_text = BibTex_text.replace("{\\'a}", "á")
BibTex_text = re.sub(' +', ' ', BibTex_text)
print(BibTex_text)

all_bibtex_citations = re.findall(
    '(?<=@article)(.*?)(?=\}\s*\})', BibTex_text, flags=re.DOTALL)


if all_bibtex_citations:
    for citation in all_bibtex_citations:
        print('Citation :')
        print(citation)

        author = re.findall(
            '(?<=author\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if author:
            print('author found')
            print(author)

        year = re.findall(
            '(?<=year\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if year:
            print('year found')
            print(year)

        title = re.findall(
            '(?<=title\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if title:
            print('title found')
            print(title)

        publisher = re.findall(
            '(?<=publisher\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if publisher:
            print('publisher found')
            print(publisher)

        doi = re.findall(
            '(?<=doi\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if doi:
            print('doi found')
            print(doi)

        url = re.findall(
            '(?<=URL\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if url:
            print('url found')
            print(url)

        journal = re.findall(
            '(?<=journal\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if journal:
            print('journal found')
            print(journal)


dict_file = [{'authors': [{'family-names': ['1', '2']}, 'given-names']},
             {'cff-version': '1.2.0'},
             {'message': ''},
             {'title': ''},
             {'identifiers': [{'description': ''},
                              {'type': 'doi'}, {'value': ''}]},
             {'repository-code': ''},
             {'repository': ''},

             ]

with open(r'CITATION.cff', 'w') as file:
    documents = yaml.dump(dict_file, file)
