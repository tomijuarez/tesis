import csv
from nltk.corpus import stopwords

class variablesGlobales(object):

    def __init__(self):
        self.recognized_entities = 0
        self.count_queries = 0
        self.cached_entity_count = 0
        self.current_document = 1
        self.rowsContexts = [['#Doc','Entidad','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15']]
        self.rowsResults = [['#Doc', 'Entidad','Jaccard','Jaccard','SpaCy','SpaCy','SorensenDice','SorensenDice', 'Dist Cos', 'Dist Cos'],['', '','idElegida', 'resultado','idElegida', 'resultado','idElegida', 'resultado','idElegida', 'resultado']]

        self.stop_words = set(stopwords.words("english"))  # load stopwords

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

    def add_row(self, row, nameArch):
        if(nameArch == 'contexts'):
            self.rowsContexts.append(row)
        else:
            self.rowsResults.append(row)

    def exports_rows(self):
        with open('contextosXEntidad.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.rowsContexts)
        f.close()

        with open('resultados.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.rowsResults)
        f.close()

    def get_stop_words(self):
        return self.stop_words

