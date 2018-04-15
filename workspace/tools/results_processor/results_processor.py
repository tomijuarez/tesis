import sys
import csv
from os import listdir
from os.path import isdir, join, isfile
from hitlist_reader import HitlistReader
from metrics import *

__author__ = 'ignacio'


HIT_SIMBOL = 1
NO_HIT_SIMBOL = 0
RESULTS_WINDOW_SIZE = 10

def main():
    if len(sys.argv) > 3:
        if isfile(sys.argv[1]) and isfile(sys.argv[2]):
            hitlist_map = {}
            print 'processing results...'
            hitlist_reader = HitlistReader()
            hitlist_reader.load_from_file(sys.argv[1])
            query_id = 0
            for mapping in hitlist_reader.get_elements([HitlistReader.HITLIST_TAG_VALUE]):
                relevants = []
                for relevant in hitlist_reader.get_elements_from(mapping, [HitlistReader.HITLIST_TAG_IDDOC]):
                    relevants.append(relevant.text)
                hitlist_map[query_id] = relevants
                query_id += 1

            query_id = 0
            with open(sys.argv[2], 'rb') as results_file:
                with open(sys.argv[3], 'wb') as processed_results_file:
                    results_reader = csv.reader(results_file)
                    #processed_results_writer = csv.writer(processed_results_file)
                    matrix = []
                    n_relevant_array = []
                    for results in results_reader:
                        if any(field.strip() for field in results):
                            #processed_results_row = []
                            #processed_results_row.insert(0, len(hitlist_map[query_id]))
                            n_relevant_array.append(len(hitlist_map[query_id]))
                            row = []
                            if len(results) < RESULTS_WINDOW_SIZE:
                                results = results[0:len(results)]
                            else:
                                results = results[0:RESULTS_WINDOW_SIZE]
                            for result in results:
                                result_wsdl = result.split("/")
                                result_wsdl = result_wsdl[len(result_wsdl)-1]
                                if result_wsdl in hitlist_map[query_id]:
                                    row.append(HIT_SIMBOL)
                                else:
                                    row.append(NO_HIT_SIMBOL)
                            while len(row) < RESULTS_WINDOW_SIZE:
                            	row.append(NO_HIT_SIMBOL)
                            matrix.append(row)
                            query_id += 1
                    write_matrix_to_file(matrix, sys.argv[3])
                    processed_results_file.write('NDCG(avg): ' + str(average_ndcg(matrix)) + '\n' + '\n')
                    for i in range(0, RESULTS_WINDOW_SIZE):
                        processed_results_file.write('Recall at ' + str(i+1) + '(avg): ' + str(average_recall([x[:i+1] for x in matrix], n_relevant_array)) + "\n")                   
                    precision_array = average_precision(matrix, 0, RESULTS_WINDOW_SIZE)
                    for i in range(len(precision_array)):
                        processed_results_file.write('\n' + 'Precision at ' + str(i + 1) + ': ' + str(precision_array[i]))
            print 'done'
        else:
            print 'invalid arguments'
    else:
        print 'invalid number of arguments'

def write_matrix_to_file(matrix, filename):
    out = ''

    for row in matrix:
        for element in row:
            out += str(element)
        out += '\n'

    filename = filename.split('.')[0] + '_matrix.txt'
    with open(filename,'wt') as file:
        file.write(out)

if __name__ == "__main__":
    main()