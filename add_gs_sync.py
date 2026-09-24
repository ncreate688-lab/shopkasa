import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add syncingGoogleSheets state and handleGoogleSheetSync method
js_logic = """
      const [syncingGoogleSheets, setSyncingGoogleSheets] = useState(false);
      const handleGoogleSheetSync = async () => {
        if (!settings.googleSheetWebhookUrl) {
          toast.error('Please enter a Google Sheets Webhook URL first.');
          return;
        }
        
        setSyncingGoogleSheets(true);
        const toastId = toast.loading('Syncing data to Google Sheets...');
        
        try {
          const allData = [
            { sheetName: 'Products', data: products || [] },
            { sheetName: 'Sales History', data: salesHistory || [] },
            { sheetName: 'Expenses', data: expenses || [] },
            { sheetName: 'Debts', data: debts || [] },
            { sheetName: 'Paid Debts', data: paidDebts || [] },
            { sheetName: 'Stock History', data: stockHistory || [] }
          ];

          for (const sheetData of allData) {
            if (sheetData.data.length > 0) {
              await fetch(settings.googleSheetWebhookUrl, {
                method: 'POST',
                body: JSON.stringify(sheetData)
              });
            }
          }
          toast.success('Sync complete!', { id: toastId });
        } catch (error) {
          console.error(error);
          toast.error('Sync failed. Please check the Webhook URL.', { id: toastId });
        } finally {
          setSyncingGoogleSheets(false);
        }
      };
"""

content = content.replace(
    'const [activeSettingsTab, setActiveSettingsTab] = useState(\'receipt\');',
    'const [activeSettingsTab, setActiveSettingsTab] = useState(\'receipt\');\n' + js_logic
)

# 2. Add Google Sheets section to Data Management tab
ui_section = """
        <div className="pt-6 border-t">
          <h3 className="font-semibold text-slate-800 mb-4 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-600"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>
            Data Management
          </h3>
          <p className="text-sm font-semibold text-slate-700 mt-4 mb-1">Google Sheets Webhook URL</p>
          <p className="text-sm text-slate-500 mb-4">Paste your Google Apps Script Web App URL here to automatically sync your POS data to a live Google Sheet.</p>
          <input 
            className="input-field w-full mb-4" 
            placeholder="https://script.google.com/macros/s/..." 
            value={settings.googleSheetWebhookUrl || ''} 
            onChange={e => update('googleSheetWebhookUrl', e.target.value)} 
          />
          <button 
            onClick={handleGoogleSheetSync} 
            disabled={syncingGoogleSheets} 
            className={`w-full py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors ${syncingGoogleSheets ? 'bg-indigo-400 cursor-not-allowed text-white' : 'bg-indigo-600 text-white hover:bg-indigo-700'}`}
          >
            {syncingGoogleSheets ? 'Syncing...' : '✓ Force Sync All Data to Google Sheets'}
          </button>
        </div>
"""

content = content.replace(
    '{activeSettingsTab === \'data\' && (\n          <>',
    '{activeSettingsTab === \'data\' && (\n          <>\n' + ui_section
)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
