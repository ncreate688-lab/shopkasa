import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure Globe and other icons are imported (if not already)
# They were already imported in the previous step.

export_ui = """
            {activeTab === 'export' && (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 pb-12">
                
                {/* 1. Sales History */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <DollarSign className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Sales History</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export all recorded sales transactions.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.salesHistory?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => {
                        if (!props.salesHistory?.length) return toast.error('No data');
                        const headers = 'Date,Product,Quantity,Total,Cashier\\n';
                        const rows = props.salesHistory.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.quantity},${s.finalPrice},"${s.cashierName}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'sales_history.csv'; a.click();
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel export uses CSV logic for now.')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={async () => {
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings > Data Management');
                        const tid = toast.loading('Syncing Sales...');
                        try {
                          await fetch(props.settings.googleSheetWebhookUrl, { method: 'POST', body: JSON.stringify({ sheetName: 'Sales History', data: props.salesHistory || [] }) });
                          toast.success('Synced successfully!', { id: tid });
                        } catch(e) { toast.error('Sync failed', { id: tid }); }
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 2. Stock History */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <ClipboardList className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Stock History</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export inventory changes and adjustments.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.stockHistory?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => {
                        if (!props.stockHistory?.length) return toast.error('No data');
                        const headers = 'Date,Product,Quantity,Action,Cashier\\n';
                        const rows = props.stockHistory.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.qty},"${s.action}","${s.cashierName}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'stock_history.csv'; a.click();
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel export uses CSV logic for now.')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('PDF generation coming soon')} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={async () => {
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings');
                        const tid = toast.loading('Syncing Stock...');
                        try {
                          await fetch(props.settings.googleSheetWebhookUrl, { method: 'POST', body: JSON.stringify({ sheetName: 'Stock History', data: props.stockHistory || [] }) });
                          toast.success('Synced successfully!', { id: tid });
                        } catch(e) { toast.error('Sync failed', { id: tid }); }
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 3. Products Inventory */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <Package className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Products Inventory</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export current product catalog and stock levels.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.products?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => {
                        if (!props.products?.length) return toast.error('No data');
                        const headers = 'Name,Category,Stock,Price,Cost\\n';
                        const rows = props.products.map(p => `"${p.name}","${p.category}",${p.stock},${p.price},${p.cost}`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'products.csv'; a.click();
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel export uses CSV logic for now.')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('PDF generation coming soon')} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={async () => {
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings');
                        const tid = toast.loading('Syncing Products...');
                        try {
                          await fetch(props.settings.googleSheetWebhookUrl, { method: 'POST', body: JSON.stringify({ sheetName: 'Products', data: props.products || [] }) });
                          toast.success('Synced successfully!', { id: tid });
                        } catch(e) { toast.error('Sync failed', { id: tid }); }
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 4. Customer Directory */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <Users className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Customer Directory</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export customer details and contact info.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.customers?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => {
                        if (!props.customers?.length) return toast.error('No data');
                        const headers = 'Name,Phone,Email\\n';
                        const rows = props.customers.map(c => `"${c.name}","${c.phone}","${c.email}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'customers.csv'; a.click();
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel export uses CSV logic for now.')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('PDF generation coming soon')} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={async () => {
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings');
                        const tid = toast.loading('Syncing Customers...');
                        try {
                          await fetch(props.settings.googleSheetWebhookUrl, { method: 'POST', body: JSON.stringify({ sheetName: 'Customers', data: props.customers || [] }) });
                          toast.success('Synced successfully!', { id: tid });
                        } catch(e) { toast.error('Sync failed', { id: tid }); }
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 5. Active Debts */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <AlertCircle className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Active Debts</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export pending and active customer debts.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.debts?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => {
                        if (!props.debts?.length) return toast.error('No data');
                        const headers = 'Customer,Amount,Date\\n';
                        const rows = props.debts.map(d => `"${d.customerName}",${d.amount},${new Date(d.date).toLocaleDateString()}`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'debts.csv'; a.click();
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel export uses CSV logic for now.')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('PDF generation coming soon')} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={async () => {
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings');
                        const tid = toast.loading('Syncing Debts...');
                        try {
                          await fetch(props.settings.googleSheetWebhookUrl, { method: 'POST', body: JSON.stringify({ sheetName: 'Debts', data: props.debts || [] }) });
                          toast.success('Synced successfully!', { id: tid });
                        } catch(e) { toast.error('Sync failed', { id: tid }); }
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 6. Suppliers Directory */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <Truck className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Suppliers Directory</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export supplier details and contact info.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.suppliers?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => {
                        if (!props.suppliers?.length) return toast.error('No data');
                        const headers = 'Name,Phone,Email\\n';
                        const rows = props.suppliers.map(s => `"${s.name}","${s.phone}","${s.email}"`).join('\\n');
                        const blob = new Blob([headers + rows], { type: 'text/csv' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a'); a.href = url; a.download = 'suppliers.csv'; a.click();
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel export uses CSV logic for now.')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('PDF generation coming soon')} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={async () => {
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings');
                        const tid = toast.loading('Syncing Suppliers...');
                        try {
                          await fetch(props.settings.googleSheetWebhookUrl, { method: 'POST', body: JSON.stringify({ sheetName: 'Suppliers', data: props.suppliers || [] }) });
                          toast.success('Synced successfully!', { id: tid });
                        } catch(e) { toast.error('Sync failed', { id: tid }); }
                      }} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

              </div>
            )}
"""

# Replace the previous export block
content = re.sub(
    r"\{activeTab === 'export' && \([\s\S]*?\}\)\n          <\/div>\n        <\/div>",
    export_ui + "\n          </div>\n        </div>",
    content
)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
