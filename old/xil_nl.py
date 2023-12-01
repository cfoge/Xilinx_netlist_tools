class Node:
    def __init__(self, value=None, data=None):
        self.value = value
        self.data = data
        self.children = []

def parse_edn(edn_str):
    root = Node("None")
    stack = [root]
    current_node = root
    current_data = ""

    for char in edn_str:
        if char == "(":
            stack.append(Node())
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

def print_hierarchy(node, depth=0):
    print(" " * (depth * 2) + f"{node.data} - {node.value}")
    for child in node.children:
        print_hierarchy(child, depth + 1)

# Example usage
# edn_str = "(cell IBUF (celltype GENERIC) (view netlist (viewtype NETLIST) (interface (port O (direction OUTPUT)) (port I (direction INPUT)))))"
with open("osc.edn", "r") as file:
    edn_str = file.read()
objects_list = parse_edn(edn_str)

print("Extracted Objects:")
for obj in objects_list:
    print_hierarchy(obj)
print(")")
