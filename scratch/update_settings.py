import os

path = 'academic_portal/settings.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "'import_export'," in line:
        new_lines.append("    'safedelete',\n")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
