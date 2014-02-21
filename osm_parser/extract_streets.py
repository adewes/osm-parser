import sys
import os
import json

from lxml import etree

def extract_street_nodes(root):
    """
    Extract all street nodes from the XML tree
    """
    way_objects = []

    ways = [node for node in root if node.tag == 'way' and [tag for tag in node if tag.tag == "tag" and "k" in tag.attrib and tag.attrib["k"] == "highway"] ]

    def extract_k_values(parent):
        """
        Extract the "k" values of a street node
        """
        return  dict([(node.attrib["k"],node.attrib["v"]) for node in parent if node.tag == "tag" and "k" in node.attrib])

    def extract_nodes(parent):
        """
        Extract the IDs and coordinates of all nodes of a given street.
        """
        node_ids = [node.attrib["ref"] for node in parent if node.tag == "nd"]
        nodes = [node for node in root if node.tag == "node" and node.attrib["id"] in node_ids]

        node_objects = []

        for node in nodes:
            node_object = {
                'id' : node.attrib["id"],
                'lat' : node.attrib["lat"],
                "lon" : node.attrib["lon"]
            }
            node_objects.append(node_object)

        return node_objects


    for way in ways:

        way_object = {
            'id' : way.attrib["id"],
            'nodes' : extract_nodes(way),
        }
        way_object.update(extract_k_values(way))
        way_objects.append(way_object)

    return way_objects

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Usage: %(filename)s filename [output filename]" % {'filename' : os.path.basename(__file__)}

    filename = sys.argv[1]

    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
    else:
        output_filename = None

    print "Loading data from %s" % filename

    with open(filename,"r") as input_file:
        content = input_file.read()

    root = etree.fromstring(content)
    streets = extract_street_nodes(root)

    #If we defined an output filename, write the results to it, otherwise just print them to stdout
    if output_filename:
        with open(output_filename,"w") as output_file:
            output_file.write(json.dumps(streets,indent = 2))
    else:
        print json.dumps(street,indent = 2)