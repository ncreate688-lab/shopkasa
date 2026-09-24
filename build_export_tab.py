def fix_export_tab():
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        content = f.read()

    start_str = "            {activeTab === 'export' && ("
    end_str = "            )}\n          </div>\n        \n          {exportModalState.isOpen && ("
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find bounds")
        return
        
    export_tab_str = """            {activeTab === 'export' && (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 pb-12">
"""
    cards = [
        ("Sales History", "sales", "Sales", "props.salesHistory", "Export all processed sales transactions.", "TrendingUp"),
        ("Stock History", "stock", "Stock", "props.stockHistory", "Export inventory changes and adjustments.", "ClipboardList"),
        ("Products Inventory", "products", "Products", "props.products", "Export current product catalog and stock levels.", "Package"),
        ("Customer Directory", "customers", "Customers", "props.customers", "Export customer details and contact info.", "Users"),
        ("Active Debts", "debts", "Debts", "props.debts", "Export outstanding customer balances.", "CreditCard"),
        ("Suppliers Directory", "suppliers", "Suppliers", "props.suppliers", "Export supplier contact info and details.", "Truck"),
        ("M-Pesa Transactions", "mpesa", "M-Pesa", "[]", "Export recorded mobile money payments.", "CreditCard")
    ]
    
    for i, (title, type_val, sync_name, prop_name, desc, icon) in enumerate(cards):
        export_tab_str += f"""                {{/* {i+1}. {title} */}}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col p-5">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 bg-emerald-50">
                      <{icon} className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-base">{title}</h3>
                      <p className="text-sm text-slate-500 mt-0.5">{desc}</p>
                      <p className="text-xs text-slate-400 mt-1">{{{prop_name}?.length || 0}} Records</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-3 mt-auto">
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={{() => setExportModalState({{ isOpen: true, type: '{type_val}', format: 'csv' }})}} className="flex justify-center items-center gap-2 py-2 px-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-xs font-semibold text-slate-600">
                         <Download className="w-4 h-4" /> CSV
                      </button>
                      <button onClick={{() => setExportModalState({{ isOpen: true, type: '{type_val}', format: 'excel' }})}} className="flex justify-center items-center gap-2 py-2 px-3 border border-amber-200 rounded-lg hover:bg-amber-50 transition-colors text-xs font-semibold text-amber-600">
                         <FileText className="w-4 h-4" /> Excel
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={{() => setExportModalState({{ isOpen: true, type: '{type_val}', format: 'pdf' }})}} className="flex justify-center items-center gap-2 py-2 px-3 border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors text-xs font-semibold text-emerald-600">
                         <FileText className="w-4 h-4" /> PDF
                      </button>"""

        if type_val == 'mpesa':
            export_tab_str += f"""\n                      <button onClick={{() => toast.success('Google Sheet sync happens automatically on CSV export for >100 records')}} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>"""
        else:
            export_tab_str += f"""\n                      <button onClick={{async () => {{
                        if (!props.settings?.googleSheetWebhookUrl) return toast.error('Add Webhook URL in Settings');
                        const tid = toast.loading('Syncing {sync_name}...');
                        try {{
                          await fetch(props.settings.googleSheetWebhookUrl, {{ method: 'POST', body: JSON.stringify({{ sheetName: '{sync_name}', data: {prop_name} || [] }}) }});
                          toast.success('Synced successfully!', {{ id: tid }});
                        }} catch(e) {{ toast.error('Sync failed', {{ id: tid }}); }}
                      }}}} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>"""

        if type_val in ['stock', 'products', 'customers', 'debts', 'suppliers']:
            export_tab_str += f"""\n                    <button onClick={{() => triggerImport('{type_val}')}} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>"""

        export_tab_str += """
                  </div>
                </div>\n"""

    export_tab_str += "              </div>\n"
    
    content = content[:start_idx] + export_tab_str + content[end_idx:]
    
    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(content)

fix_export_tab()
