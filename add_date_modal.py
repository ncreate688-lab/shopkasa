import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the activeTab === 'export' block and the BusinessAnalyticsWrapper state definitions
state_logic = """
    const BusinessAnalyticsWrapper = (props) => {
      const [activeTab, setActiveTab] = useState('overview');
      const fileInputRef = useRef(null);
      const [importTarget, setImportTarget] = useState(null);
      
      const [exportModalState, setExportModalState] = useState({ isOpen: false, type: null, format: null });
      const [exportStartDate, setExportStartDate] = useState('');
      const [exportEndDate, setExportEndDate] = useState('');

      const handleExportConfirm = () => {
         let headers = '';
         let rows = '';
         let filename = '';

         const filterByDate = (arr, dateField = 'date') => {
            if (!exportStartDate && !exportEndDate) return arr;
            return arr.filter(item => {
               if (!item[dateField]) return true;
               const d = new Date(item[dateField]);
               if (exportStartDate && d < new Date(exportStartDate)) return false;
               if (exportEndDate && d > new Date(exportEndDate + 'T23:59:59.999Z')) return false;
               return true;
            });
         };

         if (exportModalState.type === 'sales') {
            const data = filterByDate(props.salesHistory || []);
            if (!data.length) { toast.error('No data for selected range'); return; }
            headers = 'Date,Product,Quantity,Total,Cashier\\n';
            rows = data.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.quantity},${s.finalPrice},"${s.cashierName}"`).join('\\n');
            filename = 'sales_history.csv';
         }
         else if (exportModalState.type === 'stock') {
            const data = filterByDate(props.stockHistory || []);
            if (!data.length) { toast.error('No data for selected range'); return; }
            headers = 'Date,Product,Quantity,Action,Cashier\\n';
            rows = data.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.qty},"${s.action}","${s.cashierName}"`).join('\\n');
            filename = 'stock_history.csv';
         }
         else if (exportModalState.type === 'debts') {
            const data = filterByDate(props.debts || []);
            if (!data.length) { toast.error('No data for selected range'); return; }
            headers = 'Customer,Amount,Date\\n';
            rows = data.map(d => `"${d.customerName}",${d.amount},${new Date(d.date).toLocaleDateString()}`).join('\\n');
            filename = 'debts.csv';
         }
         else if (exportModalState.type === 'products') {
            const data = props.products || []; 
            if (!data.length) { toast.error('No data'); return; }
            headers = 'Name,Category,Stock,Price,Cost\\n';
            rows = data.map(p => `"${p.name}","${p.category}",${p.stock},${p.price},${p.cost}`).join('\\n');
            filename = 'products.csv';
         }
         else if (exportModalState.type === 'customers') {
            const data = props.customers || []; 
            if (!data.length) { toast.error('No data'); return; }
            headers = 'Name,Phone,Email\\n';
            rows = data.map(c => `"${c.name}","${c.phone}","${c.email}"`).join('\\n');
            filename = 'customers.csv';
         }
         else if (exportModalState.type === 'suppliers') {
            const data = props.suppliers || []; 
            if (!data.length) { toast.error('No data'); return; }
            headers = 'Name,Phone,Email\\n';
            rows = data.map(s => `"${s.name}","${s.phone}","${s.email}"`).join('\\n');
            filename = 'suppliers.csv';
         }

         const blob = new Blob([headers + rows], { type: 'text/csv' });
         const url = URL.createObjectURL(blob);
         const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
         URL.revokeObjectURL(url);
         setExportModalState({ isOpen: false, type: null, format: null });
      };
"""

content = re.sub(r'const BusinessAnalyticsWrapper = \(props\) => \{[\s\S]*?const \[importTarget, setImportTarget\] = useState\(null\);', state_logic, content)

