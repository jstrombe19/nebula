# this utility generates cpp/hpp files based on human-readable yml config files
import yaml

with open('../inc/nebula.yml', 'r') as file:
    data = yaml.safe_load(file)

def generate_hpp(class_data):
    hpp_content = ""
    hpp_content += "// WARNING::Auto-generated file; do not modify this file! \n// If change is necessary, update the corresponding yml and re-generate!\n"
    hpp_content += "#pragma once\n\n"

    class_name = class_data['name']
    screened_class_name = class_name.replace(" ", "")
    upper_class_name = class_name.replace(" ", "_").upper()

    hpp_content += "#ifndef _" + upper_class_name + "_H_\n"
    hpp_content += "#define _" + upper_class_name + "_H_\n\n"

    # Include additional headers if specified
    additional_headers = class_data.get('headers', [])
    for header in additional_headers:
        hpp_content += f"#include \"{header}\"\n"
    hpp_content += "\n"

    hpp_content += f"class {screened_class_name} {{\n"

    # Add members
    hpp_content += "public:\n"
    for member in class_data['members']:
        hpp_content += f"     {member['type']} {member['name']};\n"

    # Check if the class is marked as virtual
    is_virtual_class = class_data.get('virtual', False)

    # Add methods
    for method in class_data['methods']:
        if is_virtual_class:
            hpp_content += f"     virtual {method['return_type']} {method['name']}("  # Virtual and pure virtual
        else:
            hpp_content += f"     {method['return_type']} {method['name']}("  # Regular method
        params = ", ".join([f"{param['type']} {param['name']}" for param in method['parameters']])
        hpp_content += f"{params})"
        hpp_content += " = 0;\n" if is_virtual_class else ";\n"

    hpp_content += "};\n\n"
    hpp_content += "#endif"
    return hpp_content

def write_hpp(data, header_dir):
    for classdata in data['classes']:
        # Skip virtual base classes
        if classdata.get('virtual', False):
            continue

        hpp_content = generate_hpp(classdata)
        classname = f"{header_dir}/{classdata['name'].lower().replace(' ', '_')}.hpp"
        with open(classname, 'w') as file:
            file.write(hpp_content)


def generate_cpp(data):
    cpp_content = ""
    for class_data in data['classes']:
        cpp_content += f"#include \"../inc/{class_data['name'].lower().replace(' ', '_')}.hpp\"\n\n"

        for method in class_data['methods']:
            params = ", ".join([f"{param['type']} {param['name']}" for param in method['parameters']])
            cpp_content += f"{method['return_type']} {class_data['name']}::{method['name']}({params}) {{\n"
            cpp_content += "    // TODO: Implement this method\n"
            if method['return_type'] != "void":
                cpp_content += f"    return {method['return_type']}();\n"
            cpp_content += "}\n\n"

    return cpp_content

def write_cpp(data, source_dir):
    for class_data in data['classes']:
        # Skip virtual base classes
        if class_data.get('virtual', False):
            continue

        cpp_content = generate_cpp(data)
        with open(f"{source_dir}/auto_generated.cpp", 'w') as file:
            file.write(cpp_content)


def generate_derived_hpp(base_class_name, derived_class, base_methods):
    hpp_content = f"#pragma once\n\n"
    hpp_content += f"#include \"../inc/{base_class_name.lower().replace(' ', '_')}.hpp\"\n"
    for header in derived_class.get('headers', []):
        hpp_content += f"#include \"{header}\"\n"
    hpp_content += "\n"

    derived_name = derived_class['name']
    hpp_content += f"class {derived_name} : public {base_class_name} {{\n"
    hpp_content += "public:\n"
    hpp_content += f"    {derived_name}() = default;\n"
    hpp_content += f"    ~{derived_name}() override = default;\n\n"

    for method in base_methods:
        params = ", ".join([f"{param['type']} {param['name']}" for param in method.get('parameters', [])])
        hpp_content += f"    {method['return_type']} {method['name']}({params}) override;\n"

    hpp_content += "};\n\n"
    return hpp_content

def write_derived_hpp(base_class_name, derived_classes, base_methods, header_dir):
    for derived_class in derived_classes:
        hpp_content = generate_derived_hpp(base_class_name, derived_class, base_methods)
        derived_filename = f"{header_dir}/{derived_class['name'].lower().replace(' ', '_')}.hpp"
        with open(derived_filename, 'w') as file:
            file.write(hpp_content)

def generate_derived_cpp(base_class_name, derived_class, base_methods):
    cpp_content = f"#include \"../inc/{derived_class['name'].lower().replace(' ', '_')}.hpp\"\n\n"
    # for header in derived_class.get('headers', []):
    #     cpp_content += f"#include \"{header}\"\n"
    cpp_content += "\n"

    for method in base_methods:
        params = ", ".join([f"{param['type']} {param['name']}" for param in method.get('parameters', [])])
        cpp_content += f"{method['return_type']} {derived_class['name']}::{method['name']}({params}) {{\n"
        cpp_content += "    // TODO: Implement this method\n"
        if method['return_type'] != "void":
            cpp_content += f"    return {method['return_type']}();\n"
        cpp_content += "}\n\n"

    return cpp_content

def write_derived_cpp(base_class_name, derived_classes, base_methods, source_dir):
    for derived_class in derived_classes:
        cpp_content = generate_derived_cpp(base_class_name, derived_class, base_methods)
        derived_filename = f"{source_dir}/{derived_class['name'].lower().replace(' ', '_')}.cpp"
        with open(derived_filename, 'w') as file:
            file.write(cpp_content)

def main(data, header_dir="../inc", source_dir="../src"):
    # Skip regeneration of base classes in both HPP and CPP
    for class_data in data['classes']:
        derived_classes = class_data.get('derived_classes', [])
        if class_data.get('virtual', False):
            base_methods = class_data['methods']
            write_derived_hpp(class_data['name'], derived_classes, base_methods, header_dir)
            write_derived_cpp(class_data['name'], derived_classes, base_methods, source_dir)

# Run the script
import sys
header_dir = sys.argv[1] if len(sys.argv) > 1 else "../inc"
source_dir = sys.argv[2] if len(sys.argv) > 2 else "../src"
main(data, header_dir, source_dir)

