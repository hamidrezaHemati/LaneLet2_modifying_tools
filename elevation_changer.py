import xml.etree.ElementTree as ET
import os

# Path of the file you want to update its elevation tags
file_path = 'elevation/lanelet2_map.osm'
output_directory = 'elevation/updated_file'


def get_output_file_path():
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Construct the output file path
    output_file_path = os.path.join(output_directory, os.path.basename(file_path))
    return output_file_path


def get_average_ele(root):
    counter = 0
    sum = 0
    for node in root.findall('.//node'):
        for tag in node.findall('./tag'):
            tag_key = tag.get('k')
            if tag_key == "ele":
                ele = float(tag.get('v'))
                sum += ele
                counter += 1
                break
    return round(sum/counter, 2)


def change_elevations_value(tree, root, avg):
    for node in root.findall('.//node'):
        for tag in node.findall('./tag'):
            tag_key = tag.get('k')
            if tag_key == "ele":
                tag.set('v', str(avg))
    tree.write(get_output_file_path(), encoding='utf-8', xml_declaration=True)


def main():
    print("start")
    tree = ET.parse(file_path)
    root = tree.getroot()
    avg = get_average_ele(root)
    print(avg)
    change_elevations_value(tree, root, avg)


if __name__ == '__main__':
    main()