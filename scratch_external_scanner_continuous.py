import sys
import os

file_path = r"c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make it continuous for external scanner
old_handleScan_sell = "if (scannerMode === 'sell') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } addToCart(p); setScannerMode(null); return; }"
new_handleScan_sell = "if (scannerMode === 'sell') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } addToCart(p); if (!useExternalScanner) setScannerMode(null); return; }"
content = content.replace(old_handleScan_sell, new_handleScan_sell)

old_handleScan_stock = "if (scannerMode === 'stock') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } setScannerMode(null); const q = prompt(`Add Stock for \"${p.name}\":`, '1'); if (q !== null) { const n = parseFloat(q); if (!isNaN(n) && n > 0) addStock(p, n); else toast.error('Invalid quantity'); } return; }"
new_handleScan_stock = "if (scannerMode === 'stock') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } if (!useExternalScanner) setScannerMode(null); const q = prompt(`Add Stock for \"${p.name}\":`, '1'); if (q !== null) { const n = parseFloat(q); if (!isNaN(n) && n > 0) addStock(p, n); else toast.error('Invalid quantity'); } return; }"
content = content.replace(old_handleScan_stock, new_handleScan_stock)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
