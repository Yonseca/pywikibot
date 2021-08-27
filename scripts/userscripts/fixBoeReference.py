import pywikibot
import validators
import requests
from bs4 import BeautifulSoup

site = pywikibot.Site()
page = pywikibot.Page(site, u"Usuario:CardoBOT/Taller")
text = page.text

soup = BeautifulSoup(text, features="lxml")
refs = soup.find_all('ref')

for ref in refs:
    refContent = ref.text
    if refContent[0] == '[':
        endSubstring = refContent.find(" ")
        url = refContent[1:endSubstring]
        if validators.url(url):
            htmlBoe = requests.get(url).content
            boeSoup = BeautifulSoup(htmlBoe, features="lxml")
            metadata = boeSoup.find("abbr", title="metadatos")
            if hasattr(metadata, 'next'):
                metadata = metadata.next.split(", ")
                boeNum = metadata[0]
                date = metadata[1][3:]
                pages = metadata[2].split(" ")
                pageStart = pages[1]
                pageEnd = pages[3]

            title = boeSoup.find("h3", class_="documento-tit")
            if hasattr(title, 'next'): 
                if pageStart - pageEnd == 0:
                    refContent = f'{{Cita BOE |referencia= |título={title.next}|fecha={date}|número={boeNum}|página={pageStart}}}'
                else:
                    refContent = f'{{Cita BOE |referencia= |título={title.next}|fecha={date}|número={boeNum}|páginas={pageStart}-{pageEnd}}}'
                print(title.next)
            




#page.text = u"Test, test, test"


#page.save(u"Probando pywikibot después de 7 años...")

