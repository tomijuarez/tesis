# -*- coding: utf-8 -*-
import codecs
import csv
from nltk.corpus import stopwords
import unicodedata

class variablesGlobales(object):

    def __init__(self):
        self.recognized_entities = 0
        self.count_queries = 0
        self.cached_entity_count = 0
        self.current_document = 1
        self.rowsContexts = [['#Doc','Entidad','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15']]
        self.rowsResults = [['#Doc', 'Entidad','Jaccard','Jaccard','SpaCy','SpaCy','SorensenDice','SorensenDice', 'Dist Cos', 'Dist Cos'],['', '','textoElegido', 'resultado','textoElegido', 'resultado','textoElegido', 'resultado','textoElegido', 'resultado']]

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
            ''' 
            with codecs.open('resultados.csv', 'a', encoding="utf8") as csv_file:
                text = 'Pokémon_(video_game_series)'
                print 'row'
                print row
                #[152, u'Pokemon', u'Pok\xe9mon_(video_game_series)', 0.045454545454545456, 
                #u'Q1079748_EN', 0.7778036768539751, u'Pok\xe9mon_(video_game_series)', 0.08695652173913043]
                csv_file.write(str(row[0])+','+row[1]) #Doc + Entidad
                csv_file.write(unicodedata.normalize('NFKD', row[2]).encode('ascii', 'ignore'))

                csv_file.write(unicode(row[2], encoding="utf8")+','+str(row[3])) #(Jaccard) id + value 
                csv_file.write(unicode(row[4], encoding="utf8")+','+str(row[5])) #(SpaCy) id + value 
                csv_file.write(unicode(row[6], encoding="utf8")+','+str(row[7])) #(SorensenDice) id + value 
                csv_file.write(unicode(row[8], encoding="utf8")+','+str(row[9])) #(Dist Cos) id + value 
                csv_file.write(+u'\n') #(Dist Cos) id + value 
                '''


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

