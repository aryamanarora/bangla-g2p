# scrape words from the digitzed Learner's Hindi-English Dictionary
# clean up Wiktionary translit

from bs4 import BeautifulSoup
import urllib.request
import unicodedata
import re

pattern = re.compile(r'\[[^\[]*?\]')
compounds = re.compile(r'\].*?([^\s]+).*?\[([^\]\s]+)')

def scrape():
    dic = 'bhattacharya'
    PAGES = 411
    with open('bn_pron.csv', 'w') as fout:
        fout.write('word,ipa,altipa,type\n')
        for page in range(1, PAGES + 1):
            print(page)
            link = 'https://dsalsrv04.uchicago.edu/cgi-bin/app/' + dic + '_query.py?page=' + str(page)
            with urllib.request.urlopen(link) as resp:
                soup = BeautifulSoup(resp, 'html.parser')
                entries = soup.find(class_='hw_result')
                for entry in entries.find_all('div'):
                    word = entry.span.get_text()
                    entry.extract()
                    try:
                        ipa = pattern.search(str(entry)).group(0)[1:-1].split('/')
                        altipa = ""
                        if len(ipa) > 1: altipa = ipa[1]
                        ipa = ipa[0]
                        for variant in word.split(','):
                            fout.write(f'"{variant.strip()}","{ipa}","{altipa}",headword\n')
                        for word2, ipa2 in compounds.findall(str(entry)):
                            altipa2 = ""
                            if ipa2[0] == '̃':
                                if altipa != "": altipa2 = altipa + ipa2[1:]
                                ipa2 = ipa + ipa2[1:]
                            fout.write(f'"{word2}","{ipa2}","{altipa2}",derivation\n')
                    except:
                        print(f'error at {word}')
                        print(entry)

if __name__ == '__main__':
    scrape()