class Node:
    def __init__(self, value=None, data=None, line_number=None):
        self.value = value
        self.data = data
        self.line_number = line_number
        self.children = []

def parse_edn(edn_str):
    root = Node("None")
    stack = [root]
    current_node = root
    current_data = ""
    line_number = 1

    for char in edn_str:
        if char == "\n":
            line_number += 1
        if char == "(":
            stack.append(Node(line_number=line_number))
            current_node.children.append(stack[-1])
            current_node = stack[-1]
            current_data = ""
        elif char == ")":
            if current_data.strip():
                current_node.value = current_data.strip()
            stack.pop()
            if stack:
                current_node = stack[-1]
            current_data = ""
        elif char.isalnum():
            current_data += char
        elif char.isspace() and current_data.strip():
            if current_node.data:
                current_node.value = current_data.strip()
            else:
                current_node.data = current_data.strip()
            current_data = ""

    return root.children

def objects_hierarchy_set(objects_list):
    hierarchy_set = set()
    for obj in objects_list:
        obj_set = ((obj.data, obj.value, obj.line_number),)
        obj_set += tuple(objects_hierarchy_set(obj.children))
        hierarchy_set.add(obj_set)
    return hierarchy_set

def find_changed_objects(objects_list1, objects_list2):
    changed_objects = []

    def compare_objects(node1, node2):
        if node1.value != node2.value or node1.data != node2.data:
            changed_objects.append([(node1.data, node1.value, node1.line_number),(node2.data, node2.value, node2.line_number)])
        for child1, child2 in zip(node1.children, node2.children):
            compare_objects(child1, child2)

    for obj1, obj2 in zip(objects_list1, objects_list2):
        compare_objects(obj1, obj2)

    return changed_objects

def find_changed_hierarchy(node, changed_objects, hierarchy_path):
    if (node.data, node.value, node.line_number) in changed_objects:
        hierarchy_path.append((node.data, node.value, node.line_number))

    for child in node.children:
        find_changed_hierarchy(child, changed_objects, hierarchy_path)

def print_changed_hierarchy(node, changed_objects, hierarchy_path):
    for changed in changed_objects:
        if (node.data == changed[0] and node.value == changed[1]): ## we need to know what has changed!!! and then return the path when we find the changed thing
            hierarchy_path.append((node.data, node.value, node.line_number))
            print("Changed Hierarchy:")
            for path_item in reversed(hierarchy_path):
                print(f"  {path_item[0]} - {path_item[1]} - Line {path_item[2]}")
            print()

    for child in node.children:
        new_path = hierarchy_path + [(node.data, node.value, node.line_number)]
        print_changed_hierarchy(child, changed_objects, new_path)

# Update diff_edns function accordingly
def diff_edns(edn_str1, edn_str2):
    objects_list1 = parse_edn(edn_str1)
    objects_list2 = parse_edn(edn_str2)

    changed_objects = find_changed_objects(objects_list1, objects_list2)
    for changed in changed_objects:
        print(f"diff: file1 -> file2\n    {changed[0][0]} -> {changed[1][0]}\n    {changed[0][1]} -> {changed[1][1]}\nline: {changed[0][2]} -> {changed[1][2]}\n")

    # for obj2 in objects_list2:
    #     print_changed_hierarchy(obj2, changed_objects, [])
    #     print()


# Example usage
with open("osc.edn", "r") as file1, open("osc2.edn", "r") as file2:
    edn_str1 = file1.read()
    edn_str2 = file2.read()

diff_edns(edn_str1, edn_str2)
