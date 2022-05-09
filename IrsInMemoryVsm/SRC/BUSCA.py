import csv
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from utils import init_irs

def main():
    config, logger = init_irs('BUSCA')
    logger.info('\n\nInicializando o módulo "BUSCADOR (BUSCA)". \n')

    logger.info(' Lendo a configuração de "BUSCA".')
    model_filename = config['MODELO']
    query_filename = config['CONSULTAS']
    results_filename = config['RESULTADOS']

    logger.info(f' Carregando o modelo presente em "{model_filename}"')
    with open(model_filename, 'rb') as model:
        all_terms = np.load(model)
        all_documents = np.load(model)
        term_document_matrix = np.load(model)

    T = len(all_terms)
    N = len(all_documents)
    queries = []
    all_queries = np.empty((T, 0))
    logger.info(f' Analisando as consultas em "{query_filename}"')
    with open(query_filename, newline='') as query:
        query_csv = csv.reader(query, delimiter=';')
        header = query_csv.__next__()
        for query_number, query_text in query_csv:
            queries.append(query_number)
            query = np.zeros((T, 1))
            for w in word_tokenize(query_text):
                result = np.where(all_terms == w)
                if len(result[0]) > 0:
                    index = result[0][0]
                    query[index, 0] = 1
            all_queries = np.concatenate([all_queries, query], axis=1)

    logger.info(' Cálculo das similaridades.\n\n(Calculando...)\n')
    inner_product = np.dot(all_queries.transpose(), term_document_matrix)
    norm_query = np.linalg.norm(all_queries, axis=0).reshape(-1, 1)
    norm_model = np.linalg.norm(term_document_matrix, axis=0).reshape(1, -1)
    norm_product = np.dot(norm_query, norm_model)
    results = inner_product/norm_product
    sorted_results = np.argsort(-results)

    logger.info(f' Escrevendo os resultados em "{results_filename}"')
    with open(results_filename, 'w', newline='') as results_file:
        results_csv = csv.writer(results_file, delimiter=';')

        for i, query in enumerate(queries):
            total_results = sum(results[i, :] != 0)
            for j in range(total_results):
                order = j + 1
                document_index = sorted_results[i, j]
                document = all_documents[document_index]
                distance = results[i, document_index]
                results_csv.writerow([query, str([order, document, distance])])

    logger.info(' Fim do processamento de "BUSCA". \n\n')

if __name__ == '__main__':
    main()

