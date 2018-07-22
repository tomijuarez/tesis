import csv

class variablesGlobales(object):

    def __init__(self):
        self.recognized_entities = 0
        self.count_queries = 0
        self.cached_entity_count = 0
        self.current_document = 1
        self.rows = []

    def get_reconognized_entities(self):
        return self.recognized_entities

    def increment_reconognized_entities(self):
        self.recognized_entities += 1

    def get_count_queries(self):
        return self.count_queries

    def increment_count_queries(self):
        self.count_queries += 1

    def get_cached_entity_count(self):
        return self.cached_entity_count

    def increment_cached_entity_count(self):
        self.cached_entity_count += 1

    def get_current_document(self):
        return self.current_document

    def increment_current_document(self):
        self.current_document += 1

    def add_row(self, row):
        self.rows.append(row)

    def set_header(self, header):
        self.rows.insert(0,header)

    def set_name(self, name):
        self.file_name = name

    def exports_rows(self):
        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.rows)

