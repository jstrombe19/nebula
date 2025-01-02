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

def write_hpp(data):
  for classdata in data['classes']:
    hpp_content = generate_hpp(classdata)

    classname = '../inc/' + classdata['name'].lower().replace(" ", "_") + '.hpp'
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

def write_cpp(data):
  cpp_content = generate_cpp(data)
  with open('../src/auto_generated.cpp', 'w') as file:
    file.write(cpp_content)

# Write the header and cpp files
write_hpp(data)
write_cpp(data)
