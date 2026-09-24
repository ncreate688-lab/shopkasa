const fs = require('fs');

const path = 'c:\\Softly built updates\\license-server\\index.html';
let content = fs.readFileSync(path, 'utf8');

// 1. Add column header Action
content = content.replace('<th>Status</th>', '<th>Status</th>\n                  <th>Action</th>');

// 2. Add button to row
const rowReplacement = `<td class="status-\${row.status}">\${row.status.toUpperCase()}</td>
                        <td>
                            <button onclick="toggleLock('\${row.username}', '\${row.status}')" style="padding:4px 8px; font-size:12px; cursor:pointer;">
                                \${row.status === 'active' ? '🔒 Lock' : '🔓 Unlock'}
                            </button>
                        </td>`;
content = content.replace(/<td class="status-\$\{row\.status\}">\$\{row\.status\.toUpperCase\(\)\}<\/td>/, rowReplacement);

// 3. Add toggleLock function
const toggleLockFn = `
    async function toggleLock(username, currentStatus) {
        if(!confirm(\`Are you sure you want to \${currentStatus === 'active' ? 'lock' : 'unlock'} \${username}?\`)) return;
        const newStatus = currentStatus === 'active' ? 'locked' : 'active';
        try {
            await tursoQuery(
                "UPDATE licenses SET status = ? WHERE username = ?",
                [
                    { type: "text", value: newStatus },
                    { type: "text", value: username }
                ]
            );
            loadLicenses();
        } catch(e) {
            alert("Error updating status: " + e.message);
        }
    }
    
    async function loadLicenses() {`;

content = content.replace('async function loadLicenses() {', toggleLockFn);

fs.writeFileSync(path, content, 'utf8');
console.log("admin.html updated");
