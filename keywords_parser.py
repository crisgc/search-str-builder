import bibtexparser as bib;
import sys
import string as str
import itertools as itr
from collections import Counter

def main():
    # TODO colocar uma funcionalidade de leitura do arquivo bib a partir da linha de comando
    file_name = 'D:\\00_repositories\\dissertacao\\qualificacao\\search_files\\search_unification.bib'
    with open(file_name) as bib_file:
        bib_db = bib.load(bib_file)
        print len(bib_db.entries)
        key = u'author_keywords'
        authors_key = [str.split(entry[key], sep=';')
                       for entry in bib_db.entries
                       if key in entry]
        
        terms = list(itr.chain.from_iterable(authors_key))

        # Process
        terms = [term.strip().lower() for term in terms]

        counter = Counter(terms)
        items = sorted(counter.items(), key=lambda x : x[1], reverse=True);
        print items
        result = u'\n'.join([unicode(item[1]) + ' ' + item[0] for item in items])
        print result

        with open('result.txt', mode='w') as out_file:
            out_file.write(result)
        
        print terms[0]
    #print authors_key

if __name__=='__main__':
    sys.exit(main())
    
