import xml.etree.ElementTree as ET

file_path = 'test_files/test/lanelet2_map.osm'
# Parse the .osm file
tree = ET.parse(file_path)
root = tree.getroot()
# Create a mapping dictionary for old IDs to new IDs
id_mapping = {}
current_id = 1

print("debug 1")
# Process Node tags
for node in root.findall('.//node'):
    print("debug 2")
    old_id = node.get('id')
    print(old_id)
    id_mapping[old_id] = str(current_id)
    node.set('id', str(current_id))
    current_id += 1

# Process Way tags
for way in root.findall('.//way'):
    old_id = way.get('id')
    id_mapping[old_id] = str(current_id)
    way.set('id', str(current_id))
    current_id += 1

# Process Relation tags
for relation in root.findall('.//relation'):
    old_id = relation.get('id')
    id_mapping[old_id] = str(current_id)
    relation.set('id', str(current_id))
    current_id += 1

# Write the modified XML back to a file
tree.write('new_file.xml', encoding='utf-8', xml_declaration=True)

# Save the ID mapping to a separate file (if needed)
with open('id_mapping.txt', 'w') as mapping_file:
    for old_id, new_id in id_mapping.items():
        mapping_file.write(f'{old_id} => {new_id}\n')
