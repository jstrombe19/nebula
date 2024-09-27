# this utility generates cpp/hpp files based on human-readable yml config files


import yaml

with open('../inc/nebula.yml', 'r') as file:
  data = yaml.safe_load(file)


def generate_hpp(data):
  hpp_content = ""

  hpp_content += "#pragma once\n\n"


  for class_data in data['classes']:
    class_name = class_data['name']
    upper_class_name = class_name.upper()
    
    hpp_content += "#ifndef _" + upper_class_name + "_H_\n"
    hpp_content += "#define _" + upper_class_name + "_H_\n\n"
    hpp_content += f"class {class_name} {{\n"
    
    # Add members
    hpp_content += "public:\n"
    for member in class_data['members']:
      hpp_content += f"     {member['type']} {member['name']};\n"

    # Add methods
    for method in class_data['methods']:
      hpp_content += f"     {method['return_type']} {method['name']}("
      params = ", ".join([f"{param['type']} {param['name']}" for param in method['parameters']])  
      hpp_content += f"{params});\n"

    hpp_content += "};\n\n"

    hpp_content += "#endif"
  return hpp_content

hpp_content = generate_hpp(data)

with open('../inc/myclass.hpp', 'w') as file:
  file.write(hpp_content)

