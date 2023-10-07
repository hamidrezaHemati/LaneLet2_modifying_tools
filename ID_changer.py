import xml.etree.ElementTree as ET

# Replace 'your_file.osm' with the path to your .osm file
file_path = 'test_files/test/lanelet2_map.osm'
ID_mapping = {}

# Parse the .osm file
tree = ET.parse(file_path)
root = tree.getroot()

# You can now access and manipulate the XML data through the 'root' element
# Find and iterate through all <node> elements
new_ID = 1
for element in root:
    if element.tag == "MetaInfo":
        continue
    print(element.tag, element.attrib)
    ID_mapping[element.attrib['id']] = new_ID
    new_ID += 1

for key, value in ID_mapping.items():
    print(key, ":", value)

# for node in root.findall('.//node'):
#     node_id = node.get('id')
#     lat = node.get('lat')
#     lon = node.get('lon')
#
#     print(f"Node ID: {node_id}")
#     print(f"Latitude: {lat}")
#     print(f"Longitude: {lon}")
#
#     # Iterate through <tag> elements within the <node>
#     for tag in node.findall('./tag'):
#         tag_key = tag.get('k')
#         tag_value = tag.get('v')
#         print(f"Tag Key: {tag_key}, Tag Value: {tag_value}")
#
#     print("\n")  # Separating each node's data