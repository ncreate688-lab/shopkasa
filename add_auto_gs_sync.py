import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add isAutoSyncing state and trigger function to Dashboard
js_logic = """
      const [isAutoSyncing, setIsAutoSyncing] = useState(false);
      const triggerGoogleSheetSync = async (type, data) => {
        if (!settings.googleSheetWebhookUrl) return;
        setIsAutoSyncing(true);
        try {
          await fetch(settings.googleSheetWebhookUrl, {
            method: 'POST',
            body: JSON.stringify({ sheetName: type, data: data || [] })
          });
        } catch (e) { console.error('Auto sync error', e); }
        finally { setIsAutoSyncing(false); }
      };
"""

content = content.replace(
    'const [receiptData, setReceiptData] = useState(null);',
    'const [receiptData, setReceiptData] = useState(null);\n' + js_logic
)

# Append triggerGoogleSheetSync inside the update methods on line 4670
content = content.replace(
    '''tursoSync('products', v); return v; }); };''',
    '''tursoSync('products', v); triggerGoogleSheetSync('Products', v); return v; }); };'''
)
content = content.replace(
    '''tursoSync('customers', v); return v; }); };''',
    '''tursoSync('customers', v); triggerGoogleSheetSync('Customers', v); return v; }); };'''
)
content = content.replace(
    '''tursoSync('debts', v); return v; }); };''',
    '''tursoSync('debts', v); triggerGoogleSheetSync('Debts', v); return v; }); };'''
)
content = content.replace(
    '''tursoSync('paidDebts', v); return v; }); };''',
    '''tursoSync('paidDebts', v); triggerGoogleSheetSync('Paid Debts', v); return v; }); };'''
)
content = content.replace(
    '''tursoSync('expenses', v); return v; }); };''',
    '''tursoSync('expenses', v); triggerGoogleSheetSync('Expenses', v); return v; }); };'''
)
content = content.replace(
    '''tursoSync('salesHistory', v); const snaps''',
    '''tursoSync('salesHistory', v); triggerGoogleSheetSync('Sales History', v); const snaps'''
)
content = content.replace(
    '''tursoSync('stockHistory', v); return v; }); };''',
    '''tursoSync('stockHistory', v); triggerGoogleSheetSync('Stock History', v); return v; }); };'''
)

# Add the UI popup for Auto Sync in Dashboard
ui_popup = """
        {isAutoSyncing && (
          <div className="fixed top-4 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg text-sm flex items-center gap-2 z-[9999] font-medium animate-pulse">
            <svg className="w-4 h-4 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            Syncing to Google Sheets...
          </div>
        )}
"""

content = content.replace(
    '''<div className="md:pl-64 flex flex-col flex-1 min-h-screen">''',
    '''<div className="md:pl-64 flex flex-col flex-1 min-h-screen">''' + ui_popup
)

# Add "Pull Data" to SettingsPanel
pull_logic = """
          <button 
            onClick={async () => {
              if (!settings.googleSheetWebhookUrl) return toast.error("Please enter a webhook URL");
              const toastId = toast.loading('Pulling data from Google Sheets...');
              try {
                const res = await fetch(settings.googleSheetWebhookUrl);
                const json = await res.json();
                if (json.ok && json.data) {
                  if (json.data['Products'] && updateProducts) updateProducts(json.data['Products']);
                  if (json.data['Sales History'] && updateSalesHistory) updateSalesHistory(json.data['Sales History']);
                  if (json.data['Expenses'] && updateExpenses) updateExpenses(json.data['Expenses']);
                  if (json.data['Debts'] && updateDebts) updateDebts(json.data['Debts']);
                  if (json.data['Paid Debts'] && updatePaidDebts) updatePaidDebts(json.data['Paid Debts']);
                  if (json.data['Stock History'] && updateStockHistory) updateStockHistory(json.data['Stock History']);
                  toast.success('Data pulled successfully!', { id: toastId });
                } else {
                  toast.error('Failed to pull data.', { id: toastId });
                }
              } catch (e) {
                toast.error('Error pulling data.', { id: toastId });
              }
            }}
            className="w-full py-3 mt-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors bg-white border border-indigo-600 text-indigo-700 hover:bg-indigo-50"
          >
            ↓ Pull Data from Google Sheets
          </button>
"""

content = content.replace(
    '''{syncingGoogleSheets ? 'Syncing...' : '✓ Force Sync All Data to Google Sheets'}\n          </button>''',
    '''{syncingGoogleSheets ? 'Syncing...' : '✓ Force Sync All Data to Google Sheets'}\n          </button>\n''' + pull_logic
)


with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
