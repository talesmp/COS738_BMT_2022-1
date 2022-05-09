import ast
import csv
import re
from collections import Counter, defaultdict
import numpy as np
from utils import init_irs

def main():
    config, logger = init_irs('INDEX')
    logger.info('\n\nInicializando o módulo "INDEXADOR (INDEX)". \n')

    logger.info(' Lendo a configuração de "INDEX".')
    inverted_list_filename = config['LEIA']
    model_filename = config['ESCREVA']

    all_documents_set = set()
    n_i = {}
    f_raw = {}
    max_count_per_document = defaultdict(int)
    with open(inverted_list_filename, newline='') as inverted_list_file:
        inverted_list_csv = csv.reader(inverted_list_file, delimiter=';')
        for w, l in inverted_list_csv:
            if re.match('^[A-Z]{2,}$', w):
                documents = ast.literal_eval(l)
                document_counter = Counter(documents)
                unique_documents = document_counter.keys()
                all_documents_set.update(unique_documents)
                n_i[w] = len(unique_documents)
                f_raw[w] = document_counter
                for d, c in document_counter.items():
                    max_count_per_document[d] = max(max_count_per_document[d], c)

    all_documents = list(all_documents_set)
    all_terms = list(f_raw.keys())
    N = len(all_documents)
    T = len(all_terms)
    term_document_matrix = np.zeros((T, N))
    logger.info(f' Cálculo da matriz termo-documento de dimensão {T} x {N}. \n\n(Calculando...)\n')
    for j, d in enumerate(all_documents):
        for i, t in enumerate(all_terms):
            tf = f_raw[t][d]/max_count_per_document[d]
            idf = np.log(N/n_i[t])
            term_document_matrix[i, j] = tf*idf

    logger.info(f' Salvando o modelo no arquivo binário de formato NumPy em "{model_filename}"')
    with open(model_filename, 'wb') as model:
        np.save(model, all_terms)
        np.save(model, all_documents)
        np.save(model, term_document_matrix)

    logger.info(' Fim do processamento de "INDEX". \n\n')

if __name__ == '__main__':
    main()

