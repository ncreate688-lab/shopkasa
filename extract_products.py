import subprocess
import sys
import csv

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import pypdf
except ImportError:
    install('pypdf')
    import pypdf

reader = pypdf.PdfReader("SoftlyBuilt_Report_2026-10-05_261005_185033.pdf")
lines = []
for page in reader.pages:
    text = page.extract_text()
    if text:
        lines.extend(text.split('\n'))

with open("SoftlyBuilt_Products.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Barcode", "Name", "Price", "Category", "Cost", "Stock", "Expiry Date"])
    
    in_products = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if "Barcode" in line and "Name" in line and "Price" in line:
            in_products = True
            continue
            
        if "Date" in line and "Product" in line and "Qty" in line and "Total" in line:
            # We reached the sales section
            in_products = False
            break
            
        if in_products:
            parts = line.split()
            if len(parts) < 6:
                continue
            
            expiry = parts[-1]
            stock = parts[-2]
            cost = parts[-3]
            
            price_idx = -1
            for i in range(len(parts)-4, 0, -1):
                try:
                    float(parts[i].replace(',', ''))
                    price_idx = i
                    break
                except ValueError:
                    continue
            
            if price_idx == -1:
                continue
                
            price = parts[price_idx]
            category = " ".join(parts[price_idx+1:-3])
            barcode = parts[0]
            name = " ".join(parts[1:price_idx])
            
            writer.writerow([barcode, name, price, category, cost, stock, expiry])
            
print("Extraction complete. Data saved to SoftlyBuilt_Products.csv")
