import xml.etree.ElementTree as ET
import os

# Path of the file you want to update its ID's
file_path = 'modify/original/lanelet2_map.osm'
output_directory = 'modify/modified'

# Create a mapping dictionary for old IDs to new IDs
id_mapping = {}


def get_output_file_path():
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Construct the output file path
    output_file_path = os.path.join(output_directory, os.path.basename(file_path))
    return output_file_path


def update_relation_members(root, element):
    for member in element.findall('.//member[@type="relation"]'):
        old_ref = member.get('ref')
        new_ref = id_mapping.get(old_ref)
        if new_ref:
            member.set('ref', new_ref)
            # Find and process the referenced relation recursively
            referenced_relation = root.find(f'.//relation[@id="{new_ref}"]')
            if referenced_relation:
                update_relation_members(referenced_relation, element)


def update_tags(root, new_id, tag_name):
    for node in root.findall(f'.//{tag_name}'):
        old_id = node.get('id')
        id_mapping[old_id] = str(new_id)
        node.set('id', str(new_id))
        new_id += 1
    return new_id


def update_ids():
    tree = ET.parse(file_path)
    root = tree.getroot()

    new_id = 1
    # update Node tags
    new_id = update_tags(root, new_id, 'node')
    # update Way tags
    new_id = update_tags(root, new_id, 'way')
    # update Relation tags
    new_id = update_tags(root, new_id, 'relation')

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
    # Process Relation tags to update references to Relation IDs
    for relation in root.findall('.//relation'):
        update_relation_members(root, relation)

    # Write the modified XML back to the output file
    tree.write(get_output_file_path(), encoding='utf-8', xml_declaration=True)


def delete_tags_from_nodes(node_tags_to_delete):
    # Parse the .osm file
    tree = ET.parse(get_output_file_path())
    root = tree.getroot()
    # Iterate through the <node> elements
    for node in root.findall('.//node'):
        # Iterate through the <tag> elements within each <node> element
        tags_to_delete = []
        for tag in node.findall('./tag'):
            tag_key = tag.get('k')
            if tag_key in node_tags_to_delete:
                tags_to_delete.append(tag)

        # Delete the specified tags within <node> elements
        for tag in tags_to_delete:
            node.remove(tag)
    # Write the modified XML back to the same file
    tree.write(get_output_file_path(), encoding='utf-8', xml_declaration=True)


def save_id_mapping():
    # Save the ID mapping to a separate file for manually checking files
    with open('modify/id_mapping.txt', 'w') as mapping_file:
        for old_id, new_id in id_mapping.items():
            mapping_file.write(f'{old_id} => {new_id}\n')


def modify_lanelet():
    # ID reset
    update_ids()
    save_id_mapping()

    # deleting extra tags
    node_tags_to_delete = ['along_slope', 'lane_width', 'heading', 'shoulder_width', 'cross_slope', 'curvature']
    delete_tags_from_nodes(node_tags_to_delete)


def main():
    modify_lanelet()


if __name__ == '__main__':
    main()


