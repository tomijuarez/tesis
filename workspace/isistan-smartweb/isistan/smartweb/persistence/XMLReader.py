import xml.etree.ElementTree as ElementTree
import urllib2

__author__ = 'ignacio'


class XMLReader(object):
    #
    # XML File Reader

    def __init__(self):
        self._xml_tree = None
        self._xml_root = None

    def _parse_map(file_path):
        """Parses the WSDL file"""
        events = "start", "start-ns", "end-ns"

        root = None
        ns_map = []

        for event, elem in ElementTree.iterparse(file_path, events):
                if event == "start-ns":
                        ns_map.append(elem)
                elif event == "end-ns":
                        ns_map.pop()
                elif event == "start":
                        if root is None:
                                root = elem
                        elem.ns_map = dict(ns_map)
        return ElementTree.ElementTree(root)

    def load_from_file(self, path):
        """Load wsdl from file"""
        self._xml_tree = ElementTree.parse(path)
        self._xml_root = self._xml_tree.getroot()

    def load_from_url(self, url):
        """Load wsdl from url"""
        wsdl = urllib2.urlopen(url)
        self._xml_tree = ElementTree.parse(wsdl)
        self._xml_root = self._xml_tree.getroot()

    def get_elements(self, element_types_list):
        """Return all the elements of the specified types"""
        return self.get_elements_from(self._xml_root, element_types_list)

    @staticmethod
    def get_elements_from(root, element_types_list):
        elements = []
        for element in root.iter():
            tag = element.tag
            for type_elem in element_types_list:
                if '}' in tag:
                    tag = tag.split('}')[1]
                if type_elem == tag:
                    elements.append(element)
        return elements

    def write_to_file(self, path):
        """Write wsdl to file"""
        self._xml_tree.write(path, encoding="UTF-8")
