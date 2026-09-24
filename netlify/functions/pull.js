const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Content-Type': 'application/json'
};

async function tursoQuery(dbUrl, dbToken, requests) {
  const url = dbUrl.trim().replace(/^libsql:\/\//, 'https://');
  const res = await fetch(`${url}/v2/pipeline`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${dbToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ requests })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(`Turso HTTP ${res.status}: ${JSON.stringify(data)}`);
  return data;
}

export const handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers: cors, body: '' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers: cors, body: JSON.stringify({ ok: false, error: 'Method not allowed' }) };

  let body = {};
  try {
    let rawBody = event.body || '{}';
    if (event.isBase64Encoded) rawBody = Buffer.from(rawBody, 'base64').toString('utf-8');
    body = JSON.parse(rawBody);
  } catch (_) {}

  const { url: bodyUrl, token: bodyToken } = body;
  const url = (bodyUrl || process.env.TURSO_DATABASE_URL || '').trim().replace(/^libsql:\/\//, 'https://');
  const token = (bodyUrl ? (bodyToken || '') : (bodyToken || process.env.TURSO_AUTH_TOKEN || '')).replace(/\s+/g, '');

  if (!url || !token) return { statusCode: 500, headers: cors, body: JSON.stringify({ ok: false, error: 'Database configuration missing.' }) };

  try {
    const schemas = [
      `CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, firebase_uid TEXT UNIQUE, full_name TEXT, email TEXT, role TEXT, business_id TEXT, created_at TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, name TEXT, price REAL, costPrice REAL, barcode TEXT, expiryDate TEXT, quantity REAL, category TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS salesHistory (id TEXT PRIMARY KEY, date TEXT, total REAL, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS customers (id TEXT PRIMARY KEY, name TEXT, phone TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS debts (id TEXT PRIMARY KEY, customerName TEXT, amount REAL, date TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS paidDebts (id TEXT PRIMARY KEY, customerName TEXT, amount REAL, date TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS expenses (id TEXT PRIMARY KEY, category TEXT, amount REAL, date TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS stockHistory (id TEXT PRIMARY KEY, productName TEXT, addedQuantity REAL, date TEXT, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, full_json TEXT)`,
      `CREATE TABLE IF NOT EXISTS superAdminSettings (id INTEGER PRIMARY KEY, full_json TEXT)`
    ];
    
    let schemaRequests = schemas.map(sql => ({ type: 'execute', stmt: { sql } }));
    await tursoQuery(url, token, schemaRequests);

    const tables = ['users', 'products', 'salesHistory', 'customers', 'debts', 'paidDebts', 'expenses', 'stockHistory', 'settings', 'superAdminSettings'];
    let selectRequests = tables.map(t => ({ type: 'execute', stmt: { sql: `SELECT full_json FROM ${t}` } }));
    const results = await tursoQuery(url, token, selectRequests);

    const data = {};
    if (results.results) {
        results.results.forEach((resultItem, idx) => {
          const key = tables[idx];
          const parsedRows = [];
          if (resultItem.response && resultItem.response.result && resultItem.response.result.rows) {
              for (const row of resultItem.response.result.rows) {
                if (row[0] && row[0].value) {
                  try { const item = JSON.parse(row[0].value); if (item && typeof item === 'object') parsedRows.push(item); } catch (_) {}
                }
              }
          }
          data[key] = (key === 'settings' || key === 'superAdminSettings') ? (parsedRows[0] ?? null) : parsedRows;
        });
    }

    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: true, data }) };
  } catch (err) {
    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: false, error: err?.message || 'Pull failed.' }) };
  }
};
