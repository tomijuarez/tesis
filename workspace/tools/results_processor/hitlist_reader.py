import xml.etree.ElementTree as ElementTree
from xml.dom.minidom import parseString

__author__ = 'ignacio'


class HitlistReader(object):
    #
    # Hitlist XML Reader

    HITLIST_TAG_ROOT = 'qryMap'
    HITLIST_TAG_ENTRY = 'entry'
    HITLIST_TAG_KEY = 'key'
    HITLIST_TAG_VALUE = 'value'
    HITLIST_TAG_IDDOC = 'idDoc'

    def __init__(self):
        self._xml_root = None
        self._xml_tree = None

    def load_from_file(self, path):
        self._xml_tree = ElementTree.parse(path)
        self._xml_root = self._xml_tree.getroot()

    def get_elements(self, element_types_list):
        """Return all the elements of the specified types"""
        return self.get_elements_from(self._xml_root, element_types_list)

    @staticmethod
    def get_elements_from(root, element_types_list):
        elements = []
        for element in root.iter():
                for type_elem in element_types_list:
                    if type_elem in element.tag:
                        elements.append(element)
        return elements