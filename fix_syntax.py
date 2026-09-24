with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("headers = 'Date,Product,Quantity,Total,Cashier\n';", "headers = 'Date,Product,Quantity,Total,Cashier\\n';")
content = content.replace("headers = 'Date,Product,Quantity,Action,Cashier\n';", "headers = 'Date,Product,Quantity,Action,Cashier\\n';")
content = content.replace("headers = 'Customer,Amount,Date\n';", "headers = 'Customer,Amount,Date\\n';")
content = content.replace("headers = 'Name,Category,Stock,Price,Cost\n';", "headers = 'Name,Category,Stock,Price,Cost\\n';")
content = content.replace("headers = 'Name,Phone,Email\n';", "headers = 'Name,Phone,Email\\n';")

content = content.replace(").join('\n');", ").join('\\n');")

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax errors")
