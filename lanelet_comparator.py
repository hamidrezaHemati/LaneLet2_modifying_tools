import xml.etree.ElementTree as ET

file_path = 'compare_test/A/lanelet2_map.osm'
# Parse the .osm file
tree = ET.parse(file_path)
root = tree.getroot()

items_list = []


def append(item_to_check):
    if item_to_check not in items_list:
        items_list.append(item_to_check)


for element in root:
    append(element.tag)

print(items_list)


