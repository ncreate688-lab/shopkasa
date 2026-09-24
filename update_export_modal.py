import re

def update_app():
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        app_content = f.read()

    # 1. Update the Excel and PDF buttons
    # We can just replace the onClick handlers string by string based on the known types.
    
    types = ['sales', 'stock', 'products', 'customers', 'debts', 'suppliers']
    
    for t in types:
        # Excel button
        old_excel_btn = f"onClick={{() => toast.success('Excel export uses CSV logic for now.')}}"
        new_excel_btn = f"onClick={{() => setExportModalState({{ isOpen: true, type: '{t}', format: 'excel' }})}}"
        
        # We need to find the specific block for each type. 
        # A safer way is to use regex to find the CSV button, extract type, and update the next Excel button.
    
    # Let's use regex to find `<button onClick={() => setExportModalState({ isOpen: true, type: '(.*?)', format: 'csv' })}`
    # and then replace the next `toast.success('Excel export uses CSV logic for now.')` with `setExportModalState({ isOpen: true, type: '\1', format: 'excel' })`
    
    def repl_excel(m):
        type_val = m.group(1)
        return m.group(0).replace(
            "onClick={() => toast.success('Excel export uses CSV logic for now.')}", 
            f"onClick={{() => setExportModalState({{ isOpen: true, type: '{type_val}', format: 'excel' }})}}"
        ).replace(
            "onClick={() => toast.success('PDF generation coming soon')}",
            f"onClick={{() => setExportModalState({{ isOpen: true, type: '{type_val}', format: 'pdf' }})}}"
        )
        
    # The block spans across a few lines, so we use DOTALL
    pattern = r"(setExportModalState\(\{\s*isOpen:\s*true,\s*type:\s*'([^']+)',\s*format:\s*'csv'\s*\}\).*?)(?=setExportModalState\(\{\s*isOpen:\s*true,\s*type:\s*'[^']+',\s*format:\s*'csv'\s*\}\)|$)"
    
    app_content = re.sub(pattern, repl_excel, app_content, flags=re.DOTALL)
    
    # Fix the M-Pesa one because it might have been manually added:
    app_content = app_content.replace(
        "onClick={() => toast.success('Excel export uses CSV logic for now.')}",
        "onClick={() => toast.success('Excel export uses CSV logic for now.')}" # if any missed, leave them or we can fix them.
    )

    # 2. Rewrite handleExportConfirm
    
    new_handle_export = """      const handleExportConfirm = () => {
         let headers = '';
         let rows = '';
         let filename = '';
         let pdfData = [];
         let pdfHeaders = [];

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

         let exportData = [];

         if (exportModalState.type === 'sales') {
            const data = filterByDate(props.salesHistory || []);
            if (!data.length) { toast.error('No data for selected range'); return; }
            headers = 'Date,Product,Quantity,Total,Cashier\\n';
            rows = data.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.quantity},${s.finalPrice},"${s.cashierName}"`).join('\\n');
            filename = 'sales_history';
            pdfHeaders = [['Date', 'Product', 'Quantity', 'Total', 'Cashier']];
            pdfData = data.map(s => [new Date(s.date).toLocaleDateString(), s.name, s.quantity, s.finalPrice, s.cashierName]);
         }
         else if (exportModalState.type === 'stock') {
            const data = filterByDate(props.stockHistory || []);
            if (!data.length) { toast.error('No data for selected range'); return; }
            headers = 'Date,Product,Quantity,Action,Cashier\\n';
            rows = data.map(s => `${new Date(s.date).toLocaleDateString()},"${s.name}",${s.qty},"${s.action}","${s.cashierName}"`).join('\\n');
            filename = 'stock_history';
            pdfHeaders = [['Date', 'Product', 'Quantity', 'Action', 'Cashier']];
            pdfData = data.map(s => [new Date(s.date).toLocaleDateString(), s.name, s.qty, s.action, s.cashierName]);
         }
         else if (exportModalState.type === 'debts') {
            const data = filterByDate(props.debts || [], 'dateAdded');
            if (!data.length) { toast.error('No data for selected range'); return; }
            headers = 'Customer,Amount,Date\\n';
            rows = data.map(d => `"${d.name}",${d.amount},${new Date(d.dateAdded).toLocaleDateString()}`).join('\\n');
            filename = 'debts';
            pdfHeaders = [['Customer', 'Amount', 'Date']];
            pdfData = data.map(d => [d.name, d.amount, new Date(d.dateAdded).toLocaleDateString()]);
         }
         else if (exportModalState.type === 'products') {
            const data = props.products || []; 
            if (!data.length) { toast.error('No data'); return; }
            headers = 'Name,Category,Stock,Price,Cost\\n';
            rows = data.map(p => `"${p.name}","${p.category}",${p.stock},${p.price},${p.cost}`).join('\\n');
            filename = 'products';
            pdfHeaders = [['Name', 'Category', 'Stock', 'Price', 'Cost']];
            pdfData = data.map(p => [p.name, p.category, p.stock, p.price, p.cost]);
         }
         else if (exportModalState.type === 'customers') {
            const data = props.customers || []; 
            if (!data.length) { toast.error('No data'); return; }
            headers = 'Name,Phone,Email\\n';
            rows = data.map(c => `"${c.name}","${c.phone}","${c.email}"`).join('\\n');
            filename = 'customers';
            pdfHeaders = [['Name', 'Phone', 'Email']];
            pdfData = data.map(c => [c.name, c.phone, c.email]);
         }
         else if (exportModalState.type === 'suppliers') {
            const data = props.suppliers || []; 
            if (!data.length) { toast.error('No data'); return; }
            headers = 'Name,Phone,Email\\n';
            rows = data.map(s => `"${s.name}","${s.phone}","${s.email}"`).join('\\n');
            filename = 'suppliers';
            pdfHeaders = [['Name', 'Phone', 'Email']];
            pdfData = data.map(s => [s.name, s.phone, s.email]);
         }
         else if (exportModalState.type === 'mpesa') {
             // M-Pesa is handled differently by fetching, but we can do it here if needed.
             // Actually M-Pesa export has its own button logic right now.
             toast.error("M-Pesa export uses its own button logic for now.");
             return;
         }

         if (exportModalState.format === 'pdf') {
             const doc = new jsPDF('landscape');
             doc.setFontSize(14);
             doc.text(`Data Export - ${exportModalState.type.toUpperCase()}`, 14, 20);
             if (exportStartDate || exportEndDate) {
                 doc.setFontSize(10);
                 doc.text(`Range: ${exportStartDate || 'Start'} to ${exportEndDate || 'End'}`, 14, 28);
             }
             autoTable(doc, { startY: 35, head: pdfHeaders, body: pdfData, headStyles: { fillColor: '#059669' } });
             doc.save(`${filename}_${new Date().toISOString().split('T')[0]}.pdf`);
         } else {
             const ext = exportModalState.format === 'excel' ? 'csv' : 'csv'; // Use CSV for Excel compatibility
             const blob = new Blob([headers + rows], { type: 'text/csv' });
             const url = URL.createObjectURL(blob);
             const a = document.createElement('a'); a.href = url; a.download = `${filename}.${ext}`; a.click();
             URL.revokeObjectURL(url);
         }
         
         setExportModalState({ isOpen: false, type: null, format: null });
      };"""

    # We need to replace the old handleExportConfirm up to `setExportModalState({ isOpen: false, type: null, format: null });\n      };`
    # Let's find the start
    start_str = "const handleExportConfirm = () => {"
    end_str = "setExportModalState({ isOpen: false, type: null, format: null });\n      };"
    
    start_idx = app_content.find(start_str)
    end_idx = app_content.find(end_str, start_idx) + len(end_str)
    
    if start_idx != -1 and end_idx != -1:
        app_content = app_content[:start_idx] + new_handle_export + app_content[end_idx:]
    else:
        print("Could not find handleExportConfirm block!")
        
    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(app_content)
        
    print("Export modal updated successfully.")

update_app()
