import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate BusinessAnalyticsWrapper
import_logic = """
    const BusinessAnalyticsWrapper = (props) => {
      const [activeTab, setActiveTab] = useState('overview');
      const fileInputRef = useRef(null);
      const [importTarget, setImportTarget] = useState(null);

      const triggerImport = (targetType) => {
        setImportTarget(targetType);
        if (fileInputRef.current) fileInputRef.current.click();
      };

      const onFileImport = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (evt) => {
          const text = evt.target.result;
          if (!text) return toast.error('Empty file');
          const lines = text.split('\\n').filter(l => l.trim());
          if (lines.length < 2) return toast.error('No valid data rows found');
          
          let parsedData = [];
          try {
            const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
            for (let i = 1; i < lines.length; i++) {
              const rowStr = lines[i].trim();
              if(!rowStr) continue;
              let row = [];
              let inQuotes = false;
              let current = '';
              for(let char of rowStr) {
                if(char === '"') inQuotes = !inQuotes;
                else if(char === ',' && !inQuotes) { row.push(current); current = ''; }
                else current += char;
              }
              row.push(current);
              
              let obj = {};
              headers.forEach((h, idx) => { obj[h] = row[idx] ? row[idx].replace(/^"|"$/g, '') : ''; });
              parsedData.push(obj);
            }
          } catch(err) {
            return toast.error('Failed to parse CSV');
          }

          if (importTarget === 'sales') {
            const newSales = parsedData.map(d => ({
              id: Date.now() + Math.random().toString(),
              date: d.Date || new Date().toISOString(),
              name: d.Product || 'Imported Sale',
              quantity: Number(d.Quantity) || 1,
              finalPrice: Number(d.Total) || 0,
              cashierName: d.Cashier || 'System'
            }));
            if(props.setSalesHistory) props.setSalesHistory([...(props.salesHistory||[]), ...newSales]);
            toast.success(`Imported ${newSales.length} sales`);
          }
          else if (importTarget === 'stock') {
            const newStock = parsedData.map(d => ({
              id: Date.now() + Math.random().toString(),
              date: d.Date || new Date().toISOString(),
              name: d.Product || 'Imported Item',
              qty: Number(d.Quantity) || 0,
              action: d.Action || 'add',
              cashierName: d.Cashier || 'System'
            }));
            if(props.setStockHistory) props.setStockHistory([...(props.stockHistory||[]), ...newStock]);
            toast.success(`Imported ${newStock.length} stock entries`);
          }
          else if (importTarget === 'products') {
            const newProducts = parsedData.map(d => ({
              id: Date.now() + Math.random().toString(),
              name: d.Name || 'Imported Product',
              category: d.Category || 'General',
              stock: Number(d.Stock) || 0,
              price: Number(d.Price) || 0,
              cost: Number(d.Cost) || 0
            }));
            if(props.setProducts) props.setProducts([...(props.products||[]), ...newProducts]);
            toast.success(`Imported ${newProducts.length} products`);
          }
          else if (importTarget === 'customers') {
            const newCustomers = parsedData.map(d => ({
              id: Date.now() + Math.random().toString(),
              name: d.Name || 'Imported Customer',
              phone: d.Phone || '',
              email: d.Email || ''
            }));
            if(props.setCustomers) props.setCustomers([...(props.customers||[]), ...newCustomers]);
            toast.success(`Imported ${newCustomers.length} customers`);
          }
          else if (importTarget === 'debts') {
            const newDebts = parsedData.map(d => ({
              id: Date.now() + Math.random().toString(),
              customerName: d.Customer || 'Unknown',
              amount: Number(d.Amount) || 0,
              date: d.Date || new Date().toISOString(),
              status: 'pending'
            }));
            if(props.setDebts) props.setDebts([...(props.debts||[]), ...newDebts]);
            toast.success(`Imported ${newDebts.length} debts`);
          }
          else if (importTarget === 'suppliers') {
            const newSuppliers = parsedData.map(d => ({
              id: Date.now() + Math.random().toString(),
              name: d.Name || 'Unknown',
              phone: d.Phone || '',
              email: d.Email || ''
            }));
            if(props.setSettings && props.settings) {
               props.setSettings({...props.settings, suppliers: [...(props.settings.suppliers||[]), ...newSuppliers]});
            }
            toast.success(`Imported ${newSuppliers.length} suppliers`);
          }

          e.target.value = null; 
        };
        reader.readAsText(file);
      };

      return (
        <div className="space-y-6 pb-20">
          <input type="file" accept=".csv" ref={fileInputRef} onChange={onFileImport} style={{display: 'none'}} />
"""

content = content.replace(
    """    const BusinessAnalyticsWrapper = (props) => {
      const [activeTab, setActiveTab] = useState('overview');

      return (
        <div className="space-y-6 pb-20">""",
    import_logic
)

# Replace all Import CSV buttons to trigger the import logic
content = content.replace(
    """<button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""",
    """<button onClick={() => triggerImport('sales')} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""", 1
)

content = content.replace(
    """<button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""",
    """<button onClick={() => triggerImport('stock')} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""", 1
)

content = content.replace(
    """<button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""",
    """<button onClick={() => triggerImport('products')} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""", 1
)

content = content.replace(
    """<button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""",
    """<button onClick={() => triggerImport('customers')} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""", 1
)

content = content.replace(
    """<button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""",
    """<button onClick={() => triggerImport('debts')} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""", 1
)

content = content.replace(
    """<button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""",
    """<button onClick={() => triggerImport('suppliers')} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>""", 1
)


with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added import functionality!")
