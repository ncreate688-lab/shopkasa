const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
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
  if (event.httpMethod !== 'POST' && event.httpMethod !== 'GET') return { statusCode: 405, headers: cors, body: JSON.stringify({ ok: false, error: 'Method not allowed' }) };

  try {
    let rawBody = event.body || '{}';
    if (event.isBase64Encoded) rawBody = Buffer.from(rawBody, 'base64').toString('utf-8');
    let body = {};
    try { body = JSON.parse(rawBody); } catch(_) {}

    const query = event.queryStringParameters || {};
    const storeId = body.store_id || query.store_id;
    const dbUrl = (body.url || query.url || process.env.TURSO_DATABASE_URL || '').trim().replace(/^libsql:\/\//, 'https://');
    const providedToken = body.db_token || body.token || query.db_token;
    const dbToken = ((body.url || query.url) ? (providedToken || '') : (providedToken || process.env.TURSO_AUTH_TOKEN || '')).replace(/\s+/g, '');

    if (!dbUrl || !dbToken) {
      return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: false, error: 'No database credentials configured.' }) };
    }

    let sql = 'SELECT * FROM mpesa_transactions ORDER BY timestamp DESC LIMIT 50';
    let args = [];
    if (storeId) {
      sql = 'SELECT * FROM mpesa_transactions WHERE store_id = ? ORDER BY timestamp DESC LIMIT 50';
      args = [{type: 'text', value: storeId}];
    }

    let rows = [];
    try {
      const data = await tursoQuery(dbUrl, dbToken, [{ type: 'execute', stmt: { sql, args } }]);
      const rs = data.results[0].response.result;
      rows = rs.rows.map(row => {
        const obj = {};
        rs.cols.forEach((col, i) => {
          obj[col.name] = row[i].value;
        });
        return obj;
      });
    } catch (err) {
      if (err.message && err.message.includes('no such table')) {
        return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: true, transactions: [] }) };
      }
      throw err;
    }

    let responseBody = { ok: true, transactions: rows };
    
    if (rows.length > 0) {
      const latestTx = rows[0]; // ordered by timestamp DESC
      responseBody.found = true;
      responseBody.txId = latestTx.id;
      responseBody.txAmt = latestTx.amount;
      responseBody.sender = latestTx.sender;
      responseBody.txCode = latestTx.transaction_code;
    } else {
      responseBody.found = false;
    }

    return { 
      statusCode: 200, 
      headers: cors, 
      body: JSON.stringify(responseBody) 
    };

  } catch (err) {
    console.error('get-transactions error:', err);
    return { statusCode: 500, headers: cors, body: JSON.stringify({ ok: false, error: err?.message || 'Internal server error' }) };
  }
};
