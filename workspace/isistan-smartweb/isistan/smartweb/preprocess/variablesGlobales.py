class variablesGlobales(object):

    def __init__(self):
        self.recognized_entities = 0
        self.count_queries = 0
        self.cached_entity_count = 0

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