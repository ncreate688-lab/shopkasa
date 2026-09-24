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
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: cors, body: JSON.stringify({ ok: false, error: 'Method not allowed' }) };
  }

  let body = {};
  try {
    let rawBody = event.body || '{}';
    if (event.isBase64Encoded) {
      rawBody = Buffer.from(rawBody, 'base64').toString('utf-8');
    }
    body = JSON.parse(rawBody);
  } catch (err) {}

  const { url, token } = body;

  if (!url || typeof url !== 'string' || !token || typeof token !== 'string') {
    return { statusCode: 400, headers: cors, body: JSON.stringify({ ok: false, error: 'Both "url" and "token" fields are required.' }) };
  }

  try {
    await tursoQuery(url, token, [{ type: 'execute', stmt: { sql: 'SELECT 1' } }]);
    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: true }) };
  } catch (err) {
    const message = err?.message || 'Connection failed. Please check your URL and token.';
    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: false, error: message }) };
  }
};
