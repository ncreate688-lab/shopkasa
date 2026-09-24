import re

def update_app():
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        app_content = f.read()

    # 1. Update MpesaTrackerPanel with CSV Export and Delete
    new_tracker = """const MpesaTrackerPanel = ({ settings }) => {
      const [transactions, setTransactions] = useState([]);
      const [isLoading, setIsLoading] = useState(false);
      const [searchTerm, setSearchTerm] = useState('');
      const [startDate, setStartDate] = useState('');
      const [endDate, setEndDate] = useState('');
      const [branch, setBranch] = useState('All Branches');
      
      const fetchTransactions = async () => {
        setIsLoading(true);
        try {
          const raw = localStorage.getItem('db_session');
          if (!raw) {
             setTransactions([]);
             return;
          }
          const { url, token } = JSON.parse(raw);
          if (!url || !token) return;

          const res = await fetch('https://softlybuilt.netlify.app/api/get-transactions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, token })
          });
          const data = await res.json();
          if (data.ok && data.transactions) {
            setTransactions(data.transactions);
            if (data.transactions.length > 100) {
               handleArchiveToSheets(data.transactions, url, token);
            }
          }
        } catch (e) {
          toast.error('Network error while fetching transactions');
        } finally {
          setIsLoading(false);
        }
      };

      const handleArchiveToSheets = async (txs, url, token) => {
         toast.loading("More than 100 transactions detected. Archiving to CSV for Google Sheets...", {id: 'archive'});
         // Generate CSV
         const headers = ['Date', 'Transaction Code', 'Sender', 'Phone', 'Amount', 'Status'];
         const rows = txs.map(tx => [
             new Date(tx.date || Date.now()).toLocaleDateString(),
             tx.transaction_code,
             tx.sender,
             tx.phone || 'N/A',
             tx.amount,
             'Completed'
         ]);
         const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
         
         const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
         const link = document.createElement('a');
         const objUrl = URL.createObjectURL(blob);
         link.setAttribute('href', objUrl);
         link.setAttribute('download', `Mpesa_Transactions_Archive_${new Date().toISOString().split('T')[0]}.csv`);
         document.body.appendChild(link);
         link.click();
         document.body.removeChild(link);
         
         // Delete from API
         try {
             const res = await fetch('/api/delete-transactions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, token })
             });
             const data = await res.json();
             if (data.ok) {
                 toast.success("Archived! Open CSV in Google Sheets. Turso DB cleared to save space.", {id: 'archive'});
                 setTransactions([]);
             } else {
                 toast.error("CSV downloaded but failed to clear DB.", {id: 'archive'});
             }
         } catch(e) {
             toast.error("CSV downloaded but failed to clear DB (Network error).", {id: 'archive'});
         }
      };

      const handleManualDelete = async () => {
         if (!confirm('Are you sure you want to delete all M-Pesa transaction records from the system?')) return;
         const raw = localStorage.getItem('db_session');
         if (!raw) return;
         const { url, token } = JSON.parse(raw);
         
         try {
             const res = await fetch('/api/delete-transactions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, token })
             });
             if (res.ok) {
                setTransactions([]);
                toast.success("All transactions deleted.");
             } else {
                toast.error("Failed to delete from database.");
             }
         } catch(e) {
             toast.error("Network error while deleting.");
         }
      };

      useEffect(() => {
        fetchTransactions();
      }, []);

      const filteredTx = transactions.filter(tx => {
        if (searchTerm) {
          const s = searchTerm.toLowerCase();
          if (!tx.transaction_code?.toLowerCase().includes(s) && 
              !tx.sender?.toLowerCase().includes(s) && 
              !tx.phone?.toLowerCase().includes(s) && 
              !String(tx.amount).includes(s)) {
            return false;
          }
        }
        if (startDate && new Date(tx.date) < new Date(startDate)) return false;
        if (endDate && new Date(tx.date) > new Date(endDate)) return false;
        return true;
      });

      const totalRevenue = filteredTx.reduce((sum, tx) => sum + Number(tx.amount || 0), 0);
      const avgTx = filteredTx.length > 0 ? totalRevenue / filteredTx.length : 0;

      return (
        <div className="p-6 bg-slate-50 min-h-screen">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold text-slate-800">M-Pesa Transactions Tracker</h2>
              <p className="text-sm text-slate-500">View and track M-Pesa payments received across all configured branches.</p>
            </div>
            <div className="flex gap-2">
              <button onClick={fetchTransactions} disabled={isLoading} className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg font-semibold flex items-center gap-2 transition-colors disabled:opacity-50">
                <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} /> Refresh Transactions
              </button>
              <button onClick={handleManualDelete} className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors">
                Delete All
              </button>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6 text-amber-800">
            <div className="flex items-start gap-2">
              <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-600" />
              <div>
                <p className="font-semibold text-sm">Connection notices for some businesses:</p>
                <ul className="list-disc list-inside text-xs mt-1 space-y-0.5">
                  <li>Main Store: Local branch only (Configure cloud database to view sync'ed M-Pesa payments)</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <p className="text-sm font-medium text-slate-500 mb-1">Total M-Pesa Revenue</p>
              <p className="text-3xl font-bold text-emerald-600 mb-1">Ksh. {totalRevenue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
              <p className="text-xs text-slate-400">Sum of filtered transactions</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <p className="text-sm font-medium text-slate-500 mb-1">Transaction Count</p>
              <p className="text-3xl font-bold text-slate-800 mb-1">{filteredTx.length}</p>
              <p className="text-xs text-slate-400">Total payments detected</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <p className="text-sm font-medium text-slate-500 mb-1">Average Transaction</p>
              <p className="text-3xl font-bold text-blue-600 mb-1">Ksh. {avgTx.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
              <p className="text-xs text-slate-400">Mean value per transaction</p>
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 mb-6 flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px]">
              <label className="text-xs font-semibold text-slate-500 block mb-1 uppercase">Business / Branch</label>
              <select value={branch} onChange={e => setBranch(e.target.value)} className="w-full p-2 border border-slate-200 rounded-lg bg-slate-50 outline-none text-sm">
                <option>All Branches</option>
                <option>Main Store</option>
              </select>
            </div>
            <div className="flex-2 min-w-[250px]">
              <label className="text-xs font-semibold text-slate-500 block mb-1 uppercase">Search Details</label>
              <input type="text" value={searchTerm} onChange={e => setSearchTerm(e.target.value)} placeholder="Code, sender, phone, amt..." className="w-full p-2 border border-slate-200 rounded-lg bg-slate-50 outline-none text-sm" />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label className="text-xs font-semibold text-slate-500 block mb-1 uppercase">Start Date</label>
              <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="w-full p-2 border border-slate-200 rounded-lg bg-slate-50 outline-none text-sm" />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label className="text-xs font-semibold text-slate-500 block mb-1 uppercase">End Date</label>
              <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="w-full p-2 border border-slate-200 rounded-lg bg-slate-50 outline-none text-sm" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 border-b border-slate-100 text-slate-600 font-semibold">
                  <tr>
                    <th className="p-4">Date</th>
                    <th className="p-4">Business</th>
                    <th className="p-4">Transaction Code</th>
                    <th className="p-4">Sender</th>
                    <th className="p-4">Phone</th>
                    <th className="p-4">Amount</th>
                    <th className="p-4">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTx.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="p-12 text-center text-slate-400">
                        {isLoading ? 'Loading transactions...' : 'No M-Pesa transactions found matching filters.'}
                      </td>
                    </tr>
                  ) : (
                    filteredTx.map(tx => (
                      <tr key={tx.id} className="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                        <td className="p-4 whitespace-nowrap text-slate-500">{new Date(tx.date || Date.now()).toLocaleDateString()}</td>
                        <td className="p-4 text-slate-700">Main Store</td>
                        <td className="p-4 font-mono font-medium text-slate-800">{tx.transaction_code}</td>
                        <td className="p-4 font-semibold text-slate-700">{tx.sender}</td>
                        <td className="p-4 text-slate-500">{tx.phone || 'N/A'}</td>
                        <td className="p-4 font-bold text-emerald-600">Ksh. {Number(tx.amount).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                        <td className="p-4">
                          <span className="bg-emerald-100 text-emerald-700 px-2 py-1 rounded text-xs font-semibold">Completed</span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      );
    }"""
    
    # We replace from "const MpesaTrackerPanel = ({ settings }) => {" up to "const Dashboard ="
    app_content = re.sub(r'const MpesaTrackerPanel =.*?const Dashboard =', new_tracker + '\\n    const Dashboard =', app_content, flags=re.DOTALL)
    
    # 2. Update generatePDF (Both of them!)
    
    # Let's find and replace both generatePDF instances manually.
    
    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(app_content)
        
    print("MpesaTrackerPanel updated.")

update_app()
