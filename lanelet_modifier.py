import xml.etree.ElementTree as ET
import os

# Path of the file you want to update its ID's
file_path = 'test_files/lanelet2_map.osm'
output_directory = 'updated_file'
# Path of the files you want to display_comparison to each other
file_path_A = 'compare_test/A/lanelet2_map.osm'
file_path_B = 'compare_test/B/lanelet2_map.osm'

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
    with open('id_mapping.txt', 'w') as mapping_file:
        for old_id, new_id in id_mapping.items():
            mapping_file.write(f'{old_id} => {new_id}\n')


def tag_extractor(root_tag, root):
    _list = []
    # Iterate through the <node> elements (you can also do this for <way> and <relation> elements)
    for node in root.findall(f'.//{root_tag}'):
        # Iterate through the <tag> elements within each <node> element
        for tag in node.findall('./tag'):
            # Get the value of the 'k' attribute and append it to the list
            tag_key = tag.get('k')
            if root_tag != 'node' and (tag_key == 'type' or tag_key == 'subtype'):
                tag_value = tag.get('v')
                _list.append((tag_key, tag_value))
            else:
                _list.append(tag_key)

    # Remove duplicates by converting the list to a set and back to a list (if needed)
    return list(set(_list))


def venn_diagram(list_A, list_B):
    set_A = set(list_A)
    set_B = set(list_B)
    # Elements in list A but not in list B
    elements_in_A_not_in_B = set_A - set_B
    # Elements in list B but not in list A
    elements_in_B_not_in_A = set_B - set_A
    # Elements common to both lists
    common_elements = set_A.intersection(set_B)

    # Convert the results back to lists
    unique_to_A = list(elements_in_A_not_in_B)
    unique_to_B = list(elements_in_B_not_in_A)
    common_elements_list = list(common_elements)
    return unique_to_A, unique_to_B, common_elements_list


def display_comparison(list_A, list_B):
    unique_to_A, unique_to_B, common_elements_list = venn_diagram(list_A, list_B)
    # Print common elements in green
    print("\033[92mCommon elements:", common_elements_list)
    # Reset the color to default
    print("\033[0m")
    # Print elements in A but not in B in red
    print("\033[91mElements in A but not in B:", unique_to_A)
    # Reset the color to default
    print("\033[0m")
    # Print elements in B but not in A in red
    print("\033[91mElements in B but not in A:", unique_to_B)
    # Reset the color to default
    print("\033[0m")
    print("-----------------------------------------------------------------------")


def compare():
    # Parse the .osm file
    treeA = ET.parse(file_path_A)
    rootA = treeA.getroot()
    treeB = ET.parse(file_path_B)
    rootB = treeB.getroot()
    # file A
    node_tags_A = tag_extractor('node', rootA)
    way_tags_A = tag_extractor('way', rootA)
    relation_tags_A = tag_extractor('relation', rootA)
    # file B
    node_tags_B = tag_extractor('node', rootB)
    way_tags_B = tag_extractor('way', rootB)
    relation_tags_B = tag_extractor('relation', rootB)

    print('Nodes')
    display_comparison(node_tags_A, node_tags_B)
    print('Ways')
    display_comparison(way_tags_A, way_tags_B)
    print('Relations')
    display_comparison(relation_tags_A, relation_tags_B)


def modify_lanelet():
    # ID reset
    # update_ids()
    # save_id_mapping()
    # deleting extra tags
    node_tags_to_delete = ['along_slope', 'lane_width', 'heading', 'shoulder_width', 'cross_slope', 'curvature']
    delete_tags_from_nodes(node_tags_to_delete)


def main():
    # modify lanelet2 file
    # modify_lanelet()

    # comparing lanelet files
    compare()


if __name__ == '__main__':
    main()


