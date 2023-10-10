import xml.etree.ElementTree as ET

file_path = 'test_files/lanelet2_map.osm'
# Parse the .osm file
tree = ET.parse(file_path)
root = tree.getroot()
# Create a mapping dictionary for old IDs to new IDs
id_mapping = {}
new_id = 1

# update Node tags
for node in root.findall('.//node'):
    old_id = node.get('id')
    id_mapping[old_id] = str(new_id)
    node.set('id', str(new_id))
    new_id += 1

# update Way tags
for way in root.findall('.//way'):
    old_id = way.get('id')
    id_mapping[old_id] = str(new_id)
    way.set('id', str(new_id))
    new_id += 1

# update Relation tags
for relation in root.findall('.//relation'):
    old_id = relation.get('id')
    id_mapping[old_id] = str(new_id)
    relation.set('id', str(new_id))
    new_id += 1

# Create a list of tags to update (e.g., 'original_polygon_ref')
way_tags_to_update = ['original_polygon_ref']

# Process Way tags to update references to Node IDs and specific tags
for way in root.findall('.//way'):
    for nd in way.findall('.//nd'):
        old_ref = nd.get('ref')
        new_ref = id_mapping.get(old_ref)
        if new_ref:
            nd.set('ref', new_ref)

    # Update specific tags within Way elements
    for tag in way.findall('./tag'):
        tag_key = tag.get('k')
        tag_value = tag.get('v')
        if tag_key in way_tags_to_update:
            old_value = tag_value
            new_value = id_mapping.get(old_value)
            if new_value:
                tag.set('v', new_value)

# Process Relation tags to update references to Way IDs and specific tags
for relation in root.findall('.//relation'):
    for member in relation.findall('.//member[@type="way"]'):
        old_ref = member.get('ref')
        new_ref = id_mapping.get(old_ref)
        if new_ref:
            member.set('ref', new_ref)


def update_relation_members(element):
    for member in element.findall('.//member[@type="relation"]'):
        old_ref = member.get('ref')
        new_ref = id_mapping.get(old_ref)
        if new_ref:
            member.set('ref', new_ref)
            # Find and process the referenced relation recursively
            referenced_relation = root.find(f'.//relation[@id="{new_ref}"]')
            if referenced_relation:
                update_relation_members(referenced_relation)


# Process Relation tags to update references to Relation IDs
for relation in root.findall('.//relation'):
    update_relation_members(relation)


tree.write('lanelet2_map.osm', encoding='utf-8', xml_declaration=True)

# Save the ID mapping to a separate file for manually checking files
with open('id_mapping.txt', 'w') as mapping_file:
    for old_id, new_id in id_mapping.items():
        mapping_file.write(f'{old_id} => {new_id}\n')
