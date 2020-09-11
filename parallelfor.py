# Python XML Processing Module
import xml.etree.ElementTree as ET

from joblib import Parallel, delayed

FILE = 'path/to/your/file'

tree = ET.parse(FILE)
dataset = tree.getroot()

def process_node(xml_node):
    # extract some information from
    # the xml node

    return 'node information'

# n_jobs=1 means: use all available cores
element_information = Parallel(n_jobs=-1)(delayed(process_node)(node) for node in dataset)
