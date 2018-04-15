import re
from Transformer import Transformer
from isistan.smartweb.persistence.XMLReader import XMLReader
from isistan.smartweb.persistence.WordBag import WordBag

__author__ = 'ignacio'


class WADLTransformer(Transformer):
    #
    # Transform WADL documents into bag of words

    WADL_TAG_APPLICATION = 'application'
    WADL_TAG_GRAMMARS = 'grammars'
    WADL_TAG_DOC = 'doc'
    WADL_TAG_RESOURCES = 'resources'
    WADL_TAG_RESOURCE = 'resource'
    WADL_TAG_METHOD = 'method'
    WADL_TAG_REQUEST = 'request'
    WADL_TAG_PARAM = 'param'
    WADL_TAG_REPRESENTATION = 'representation'

    WADL_ATTRIBUTE_BASE = 'base'
    WADL_ATTRIBUTE_URI = 'uri'
    WADL_ATTRIBUTE_DISPLAYNAME = 'displayName'
    WADL_ATTRIBUTE_ID = 'id'
    WADL_ATTRIBUTE_NAME = 'name'
    WADL_ATTRIBUTE_REQUIRED = 'required'
    WADL_ATTRIBUTE_STYLE = 'style'
    WADL_ATTRIBUTE_TYPE = 'type'

    def __init__(self):
        super(WADLTransformer, self).__init__()
        self._reader = XMLReader()

    def _process_application(self):
        terms = []
        application = self._reader.get_elements([self.WADL_TAG_APPLICATION])[0]
        service_documentation_list = WADLTransformer._process_documentation(self._reader.get_elements_from(
                                                                            application, 
                                                                            [self.WADL_TAG_DOC])[:1])
        if service_documentation_list is not None:
            terms.extend(service_documentation_list)

        resources_list = self._reader.get_elements([self.WADL_TAG_RESOURCES])
        terms.extend(self._process_resources(resources_list[0]))
        return terms

    def _process_resources(self, resources_root):
        terms = []
        resources_list = self._reader.get_elements_from(resources_root, [self.WADL_TAG_RESOURCE])
        for resource in resources_list:
            method_list = self._reader.get_elements_from(resource, [self.WADL_TAG_METHOD])
            for method in method_list:
                terms.extend(WADLTransformer._process_name(method, self.WADL_ATTRIBUTE_DISPLAYNAME))
                terms.extend(WADLTransformer._process_documentation(
                             self._reader.get_elements_from(method, [self.WADL_TAG_DOC])[:1]))
                request = self._reader.get_elements_from(method, [self.WADL_TAG_REQUEST])[0]
                param_list = self._reader.get_elements_from(request, [self.WADL_TAG_PARAM])
                for param in param_list:
                    terms.extend(WADLTransformer._process_name(param, self.WADL_ATTRIBUTE_NAME))
                    """terms.extend(WADLTransformer._process_documentation(
                                    self._reader.get_elements_from(param, [self.WADL_TAG_DOC])))"""
        return terms

    @staticmethod
    def _process_documentation(documentation_list):
        terms = []
        if len(documentation_list) > 0:
            for doc in documentation_list:
                if doc.text is not None:
                    terms.extend(WADLTransformer._process_text(doc.text))
        return terms

    @staticmethod
    def _process_name(operation, attribute):
        if attribute in operation.attrib:
            operation_name = operation.attrib[attribute]
            if len(operation_name.split(':')) > 1:
                operation_name = operation_name.split(':')[1]
            return re.sub(' +', ' ', re.sub("([a-z])([A-Z])", "\g<1> \g<2>",
                                            re.sub(' +', ' ',
                                                   re.sub('[^a-zA-Z ]', ' ',
                                                          operation_name
                                                          )))).split(' ')

    @staticmethod
    def _process_text(documentation):
        return re.sub(' +', ' ', re.sub('[^a-zA-Z ]', ' ', documentation)).split(' ')

    def transform(self, url):
        """Transform a wadl file into a string"""
        self._reader.load_from_url(url)
        return WordBag(self._process_application())
