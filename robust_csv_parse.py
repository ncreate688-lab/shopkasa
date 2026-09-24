with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

def make_robust_float(field, default):
    return f"parseFloat((d.{field} || '{default}').toString().replace(/[^0-9.-]+/g, '')) || {default}"

content = content.replace("quantity: Number(d.Quantity) || 1,", f"quantity: {make_robust_float('Quantity', 1)},")
content = content.replace("finalPrice: Number(d.Total) || 0,", f"finalPrice: {make_robust_float('Total', 0)},")
content = content.replace("qty: Number(d.Quantity) || 0,", f"qty: {make_robust_float('Quantity', 0)},")
content = content.replace("stock: Number(d.Stock) || 0,", f"stock: {make_robust_float('Stock', 0)},")
content = content.replace("price: Number(d.Price) || 0,", f"price: {make_robust_float('Price', 0)},")
content = content.replace("cost: Number(d.Cost) || 0,", f"cost: {make_robust_float('Cost', 0)},")
content = content.replace("amount: Number(d.Amount) || 0,", f"amount: {make_robust_float('Amount', 0)},")

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Robust parsing applied!')
