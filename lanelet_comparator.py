import xml.etree.ElementTree as ET

file_path_A = 'compare_test/A/Shinjuku.osm'
file_path_B = 'compare_test/B/kashiwa_standard.osm'
# Parse the .osm file
treeA = ET.parse(file_path_A)
rootA = treeA.getroot()

treeB = ET.parse(file_path_B)
rootB = treeB.getroot()


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


def compare(list_A, list_B):
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


# file A
node_tags_A = tag_extractor('node', rootA)
way_tags_A = tag_extractor('way', rootA)
relation_tags_A = tag_extractor('relation', rootA)
# file B
node_tags_B = tag_extractor('node', rootB)
way_tags_B = tag_extractor('way', rootB)
relation_tags_B = tag_extractor('relation', rootB)

print('Nodes')
compare(node_tags_A, node_tags_B)
print('Ways')
compare(way_tags_A, way_tags_B)
print('Relations')
compare(relation_tags_A, relation_tags_B)









