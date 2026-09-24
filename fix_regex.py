import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix literal newlines inside strings
content = re.sub(r"headers = '([^']+)\n';", r"headers = '\1\\n';", content)
content = re.sub(r"\)\.join\('\n'\);", r").join('\\n');", content)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Regex fixed")
