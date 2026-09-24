import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Globe icon to imports
content = content.replace(
    'Truck, Bell, Send, Play, Calendar, Menu, RefreshCw',
    'Truck, Bell, Send, Play, Calendar, Menu, RefreshCw, Globe'
)

# 2. Extract and replace the entire Data Export block
new_export_ui = """
            {activeTab === 'export' && (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 pb-12">
                
                {/* 1. Sales History */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                  <div className="p-5 flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <DollarSign className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Sales History</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export all recorded sales transactions.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.salesHistory?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 border-t border-slate-100 flex-1 flex flex-col justify-end gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('CSV Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 bg-white rounded-lg hover:bg-slate-100 transition-colors text-xs font-semibold text-slate-700 shadow-sm">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors text-xs font-semibold text-amber-700 shadow-sm">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors text-xs font-semibold text-emerald-700 shadow-sm">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={() => toast.success('Sync initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50/50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 2. Stock History */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                  <div className="p-5 flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <ClipboardList className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Stock History</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export inventory changes and adjustments.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.stockHistory?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 border-t border-slate-100 flex-1 flex flex-col justify-end gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('CSV Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 bg-white rounded-lg hover:bg-slate-100 transition-colors text-xs font-semibold text-slate-700 shadow-sm">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors text-xs font-semibold text-amber-700 shadow-sm">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors text-xs font-semibold text-emerald-700 shadow-sm">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={() => toast.success('Sync initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50/50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 3. Products Inventory */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                  <div className="p-5 flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <Package className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Products Inventory</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export current product catalog and stock levels.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.products?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 border-t border-slate-100 flex-1 flex flex-col justify-end gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('CSV Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 bg-white rounded-lg hover:bg-slate-100 transition-colors text-xs font-semibold text-slate-700 shadow-sm">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors text-xs font-semibold text-amber-700 shadow-sm">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors text-xs font-semibold text-emerald-700 shadow-sm">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={() => toast.success('Sync initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50/50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 4. Customer Directory */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                  <div className="p-5 flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <Users className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Customer Directory</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export customer details and contact info.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.customers?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 border-t border-slate-100 flex-1 flex flex-col justify-end gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('CSV Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 bg-white rounded-lg hover:bg-slate-100 transition-colors text-xs font-semibold text-slate-700 shadow-sm">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors text-xs font-semibold text-amber-700 shadow-sm">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors text-xs font-semibold text-emerald-700 shadow-sm">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={() => toast.success('Sync initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50/50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 5. Active Debts */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                  <div className="p-5 flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <AlertCircle className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Active Debts</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export pending and active customer debts.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.debts?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 border-t border-slate-100 flex-1 flex flex-col justify-end gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('CSV Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 bg-white rounded-lg hover:bg-slate-100 transition-colors text-xs font-semibold text-slate-700 shadow-sm">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors text-xs font-semibold text-amber-700 shadow-sm">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors text-xs font-semibold text-emerald-700 shadow-sm">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={() => toast.success('Sync initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50/50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

                {/* 6. Suppliers Directory */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                  <div className="p-5 flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <Truck className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">Suppliers Directory</h3>
                      <p className="text-sm text-slate-500 mt-0.5">Export supplier details and contact info.</p>
                      <p className="text-xs text-slate-400 mt-1">{props.suppliers?.length || 0} Records</p>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 border-t border-slate-100 flex-1 flex flex-col justify-end gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => toast.success('CSV Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 bg-white rounded-lg hover:bg-slate-100 transition-colors text-xs font-semibold text-slate-700 shadow-sm">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={() => toast.success('Excel Export initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors text-xs font-semibold text-amber-700 shadow-sm">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={props.handleDownloadPdf} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors text-xs font-semibold text-emerald-700 shadow-sm">
                         <FileText className="w-4 h-4" /> PDF
                      </button>
                      <button onClick={() => toast.success('Sync initiated')} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>
                    <button className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 bg-blue-50/50 rounded-lg hover:bg-blue-100 transition-colors text-xs font-semibold text-blue-700 shadow-sm">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>
                  </div>
                </div>

              </div>
            )}
"""

# Find the block from {activeTab === 'export' && ( ... )} inside BusinessAnalyticsWrapper
# and replace it.
content = re.sub(
    r"\{activeTab === 'export' && \([\s\S]*?\}\)\n          <\/div>\n        <\/div>",
    new_export_ui + "\n          </div>\n        </div>",
    content
)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
