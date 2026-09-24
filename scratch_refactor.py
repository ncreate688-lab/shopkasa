import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add activeSettingsTab state
content = content.replace(
    'const [selectedCashierQR, setSelectedCashierQR] = useState(null);',
    'const [selectedCashierQR, setSelectedCashierQR] = useState(null);\n      const [activeSettingsTab, setActiveSettingsTab] = useState(\'receipt\');'
)

# 2. Modify top of Settings panel to include tabs
content = content.replace(
    '<div className="card space-y-6 bg-white p-6">\n        <div><h3 className="font-semibold text-slate-800 mb-3">Receipt Details</h3>',
    '<div className="card bg-white p-0 overflow-hidden">\n        <div className="flex border-b border-slate-200 overflow-x-auto hide-scrollbar px-2 pt-2 bg-slate-50">\n          <button onClick={() => setActiveSettingsTab(\'receipt\')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeSettingsTab === \'receipt\' ? \'border-emerald-600 text-emerald-600\' : \'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300\'}`}>Receipt Details</button>\n          <button onClick={() => setActiveSettingsTab(\'features\')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeSettingsTab === \'features\' ? \'border-emerald-600 text-emerald-600\' : \'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300\'}`}>Features & Options</button>\n          <button onClick={() => setActiveSettingsTab(\'security\')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeSettingsTab === \'security\' ? \'border-emerald-600 text-emerald-600\' : \'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300\'}`}>Security</button>\n          <button onClick={() => setActiveSettingsTab(\'data\')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeSettingsTab === \'data\' ? \'border-emerald-600 text-emerald-600\' : \'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300\'}`}>Data Management</button>\n        </div>\n        <div className="p-6 space-y-6">\n        {activeSettingsTab === \'receipt\' && (\n          <>\n        <div><h3 className="font-semibold text-slate-800 mb-3">Receipt Details</h3>'
)

# 3. Staff management -> close Receipt, start Security
content = content.replace(
    '<div className="bg-slate-50 p-4 rounded-lg border border-slate-200 pt-6 border-t">\n          <h3 className="font-semibold text-slate-800 flex items-center gap-2"><UserPlus className="w-4 h-4 text-emerald-600" /> Staff Management</h3>',
    '</>\n        )}\n        {activeSettingsTab === \'security\' && (\n          <>\n        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">\n          <h3 className="font-semibold text-slate-800 flex items-center gap-2"><UserPlus className="w-4 h-4 text-emerald-600" /> Staff Management</h3>'
)

# 4. Features & Options (Starts after Owner Login, at Track Expiry Dates)
content = content.replace(
    '<div className="space-y-4 pt-4 border-t border-slate-100"><div className="flex justify-between items-center"><span className="text-slate-700 font-medium">Track Expiry Dates</span>',
    '</>\n        )}\n        {activeSettingsTab === \'features\' && (\n          <>\n        <div className="space-y-4"><div className="flex justify-between items-center"><span className="text-slate-700 font-medium">Track Expiry Dates</span>'
)

# 5. Data Management (Starts at Data Reset Schedule)
content = content.replace(
    '<div className="bg-red-50 p-4 rounded-lg border border-red-200 mt-6 pt-4 border-t">\n          <h3 className="font-semibold text-red-800 flex items-center gap-2"><Trash2 className="w-4 h-4" /> Monthly Data Reset Schedule</h3>',
    '</>\n        )}\n        {activeSettingsTab === \'data\' && (\n          <>\n        <div className="bg-red-50 p-4 rounded-lg border border-red-200">\n          <h3 className="font-semibold text-red-800 flex items-center gap-2"><Trash2 className="w-4 h-4" /> Monthly Data Reset Schedule</h3>'
)

# 6. Put ConnectDatabaseSection and CloudRecoverySection in Security Tab
content = content.replace(
    '<ConnectDatabaseSection />\n        <CloudRecoverySection />\n\n        <div className="bg-red-50 p-6 rounded-2xl border border-red-200 mt-6 shadow-sm">\n          <h3 className="font-bold text-lg mb-2 flex items-center gap-2 text-red-700">',
    '</>\n        )}\n        {activeSettingsTab === \'security\' && (\n          <>\n        <ConnectDatabaseSection />\n        <CloudRecoverySection />\n          </>\n        )}\n        {activeSettingsTab === \'data\' && (\n        <div className="bg-red-50 p-6 rounded-2xl border border-red-200 mt-6 shadow-sm">\n          <h3 className="font-bold text-lg mb-2 flex items-center gap-2 text-red-700">'
)

# 7. Close the Data Management Tab at the end of card
content = content.replace(
    '</button>\n        </div>\n      </div>\n        {showFullImportModal && (',
    '</button>\n        </div>\n        )}\n        </div>\n      </div>\n        {showFullImportModal && ('
)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done replacing.')
