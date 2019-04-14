import codecs
import re

mapping_file = codecs.open("app/static/mapping_dic.txt", "r", "utf8")
mapping_lines = mapping_file.readlines()
mapping_file.close()

mapping = {};

for line in mapping_lines:
   matches = re.findall(r"\[(.*?)\]", line, re.DOTALL)
   mapping[matches[0]] = matches[1]

def get_abbr_map ():
    return mapping
