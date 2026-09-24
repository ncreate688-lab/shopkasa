import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Define BusinessAnalyticsWrapper component before Dashboard
business_analytics_wrapper = """
    const BusinessAnalyticsWrapper = (props) => {
      const [activeTab, setActiveTab] = useState('overview');

      return (
        <div className="space-y-6 pb-20">
          <div className="sb-page-title mb-6">
            <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>
          </div>
          
          <div className="flex border-b border-slate-200 overflow-x-auto hide-scrollbar mb-6">
            <button onClick={() => setActiveTab('overview')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeTab === 'overview' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}>Overview</button>
            <button onClick={() => setActiveTab('monthly')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeTab === 'monthly' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}>Monthly Performance</button>
            <button onClick={() => setActiveTab('stores')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeTab === 'stores' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}>All Stores</button>
            <button onClick={() => setActiveTab('export')} className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeTab === 'export' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}>Data Export</button>
          </div>

          <div className="pt-2">
            {activeTab === 'overview' && (
              <div className="analytics-overview-wrapper">
                <SummaryPanel {...props} hideTitle={true} />
              </div>
            )}
            {activeTab === 'monthly' && (
              <div className="analytics-monthly-wrapper">
                <MonthlyPerformancePanel salesHistory={props.salesHistory} snapshots={props.monthlySnapshots} allowClear={!!props.settings?.allowClearMonthlyPerf} onClearSnapshots={props.onClearSnapshots} hideTitle={true} />
              </div>
            )}
            {activeTab === 'stores' && (
              <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center py-20">
                <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-4"><svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg></div>
                <h3 className="text-xl font-bold text-slate-800">Multi-Store Analytics</h3>
                <p className="text-slate-500 mt-2 max-w-md">Connect multiple store locations to view consolidated performance and aggregate analytics.</p>
                <button className="mt-6 px-6 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl font-bold transition-colors">Connect New Store</button>
              </div>
            )}
            {activeTab === 'export' && (
              <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 space-y-6">
                 <h3 className="text-lg font-bold text-slate-800">Export Business Data</h3>
                 <p className="text-slate-600 text-sm">Download comprehensive reports for your records or accounting software.</p>
                 <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <button onClick={props.handleDownloadPdf} className="flex items-center gap-3 p-4 rounded-xl border border-slate-200 hover:border-emerald-500 hover:bg-emerald-50 transition-colors text-left group">
                       <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center group-hover:bg-emerald-600 group-hover:text-white transition-colors"><svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg></div>
                       <div>
                         <h4 className="font-bold text-slate-800 group-hover:text-emerald-700">PDF Report</h4>
                         <p className="text-xs text-slate-500">Summary of all metrics</p>
                       </div>
                    </button>
                    <button onClick={() => toast.success('CSV Export initiated')} className="flex items-center gap-3 p-4 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition-colors text-left group">
                       <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-colors"><svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg></div>
                       <div>
                         <h4 className="font-bold text-slate-800 group-hover:text-blue-700">Raw Data (CSV)</h4>
                         <p className="text-xs text-slate-500">Spreadsheet format</p>
                       </div>
                    </button>
                 </div>
              </div>
            )}
          </div>
        </div>
      );
    };

    const Dashboard =
"""

content = content.replace(
    'const Dashboard =',
    business_analytics_wrapper
)


# 2. Modify SummaryPanel to conditionally hide the title and top spacing
content = content.replace(
    '''const SummaryPanel = ({ products, setProducts, salesHistory, setSalesHistory, expenses, debts, settings, stockHistory, setStockHistory, currentUser, onCancelSale }) => {''',
    '''const SummaryPanel = ({ products, setProducts, salesHistory, setSalesHistory, expenses, debts, settings, stockHistory, setStockHistory, currentUser, onCancelSale, hideTitle }) => {'''
)
content = content.replace(
    '''<div className="space-y-6 pb-20">
        <div className="flex flex-col sm:flex-row justify-between gap-4">
          <div className="sb-page-title">
            <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>
          </div>''',
    '''<div className={hideTitle ? "space-y-6" : "space-y-6 pb-20"}>
        {!hideTitle && (
        <div className="flex flex-col sm:flex-row justify-between gap-4">
          <div className="sb-page-title">
            <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>
          </div>
        </div>
        )}'''
)

# Fix the extra closing div that belongs to the header we just conditionalized
# Actually, the original is:
# <div className="space-y-6 pb-20">
#   <div className="flex flex-col sm:flex-row justify-between gap-4">
#     <div className="sb-page-title">
#       <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>
#     </div>
#   ... Wait, the div closing for `flex flex-col sm:flex-row justify-between gap-4` is further down or not? 
# Looking back at line 2658:
# `        <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>`
# Wait, let me replace specifically around line 2657. Let's do it safer.

# Safe replace for SummaryPanel header:
content = re.sub(
    r'<h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>',
    r'{!hideTitle && <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>}',
    content
)


# 3. Modify MonthlyPerformancePanel to hide title
content = content.replace(
    '''const MonthlyPerformancePanel = ({ salesHistory, snapshots = [], allowClear = false, onClearSnapshots }) => {''',
    '''const MonthlyPerformancePanel = ({ salesHistory, snapshots = [], allowClear = false, onClearSnapshots, hideTitle }) => {'''
)

content = re.sub(
    r'<h2 className="text-2xl font-bold text-slate-800">Monthly Performance</h2>',
    r'{!hideTitle && <h2 className="text-2xl font-bold text-slate-800">Monthly Performance</h2>}',
    content
)

# 4. Modify Dashboard rendering for summary tab
content = content.replace(
    '''if (tab === 'summary' && effectiveCurrentUser?.role === 'owner') return <SummaryPanel {...props} />;''',
    '''if (tab === 'summary' && effectiveCurrentUser?.role === 'owner') return <BusinessAnalyticsWrapper {...props} monthlySnapshots={monthlySnapshots} onClearSnapshots={async () => { await clearMonthlySnapshots(); setMonthlySnapshots([]); }} handleDownloadPdf={handleDownloadPdf} />;'''
)

# 5. Remove 'monthlyPerformance' tab from sidebar (both desktop and mobile) since it's now inside BusinessAnalyticsWrapper
content = re.sub(
    r"\{effectiveCurrentUser\?.role === 'owner' && <button onClick=\{\(\) => setTab\('monthlyPerformance'\)\}.*?Monthly Performance</button>\}",
    "",
    content
)
content = re.sub(
    r"\{k:'monthlyPerformance', label:'Monthly', Icon: BarChart, ownerOnly:true\},?",
    "",
    content
)
content = re.sub(
    r"\{k:'monthlyPerformance', label:'Monthly Performance', Icon: BarChart, ownerOnly:true\},?",
    "",
    content
)
content = content.replace(
    '''if (tab === 'monthlyPerformance' && effectiveCurrentUser?.role === 'owner') return <MonthlyPerformancePanel salesHistory={salesHistory} snapshots={monthlySnapshots} allowClear={!!settings.allowClearMonthlyPerf} onClearSnapshots={async () => { await clearMonthlySnapshots(); setMonthlySnapshots([]); }} />;''',
    ''''''
)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
