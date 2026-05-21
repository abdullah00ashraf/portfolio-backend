path = 'academic_portal/settings.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = [line for line in lines if "'safedelete'," not in line]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
