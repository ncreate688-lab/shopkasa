import re

def fix_all():
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        content = f.read()

    cards = [
        ("Sales History", "sales", "Sales", "props.salesHistory"),
        ("Stock History", "stock", "Stock", "props.stockHistory"),
        ("Products Inventory", "products", "Products", "props.products"),
        ("Customer Directory", "customers", "Customers", "props.customers"),
        ("Active Debts", "debts", "Debts", "props.debts"),
        ("Suppliers Directory", "suppliers", "Suppliers", "props.suppliers"),
        ("M-Pesa Transactions", "mpesa", "M-Pesa", "[]") # For M-Pesa, we just use a generic array since we don't have props.mpesa
    ]
    
    for title, type_val, sync_name, prop_name in cards:
        title_idx = content.find(f'<h3 className="font-bold text-slate-800 text-base">{title}</h3>')
        if title_idx == -1:
            print(f"Could not find {title}")
            continue
            
        mt_auto_idx = content.find('<div className="flex flex-col gap-3 mt-auto">', title_idx)
        if mt_auto_idx == -1:
            continue
            
        button_html = f"""                    <div className="grid grid-cols-2 gap-3">
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
            button_html += f"""\n                      <button onClick={{() => toast.success('Google Sheet sync happens automatically on CSV export for >100 records')}} className="flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-600">
                         <Globe className="w-4 h-4" /> Live Sync
                      </button>
                    </div>"""
        else:
            button_html += f"""\n                      <button onClick={{async () => {{
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
            button_html += f"""\n                    <button onClick={{() => triggerImport('{type_val}')}} className="w-full flex justify-center items-center gap-2 py-2 px-3 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-xs font-semibold text-blue-500">
                      <Upload className="w-4 h-4" /> Import CSV
                    </button>"""
                    
        start = mt_auto_idx + len('<div className="flex flex-col gap-3 mt-auto">\n')
        
        # We need to find the exact end of the flex-col block.
        # It's better to use regex to find `</div>` that closes `flex-col`.
        # However, it's easier to find the end of the whole card `</div>\n                </div>` and replace from `start` to `end`.
        
        # We find `</div>\n                </div>` after start.
        end_idx = content.find('                </div>\n', start)
        if end_idx != -1:
            end_match = re.search(r'\s*</div>\n\s*</div>\n', content[start:])
            if end_match:
                end_pos = start + end_match.start()
                content = content[:start] + button_html + "\n                  " + content[end_pos:]

    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(content)
        
fix_all()
