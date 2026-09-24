import re

def update_pdf_export():
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        app_content = f.read()

    # We need to find `const generatePDF = () => {` (around line 5835)
    # and `const generatePDF = () => {` inside the AutoBackup useEffect (around line 5600)
    # Actually, both can share the same async logic. Let's find both using regex.
    
    # We will replace `const generatePDF = () => {` with `const generatePDF = async () => {`
    # and add the M-Pesa fetch logic inside it.
    
    pdf_fetch_code = """
        let mpesaTx = [];
        try {
          const raw = localStorage.getItem('db_session');
          if (raw) {
            const { url, token } = JSON.parse(raw);
            if (url && token) {
              const res = await fetch('https://softlybuilt.netlify.app/api/get-transactions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, token })
              });
              const data = await res.json();
              if (data.ok && data.transactions) {
                mpesaTx = data.transactions;
              }
            }
          }
        } catch(e) {}
"""

    mpesa_table_code = "autoTable(doc, { head: [['Date', 'Transaction Code', 'Sender', 'Phone', 'Amount']], body: mpesaTx.map(t => [new Date(t.date || Date.now()).toLocaleDateString(), t.transaction_code, t.sender, t.phone || '-', t.amount]), headStyles: { fillColor: '#059669' } });"

    # Find the main generatePDF in Dashboard
    # "const generatePDF = () => {"
    
    # Wait, if we make generatePDF async, `handleDownloadPdf` must also be async:
    app_content = app_content.replace(
        "const handleDownloadPdf = () => {",
        "const handleDownloadPdf = async () => {"
    )
    app_content = app_content.replace(
        "generatePDF();",
        "await generatePDF();"
    )
    
    # Update generatePDF definitions
    app_content = app_content.replace(
        "const generatePDF = () => {\n        const doc = new jsPDF('landscape');",
        "const generatePDF = async () => {\n        const doc = new jsPDF('landscape');" + pdf_fetch_code
    )

    app_content = app_content.replace(
        "const generatePDF = () => {\n            const doc = new jsPDF('landscape');",
        "const generatePDF = async () => {\n            const doc = new jsPDF('landscape');" + pdf_fetch_code
    )
    
    # Append mpesa_table_code before doc.save
    app_content = app_content.replace(
        "doc.save(`AutoBackup_Report_",
        mpesa_table_code + "\n            doc.save(`AutoBackup_Report_"
    )
    app_content = app_content.replace(
        "doc.save(`SoftlyBuilt_Report_",
        mpesa_table_code + "\n        doc.save(`SoftlyBuilt_Report_"
    )

    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(app_content)
        
    print("PDF export updated with M-Pesa section.")

update_pdf_export()
