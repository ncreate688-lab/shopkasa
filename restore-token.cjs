const fs = require('fs');

const path = 'c:\\Softly built updates\\license-server\\netlify\\functions\\verify-license.js';
let content = fs.readFileSync(path, 'utf8');

content = content.replace(
    "const TURSO_TOKEN = db_token || process.env.TURSO_LICENSE_TOKEN || '';",
    "const TURSO_TOKEN = db_token || process.env.TURSO_LICENSE_TOKEN || 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODQxNjU1OTQsImlkIjoiMDE5ZjY4OGUtNWEwMS03ZTRmLTk3ZDUtN2UyNTQ3M2EwMzkyIiwia2lkIjoia05aTnBZOWg1QldlX0FHdzU4RG40RFNCbllDWWZPWUJWLTFTZ3V5NE5XOCIsInJpZCI6IjBiYTY0YzQxLWM1YjMtNDc5OS05MDBmLTFiNWU3ZmFkYWQ0NiJ9.aHdrwvBjrlGV49sXTViHqCDUI7lvmZrriUQXenim6Bv-YWT1JzrEW-hgE2aV1blsbM2Rw3nzVZDwEh9v9WfGDQ';"
);

fs.writeFileSync(path, content, 'utf8');
console.log("Token restored");
