import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Instead of complex regex, we'll just replace the specific button onClick text.

content = re.sub(
    r"onClick=\{\(\) => \{\s*if \(!props\.salesHistory\?\.length\) return toast\.error\('No data'\);[\s\S]*?download = 'sales_history\.csv'; a\.click\(\);\s*\}\}",
    "onClick={() => setExportModalState({ isOpen: true, type: 'sales', format: 'csv' })}",
    content
)

content = re.sub(
    r"onClick=\{\(\) => \{\s*if \(!props\.stockHistory\?\.length\) return toast\.error\('No data'\);[\s\S]*?download = 'stock_history\.csv'; a\.click\(\);\s*\}\}",
    "onClick={() => setExportModalState({ isOpen: true, type: 'stock', format: 'csv' })}",
    content
)

content = re.sub(
    r"onClick=\{\(\) => \{\s*if \(!props\.products\?\.length\) return toast\.error\('No data'\);[\s\S]*?download = 'products\.csv'; a\.click\(\);\s*\}\}",
    "onClick={() => setExportModalState({ isOpen: true, type: 'products', format: 'csv' })}",
    content
)

content = re.sub(
    r"onClick=\{\(\) => \{\s*if \(!props\.customers\?\.length\) return toast\.error\('No data'\);[\s\S]*?download = 'customers\.csv'; a\.click\(\);\s*\}\}",
    "onClick={() => setExportModalState({ isOpen: true, type: 'customers', format: 'csv' })}",
    content
)

content = re.sub(
    r"onClick=\{\(\) => \{\s*if \(!props\.debts\?\.length\) return toast\.error\('No data'\);[\s\S]*?download = 'debts\.csv'; a\.click\(\);\s*\}\}",
    "onClick={() => setExportModalState({ isOpen: true, type: 'debts', format: 'csv' })}",
    content
)

content = re.sub(
    r"onClick=\{\(\) => \{\s*if \(!props\.suppliers\?\.length\) return toast\.error\('No data'\);[\s\S]*?download = 'suppliers\.csv'; a\.click\(\);\s*\}\}",
    "onClick={() => setExportModalState({ isOpen: true, type: 'suppliers', format: 'csv' })}",
    content
)


with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced inline handlers with modal state")
