import sys
import os

file_path = r"c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Edit 1: Remove local state useExternalScanner
if "const [useExternalScanner, setUseExternalScanner] = useState(false);" in content:
    content = content.replace(" const [useExternalScanner, setUseExternalScanner] = useState(false);", "")
    content = content.replace("const [useExternalScanner, setUseExternalScanner] = useState(false); ", "")
    content = content.replace("const [useExternalScanner, setUseExternalScanner] = useState(false);", "")

# Edit 2: Restore original scan buttons
old_buttons = "{settings.showScan && (<div className=\"flex flex-wrap items-center gap-2\"><label className=\"flex items-center gap-2 bg-slate-100 px-3 py-2 rounded-lg cursor-pointer hover:bg-slate-200 transition-colors border border-slate-200\"><input type=\"checkbox\" checked={useExternalScanner} onChange={e => setUseExternalScanner(e.target.checked)} className=\"w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500\" /><span className=\"text-sm font-semibold text-slate-700\">Ext. Scanner</span></label><button onClick={() => setScannerMode('stock')} className=\"btn-primary px-4 py-2\"><PackagePlus className=\"w-4 h-4\" /> Scan to Stock</button>{settings.showScanToSell && <button onClick={() => setScannerMode('sell')} className=\"btn-primary px-4 py-2\"><Scan className=\"w-4 h-4\" /> Scan to Sell</button>}</div>)}"
new_buttons = "{settings.showScan && (<><button onClick={() => setScannerMode('stock')} className=\"btn-primary px-4 py-2\"><PackagePlus className=\"w-4 h-4\" /> Scan to Stock</button>{settings.showScanToSell && <button onClick={() => setScannerMode('sell')} className=\"btn-primary px-4 py-2\"><Scan className=\"w-4 h-4\" /> Scan to Sell</button>}</>)}"
if old_buttons in content:
    content = content.replace(old_buttons, new_buttons)

# Edit 3: Update Modal code to use settings.desktopMode
old_modal = "{scannerMode && (useExternalScanner ? <ExternalScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} /> : <ScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} scannerSize={superAdminSettings?.scannerSize} />)}"
new_modal = "{scannerMode && (settings.desktopMode ? <ExternalScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} /> : <ScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} scannerSize={superAdminSettings?.scannerSize} />)}"
if old_modal in content:
    content = content.replace(old_modal, new_modal)

# Edit 4: Update handleScan to use settings.desktopMode
old_sell = "if (scannerMode === 'sell') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } addToCart(p); if (!useExternalScanner) setScannerMode(null); return; }"
new_sell = "if (scannerMode === 'sell') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } addToCart(p); if (!settings.desktopMode) setScannerMode(null); return; }"
content = content.replace(old_sell, new_sell)

old_stock = "if (scannerMode === 'stock') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } if (!useExternalScanner) setScannerMode(null); const q = prompt(`Add Stock for \"${p.name}\":`, '1'); if (q !== null) { const n = parseFloat(q); if (!isNaN(n) && n > 0) addStock(p, n); else toast.error('Invalid quantity'); } return; }"
new_stock = "if (scannerMode === 'stock') { if (!p) { toast.error('Product not found', { duration: 1500 }); return; } if (!settings.desktopMode) setScannerMode(null); const q = prompt(`Add Stock for \"${p.name}\":`, '1'); if (q !== null) { const n = parseFloat(q); if (!isNaN(n) && n > 0) addStock(p, n); else toast.error('Invalid quantity'); } return; }"
content = content.replace(old_stock, new_stock)

# Edit 5: Add desktopMode to DEFAULT_SETTINGS
old_default = "showScanToSell: true,\n      trackExpiry: true,"
new_default = "showScanToSell: true,\n      desktopMode: false,\n      trackExpiry: true,"
if old_default in content and "desktopMode: false," not in content:
    content = content.replace(old_default, new_default)

# Edit 6: Add the UI toggle in Settings (if not already there)
old_ui = "<div className=\"flex justify-between items-center\"><span className=\"text-slate-700 font-medium\">Track Expiry Dates</span><button"
new_ui = "<div className=\"flex justify-between items-center\"><span className=\"text-slate-700 font-medium\">Desktop Mode (Physical Scanner)</span><button onClick={() => { update('desktopMode', !settings.desktopMode) }} className={`w-12 h-6 rounded-full relative transition-colors ${settings.desktopMode ? 'bg-emerald-500' : 'bg-slate-200'}`}><div className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-all ${settings.desktopMode ? 'left-7' : 'left-1'}`}></div></button></div><div className=\"flex justify-between items-center\"><span className=\"text-slate-700 font-medium\">Track Expiry Dates</span><button"
if old_ui in content and "Desktop Mode (Physical Scanner)" not in content:
    content = content.replace(old_ui, new_ui)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
