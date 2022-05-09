import re
from xml.etree import ElementTree
import unidecode
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from utils import init_irs

nltk.download('stopwords')
#nltk.download('punkt')     #descomentar somente se não localizar o pacote 'punkt' e quiser baixar apenas este pacote
#nltk.download('popular')   #descomentar somente se não localizar o pacote 'punkt' e quiser garantir de uma vez baixar outros pacotes importantes

def main():
    config, logger = init_irs('GLI')
    logger.info('\n\nInicializando o módulo "GERADOR LISTA INVERTIDA (GLI)". \n')

    logger.info(' Lendo a configuração de "GLI".')
    xml_filenames = re.split('\s*,\s*', config['LEIA'])
    inverted_list_filename = config['ESCREVA']

    inverted_list = defaultdict(list)
    stopwords_upper = [w.upper() for w in stopwords.words('english')]
    empty_articles = []
    for xml in xml_filenames:
        logger.info(f' Lendo o arquivo XML de nome "{xml}."')
        root = ElementTree.parse(xml).getroot()
        for e in root.findall('RECORD'):
            record_num = e.find('RECORDNUM').text.strip()
            abstract = ''
            if e.findall('ABSTRACT'):
                abstract = e.find('ABSTRACT').text
            elif e.findall('EXTRACT'):
                logger.warning(f' Campo "ABSTRACT" não achado para o registro {record_num}; usando o campo "EXTRACT" no lugar.')
                abstract = e.find('EXTRACT').text

            if not abstract:
                title = ''
                logger.error(f' Conteúdo de "ABSTRACT/EXTRACT" não existente para o registro {record_num} no arquivo {xml}.')
                title = e.find('TITLE').text
                empty_articles.append("___ Arquivo: "+xml+" || Registro: "+record_num+" || Título: "+title+" ___")
                continue

            text = unidecode.unidecode(abstract.replace(';', '').strip().upper())
            for w in word_tokenize(text):
                if w not in stopwords_upper:
                    inverted_list[w].append(record_num)
    if len(empty_articles)>0:
        logger.warning(f'\nLista dos {len(empty_articles)} registros com "ABSTRACT/EXTRACT" inexistentes: \n{empty_articles} \n\n')
    logger.info(f'Compondo o arquivo CSV "{inverted_list_filename}"')
    with open(inverted_list_filename, 'w', newline='') as inverted_list_file:
        inverted_list_csv = csv.writer(inverted_list_file, delimiter=';')

        for w, l in inverted_list.items():
            inverted_list_csv.writerow([w, str(l)])

    logger.info(' Fim do processamento de "GLI". \n\n')

if __name__ == '__main__':
    main()

