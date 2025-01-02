import os
import argparse
import re

def parse_virtual_class(class_content):
    """
    Parses a virtual class and extracts method declarations.
    :param class_content: Content of the virtual class.
    :return: Class name and a list of method declarations.
    """
    class_pattern = r'class\s+(\w+)\s*\{'
    method_pattern = r'virtual\s+([\w<>:&*\s]+)\s+(\w+)\(([^)]*)\)\s*=\s*0\s*;'

    class_match = re.search(class_pattern, class_content)
    if not class_match:
        raise ValueError("Could not find a valid class declaration.")

    class_name = class_match.group(1)
    methods = re.findall(method_pattern, class_content)

    return class_name, methods

def generate_header(base_class_name, derived_class_name, methods):
    """
    Generates the header file content for the derived implementation class.
    :param base_class_name: Name of the virtual class.
    :param derived_class_name: Name of the new derived class.
    :param methods: List of method declarations.
    :return: Header file content as a string.
    """
    header_guard = f"{derived_class_name.upper()}_HPP"

    header_content = [
        f"#ifndef {header_guard}",
        f"#define {header_guard}",
        "",
        f"#include \"{base_class_name}.hpp\"",
        "",
        f"class {derived_class_name} : public {base_class_name} {{",
        "public:",
        f"    {derived_class_name}() = default;",
        f"    ~{derived_class_name}() override = default;",
        "",
    ]

    for return_type, method_name, args in methods:
        header_content.append(f"    {return_type} {method_name}({args}) override;")

    header_content.append("};")
    header_content.append("")
    header_content.append(f"#endif // {header_guard}")

    return "\n".join(header_content)

def generate_cpp(derived_class_name, methods):
    """
    Generates the cpp file content for the derived implementation class.
    :param derived_class_name: Name of the new derived class.
    :param methods: List of method declarations.
    :return: CPP file content as a string.
    """

    cpp_content = [
        f"#include \"{derived_class_name}.hpp\"",
        ""
    ]

    for return_type, method_name, args in methods:
        cpp_content.append(f"{return_type} {derived_class_name}::{method_name}({args}) {{")
        cpp_content.append("    // TODO: Implement this method")
        if return_type.strip() != "void":
            cpp_content.append(f"    return {return_type.strip()}();")
        cpp_content.append("}")
        cpp_content.append("")

    return "\n".join(cpp_content)

def write_files(header_dir, cpp_dir, derived_class_name, header_content, cpp_content):
    """
    Writes the generated header and cpp content to files.
    :param header_dir: Directory to write the header file.
    :param cpp_dir: Directory to write the cpp file.
    :param derived_class_name: Name of the new derived class.
    :param header_content: Content for the header file.
    :param cpp_content: Content for the cpp file.
    """
    os.makedirs(header_dir, exist_ok=True)
    os.makedirs(cpp_dir, exist_ok=True)

    header_path = os.path.join(header_dir, f"{derived_class_name}.hpp")
    cpp_path = os.path.join(cpp_dir, f"{derived_class_name}.cpp")

    with open(header_path, "w") as header_file:
        header_file.write(header_content)

    with open(cpp_path, "w") as cpp_file:
        cpp_file.write(cpp_content)

def main():
    parser = argparse.ArgumentParser(description="Generate stub files for a virtual class.")
    parser.add_argument("virtual_class_file", help="Path to the file containing the virtual class.")
    parser.add_argument("--header_dir", default="./include", help="Directory to save the header file.")
    parser.add_argument("--cpp_dir", default="./src", help="Directory to save the cpp file.")
    parser.add_argument("--derived_class_name", required=True, help="Name of the new derived class.")

    args = parser.parse_args()

    with open(args.virtual_class_file, "r") as file:
        class_content = file.read()

    base_class_name, methods = parse_virtual_class(class_content)
    header_content = generate_header(base_class_name, args.derived_class_name, methods)
    cpp_content = generate_cpp(args.derived_class_name, methods)

    write_files(args.header_dir, args.cpp_dir, args.derived_class_name, header_content, cpp_content)

if __name__ == "__main__":
    main()
