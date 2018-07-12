import sys
import csv
import pathlib2
import argparse
from os import listdir, walk
import fnmatch
from os.path import isdir, join, isfile, abspath
from isistan.smartweb.core.SmartWebClient import SmartWebClient

__author__ = 'ignacio'


def main():
    parser = argparse.ArgumentParser(description='Launches the SmartWebClient and runs the experiments.')
    parser.add_argument("dataset_path", help="full path of the dataset that will be used for experiments", type=str)
    parser.add_argument("query_file", help="input query file", type=str)
    parser.add_argument("results_file", help="output results file", type=str)
    parser.add_argument("--address", help="specifies the address of the smartweb server, default=127.0.0.1", default='127.0.0.1', type=str)
    parser.add_argument("--port", help="specifies the port of the smartweb server, default=8080", default='8080', type=str)
    args = parser.parse_args()
    counter = 1
    if isdir(args.dataset_path):
        wsdl_documents = []
        for root, dirnames, filenames in walk(args.dataset_path):
            for filename in fnmatch.filter(filenames, '*.wsdl'):
                if counter <= 30:
                    wsdl_documents.append(pathlib2.Path(abspath(join(root, filename))).as_uri())
                else:
                    break
                counter = counter+1

        registry = SmartWebClient(args.address, args.port)
        registry.publish_services(wsdl_documents)
        with open(args.query_file, 'rb') as query_file:
            with open(args.results_file, 'wb') as results_file:
                query_reader = csv.reader(query_file)
                results_writer = csv.writer(results_file)
                query_number = 0
                for row in query_reader:
                    query = row[0]
                    results = registry.find(query)
                    results_writer.writerow(results)
                    print str(query_number) + " queries processed..."
                    query_number += 1
    else:
        registry = SmartWebClient(args.address, args.port)
        registry.publish_services(args.dataset_path)

if __name__ == "__main__":
    main()
