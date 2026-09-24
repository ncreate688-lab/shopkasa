const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Content-Type': 'application/json'
};

async function tursoQuery(dbUrl, dbToken, requests) {
  const url = dbUrl.trim().replace(/^libsql:\/\//, 'https://').replace(/\/$/, '');
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

  try {
    let rawBody = event.body || '{}';
    if (event.isBase64Encoded) rawBody = Buffer.from(rawBody, 'base64').toString('utf-8');
    const body = JSON.parse(rawBody);
    const {
      transaction_code,
      amount,
      sender,
      phone,
      timestamp,
      store_id,
      token,
      url: bodyUrl,
      db_token: bodyDbToken
    } = body;

    if (!transaction_code) return { statusCode: 400, headers: cors, body: JSON.stringify({ ok: false, error: 'Missing transaction_code' }) };
    if (!amount && amount !== 0) return { statusCode: 400, headers: cors, body: JSON.stringify({ ok: false, error: 'Missing amount' }) };

    const dbUrl = (bodyUrl || process.env.TURSO_DATABASE_URL || '').trim().replace(/^libsql:\/\//, 'https://');
    const dbToken = (bodyUrl ? (bodyDbToken || '') : (bodyDbToken || process.env.TURSO_AUTH_TOKEN || '')).replace(/[\s'"]/g, '');

    if (!dbUrl || !dbToken) {
      return { statusCode: 500, headers: cors, body: JSON.stringify({ ok: false, error: 'No database credentials provided or configured.' }) };
    }

    const schemas = [
      `CREATE TABLE IF NOT EXISTS mpesa_transactions (
        id TEXT PRIMARY KEY,
        transaction_code TEXT UNIQUE,
        amount REAL,
        sender TEXT,
        phone TEXT,
        timestamp TEXT,
        store_id TEXT,
        status TEXT DEFAULT 'pending'
      )`,
      `ALTER TABLE mpesa_transactions ADD COLUMN store_id TEXT`
    ];

    const id = `mpesa_${transaction_code}_${Date.now()}`;
    const ts = timestamp || new Date().toISOString();
    const amt = parseFloat(amount) || 0;

    const reqs = [
      { type: 'execute', stmt: { sql: schemas[0], args: [] } },
      { type: 'execute', stmt: { sql: schemas[1], args: [] } },
      { type: 'execute', stmt: { sql: `INSERT OR IGNORE INTO mpesa_transactions (id, transaction_code, amount, sender, phone, timestamp, store_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')`, args: [{type: 'text', value: id}, {type: 'text', value: transaction_code}, {type: 'float', value: amt}, {type: 'text', value: sender || ''}, {type: 'text', value: phone || ''}, {type: 'text', value: ts}, {type: 'text', value: store_id || ''}] } }
    ];

    try {
      await tursoQuery(dbUrl, dbToken, reqs);
    } catch(err) {
      if (!err.message.includes('duplicate column name')) throw err;
    }

    return { 
      statusCode: 200, 
      headers: cors, 
      body: JSON.stringify({
        ok: true,
        message: `Payment ${transaction_code} of Ksh${amount} recorded successfully.`,
        store_id: store_id || 'default'
      }) 
    };

  } catch (err) {
    console.error('sync-sms error:', err);
    return { statusCode: 500, headers: cors, body: JSON.stringify({ ok: false, error: err?.message || 'Internal server error' }) };
  }
};
