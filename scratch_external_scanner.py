import sys
import os

file_path = r"c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Edit 1
if "const [useExternalScanner" not in content:
    content = content.replace(
        "const [scannerMode, setScannerMode] = useState(null);",
        "const [scannerMode, setScannerMode] = useState(null); const [useExternalScanner, setUseExternalScanner] = useState(false);"
    )

# Edit 2
old_buttons = "{settings.showScan && (<><button onClick={() => setScannerMode('stock')} className=\"btn-primary px-4 py-2\"><PackagePlus className=\"w-4 h-4\" /> Scan to Stock</button>{settings.showScanToSell && <button onClick={() => setScannerMode('sell')} className=\"btn-primary px-4 py-2\"><Scan className=\"w-4 h-4\" /> Scan to Sell</button>}</>)}"
new_buttons = "{settings.showScan && (<div className=\"flex flex-wrap items-center gap-2\"><label className=\"flex items-center gap-2 bg-slate-100 px-3 py-2 rounded-lg cursor-pointer hover:bg-slate-200 transition-colors border border-slate-200\"><input type=\"checkbox\" checked={useExternalScanner} onChange={e => setUseExternalScanner(e.target.checked)} className=\"w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500\" /><span className=\"text-sm font-semibold text-slate-700\">Ext. Scanner</span></label><button onClick={() => setScannerMode('stock')} className=\"btn-primary px-4 py-2\"><PackagePlus className=\"w-4 h-4\" /> Scan to Stock</button>{settings.showScanToSell && <button onClick={() => setScannerMode('sell')} className=\"btn-primary px-4 py-2\"><Scan className=\"w-4 h-4\" /> Scan to Sell</button>}</div>)}"

if old_buttons not in content:
    print("Could not find old_buttons")
else:
    content = content.replace(old_buttons, new_buttons)

# Edit 3
old_modal = "{scannerMode && <ScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} scannerSize={superAdminSettings?.scannerSize} />}"
new_modal = "{scannerMode && (useExternalScanner ? <ExternalScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} /> : <ScannerModal title={scannerMode === 'sell' ? 'Scan to Sell' : scannerMode === 'stock' ? 'Scan to Stock' : 'Scan Barcode'} onScan={handleScan} onClose={() => setScannerMode(null)} scannerSize={superAdminSettings?.scannerSize} />)}"

if old_modal not in content:
    print("Could not find old_modal")
else:
    content = content.replace(old_modal, new_modal)

# Edit 4: Add ExternalScannerModal before ErrorBoundary
ext_modal_code = """
    const ExternalScannerModal = ({ onScan, onClose, title }) => {
      const [val, setVal] = useState('');
      const inputRef = useRef(null);
      useEffect(() => { if (inputRef.current) inputRef.current.focus(); }, []);
      const handleSubmit = (e) => {
        e.preventDefault();
        if (val.trim()) {
          onScan(val.trim());
          setVal('');
        }
      };
      return (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm" onClick={onClose}>
          <div className="bg-white rounded-2xl w-full max-w-sm overflow-hidden relative shadow-2xl p-6" onClick={e => e.stopPropagation()}>
            <button onClick={onClose} className="absolute top-4 right-4 p-2 bg-slate-100 rounded-full hover:bg-slate-200"><X className="w-5 h-5 text-slate-600" /></button>
            <div className="font-bold text-lg text-slate-800 mb-4">{title}</div>
            <form onSubmit={handleSubmit}>
              <input ref={inputRef} type="text" autoFocus value={val} onChange={e => setVal(e.target.value)} onBlur={() => { setTimeout(() => { if(inputRef.current) inputRef.current.focus(); }, 100); }} className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 font-mono text-center" placeholder="Scan barcode now..." />
            </form>
            <p className="text-xs text-slate-500 text-center mt-3">Ready for external barcode scanner. Keep this window open to scan.</p>
          </div>
        </div>
      );
    };

    // --- ERROR BOUNDARY ---
"""

if "const ExternalScannerModal" not in content:
    if "    // --- ERROR BOUNDARY ---" not in content:
        print("Could not find Error Boundary")
    else:
        content = content.replace("    // --- ERROR BOUNDARY ---", ext_modal_code)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