# Now, we inject the modal itself at the bottom of the wrapper before the closing div
modal_ui = """
          {exportModalState.isOpen && (
            <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 animate-in zoom-in-95">
                <h3 className="text-xl font-bold text-slate-800">Select Date Range</h3>
                <p className="text-sm text-slate-500 mt-2 mb-6">Optional: Filter by date before exporting.</p>
                
                <div className="grid grid-cols-2 gap-4 mb-8">
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 mb-1.5">Start Date</label>
                    <div className="relative">
                      <input type="date" value={exportStartDate} onChange={e => setExportStartDate(e.target.value)} className="w-full pl-3 pr-10 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all text-slate-700" />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 mb-1.5">End Date</label>
                    <div className="relative">
                      <input type="date" value={exportEndDate} onChange={e => setExportEndDate(e.target.value)} className="w-full pl-3 pr-10 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all text-slate-700" />
                    </div>
                  </div>
                </div>
                
                <div className="flex justify-end gap-3">
                  <button onClick={() => setExportModalState({ isOpen: false, type: null, format: null })} className="px-5 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-xl transition-colors">Cancel</button>
                  <button onClick={handleExportConfirm} className="px-6 py-2.5 text-sm font-bold bg-[#10b981] hover:bg-[#059669] text-white rounded-xl transition-all shadow-sm">Download</button>
                </div>
              </div>
            </div>
          )}
        </div>
      );
    };"""

content = re.sub(r'<\/div>\n      \);\n    \};\n\n    const Dashboard =', modal_ui + '\n\n    const Dashboard =', content)

# Now replace the onClick handlers for CSV buttons.
content = content.replace(
    """onClick={() => {
                        if (!props.salesHistory?.length) return toast.error('No data');
                        const headers = 'Date,Product,Quantity,Total,Cashier\\n';
                        const rows = props.salesHistory.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.quantity},${s.finalPrice},"${s.cashierName}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'sales_history.csv'; a.click();
                      }}""",
    """onClick={() => setExportModalState({ isOpen: true, type: 'sales', format: 'csv' })}"""
)

content = content.replace(
    """onClick={() => {
                        if (!props.stockHistory?.length) return toast.error('No data');
                        const headers = 'Date,Product,Quantity,Action,Cashier\\n';
                        const rows = props.stockHistory.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.qty},"${s.action}","${s.cashierName}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'stock_history.csv'; a.click();
                      }}""",
    """onClick={() => setExportModalState({ isOpen: true, type: 'stock', format: 'csv' })}"""
)

content = content.replace(
    """onClick={() => {
                        if (!props.products?.length) return toast.error('No data');
                        const headers = 'Name,Category,Stock,Price,Cost\\n';
                        const rows = props.products.map(p => `"${p.name}","${p.category}",${p.stock},${p.price},${p.cost}`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'products.csv'; a.click();
                      }}""",
    """onClick={() => setExportModalState({ isOpen: true, type: 'products', format: 'csv' })}"""
)

content = content.replace(
    """onClick={() => {
                        if (!props.customers?.length) return toast.error('No data');
                        const headers = 'Name,Phone,Email\\n';
                        const rows = props.customers.map(c => `"${c.name}","${c.phone}","${c.email}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'customers.csv'; a.click();
                      }}""",
    """onClick={() => setExportModalState({ isOpen: true, type: 'customers', format: 'csv' })}"""
)

content = content.replace(
    """onClick={() => {
                        if (!props.debts?.length) return toast.error('No data');
                        const headers = 'Customer,Amount,Date\\n';
                        const rows = props.debts.map(d => `"${d.customerName}",${d.amount},${new Date(d.date).toLocaleDateString()}`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'debts.csv'; a.click();
                      }}""",
    """onClick={() => setExportModalState({ isOpen: true, type: 'debts', format: 'csv' })}"""
)

content = content.replace(
    """onClick={() => {
                        if (!props.suppliers?.length) return toast.error('No data');
                        const headers = 'Name,Phone,Email\\n';
                        const rows = props.suppliers.map(s => `"${s.name}","${s.phone}","${s.email}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'suppliers.csv'; a.click();
                      }}""",
    """onClick={() => setExportModalState({ isOpen: true, type: 'suppliers', format: 'csv' })}"""
)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Date modal added!")
