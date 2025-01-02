# this utility generates cpp/hpp files based on human-readable yml config files
import yaml

with open('../inc/nebula.yml', 'r') as file:
  data = yaml.safe_load(file)


def generate_hpp(class_data):
  hpp_content = ""
  hpp_content += "// WARNING::Auto-generated file; do not modify this file! \n// If change is necessary, update the corresponding yml and re-generate!\n"
  hpp_content += "#pragma once\n\n"


  # for class_data in data['classes']:
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

  # Add methods
  for method in class_data['methods']:
    hpp_content += f"     virtual {method['return_type']} {method['name']}("
    params = ", ".join([f"{param['type']} {param['name']}" for param in method['parameters']])  
    hpp_content += f"{params});\n"

  hpp_content += "};\n\n"

  hpp_content += "#endif"
  return hpp_content

def write_hpp(data):
  for classdata in data['classes']:
    hpp_content = generate_hpp(classdata)

    classname = '../inc/' + classdata['name'].lower().replace(" ", "_") + '.hpp'
    with open(classname, 'w') as file:
      file.write(hpp_content)


write_hpp(data)


# hpp_content = generate_hpp(data)

# with open('../inc/myclass.hpp', 'w') as file:
#   file.write(hpp_content)


def generate_cpp(data):
  cpp_content = ""
  cpp_content += "#include \"../inc/" + data['classes']['name'] + "\"\n"

  for class_data in data['classes']:
    for method in class_data['methods']:
      cpp_content += f"     {method['return_type']} {method['name']}("
      params = ", ".join([f"{param['type']} {param['name']}" for param in method['parameters']])
      cpp_content += f"{params});\n"
    

  return cpp_content

# cpp_content = generate_cpp(data)

# with open('../src/myclass.cpp', 'w') as file:
#   file.write(cpp_content)
