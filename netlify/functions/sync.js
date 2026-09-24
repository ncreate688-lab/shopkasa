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

  const { url: bodyUrl, token: bodyToken, key, value } = body;
  const url = (bodyUrl || process.env.TURSO_DATABASE_URL || '').trim().replace(/^libsql:\/\//, 'https://');
  const token = (bodyUrl ? (bodyToken || '') : (bodyToken || process.env.TURSO_AUTH_TOKEN || '')).replace(/\s+/g, '');

  if (!url || !token) return { statusCode: 500, headers: cors, body: JSON.stringify({ ok: false, error: 'Database configuration missing.' }) };

  try {
    const schemas = {
      users: `CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, firebase_uid TEXT UNIQUE, full_name TEXT, email TEXT, role TEXT, business_id TEXT, created_at TEXT, full_json TEXT)`,
      products: `CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, name TEXT, price REAL, costPrice REAL, barcode TEXT, expiryDate TEXT, quantity REAL, category TEXT, full_json TEXT)`,
      salesHistory: `CREATE TABLE IF NOT EXISTS salesHistory (id TEXT PRIMARY KEY, date TEXT, total REAL, full_json TEXT)`,
      customers: `CREATE TABLE IF NOT EXISTS customers (id TEXT PRIMARY KEY, name TEXT, phone TEXT, full_json TEXT)`,
      debts: `CREATE TABLE IF NOT EXISTS debts (id TEXT PRIMARY KEY, customerName TEXT, amount REAL, date TEXT, full_json TEXT)`,
      paidDebts: `CREATE TABLE IF NOT EXISTS paidDebts (id TEXT PRIMARY KEY, customerName TEXT, amount REAL, date TEXT, full_json TEXT)`,
      expenses: `CREATE TABLE IF NOT EXISTS expenses (id TEXT PRIMARY KEY, category TEXT, amount REAL, date TEXT, full_json TEXT)`,
      stockHistory: `CREATE TABLE IF NOT EXISTS stockHistory (id TEXT PRIMARY KEY, productName TEXT, addedQuantity REAL, date TEXT, full_json TEXT)`,
      settings: `CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, full_json TEXT)`,
      superAdminSettings: `CREATE TABLE IF NOT EXISTS superAdminSettings (id INTEGER PRIMARY KEY, full_json TEXT)`
    };

    if (!schemas[key]) return { statusCode: 400, headers: cors, body: JSON.stringify({ ok: false, error: 'Unknown collection' }) };
    
    let parsedData = [];
    try { parsedData = JSON.parse(value); }
    catch (_) { return { statusCode: 400, headers: cors, body: JSON.stringify({ ok: false, error: 'Invalid JSON' }) }; }

    const requests = [
      { type: 'execute', stmt: { sql: schemas[key] } },
      { type: 'execute', stmt: { sql: `DELETE FROM ${key}` } }
    ];

    if (key === 'settings' || key === 'superAdminSettings') {
      requests.push({ type: 'execute', stmt: { sql: `INSERT INTO ${key} (id, full_json) VALUES (1, ?)`, args: [{ type: 'text', value: JSON.stringify(parsedData) }] } });
    } else if (Array.isArray(parsedData)) {
      const tableConfigs = {
        users: { cols: ['id','firebase_uid','full_name','email','role','business_id','created_at','full_json'], getArgs: (item,id) => [id,item.firebase_uid||'',item.full_name||'',item.email||'',item.role||'',item.business_id||'',item.created_at||'',JSON.stringify(item)] },
        products: { cols: ['id','name','price','costPrice','barcode','expiryDate','quantity','category','full_json'], getArgs: (item,id) => [id,item.name||'',item.price||0,item.cost||item.costPrice||0,item.barcode||'',item.expiryDate||'',item.stock||item.quantity||0,item.category||'',JSON.stringify(item)] },
        salesHistory: { cols: ['id','date','total','full_json'], getArgs: (item,id) => [id,item.date||'',item.total||item.finalPrice||0,JSON.stringify(item)] },
        customers: { cols: ['id','name','phone','full_json'], getArgs: (item,id) => [id,item.name||'',item.phone||'',JSON.stringify(item)] },
        debts: { cols: ['id','customerName','amount','date','full_json'], getArgs: (item,id) => [id,item.customerName||item.name||'',item.amount||0,item.date||'',JSON.stringify(item)] },
        paidDebts: { cols: ['id','customerName','amount','date','full_json'], getArgs: (item,id) => [id,item.customerName||item.name||'',item.amount||0,item.date||'',JSON.stringify(item)] },
        expenses: { cols: ['id','category','amount','date','full_json'], getArgs: (item,id) => [id,item.category||item.name||'',item.amount||0,item.date||'',JSON.stringify(item)] },
        stockHistory: { cols: ['id','productName','addedQuantity','date','full_json'], getArgs: (item,id) => [id,item.productName||'',item.addedQuantity||0,item.date||'',JSON.stringify(item)] }
      };
      const cfg = tableConfigs[key];
      if (cfg) {
        const BATCH_SIZE = 40;
        for (let i = 0; i < parsedData.length; i += BATCH_SIZE) {
          const chunk = parsedData.slice(i, i + BATCH_SIZE);
          const placeholders = chunk.map(() => `(${cfg.cols.map(() => '?').join(', ')})`).join(', ');
          const flatArgs = [];
          chunk.forEach((item, idx) => {
            const id = String(item.id || item.date || (i + idx));
            flatArgs.push(...cfg.getArgs(item, id));
          });
          const args = flatArgs.map(v => {
            if (typeof v === 'number') return { type: 'float', value: v };
            if (v === null) return { type: 'null' };
            return { type: 'text', value: String(v) };
          });
          requests.push({
            type: 'execute',
            stmt: { sql: `INSERT INTO ${key} (${cfg.cols.join(', ')}) VALUES ${placeholders}`, args }
          });
        }
      }
    }

    requests.push({ type: 'execute', stmt: { sql: `CREATE TABLE IF NOT EXISTS meta (id INTEGER PRIMARY KEY, last_modified INTEGER NOT NULL DEFAULT 0)` } });
    requests.push({ type: 'execute', stmt: { sql: `INSERT OR REPLACE INTO meta (id, last_modified) VALUES (1, ${Date.now()})` } });

    await tursoQuery(url, token, requests);

    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: true }) };
  } catch (err) {
    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: false, error: err?.message || 'Sync failed.' }) };
  }
};

