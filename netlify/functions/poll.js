// netlify/functions/poll.js
// Uses fetch directly to Turso HTTP pipeline — no npm dependencies needed

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Content-Type': 'application/json'
};

async function tursoQuery(dbUrl, dbToken, requests) {
  const url = dbUrl.trim().replace(/^libsql:\/\//, 'https://');
  const res = await fetch(`${url}/v2/pipeline`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${dbToken}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ requests })
  });
  if (!res.ok) throw new Error(`Turso HTTP ${res.status}`);
  return res.json();
}

export const handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers: cors, body: '' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers: cors, body: JSON.stringify({ ok: false, error: 'Method not allowed' }) };

  let body = {};
  try {
    let rawBody = event.body || '{}';
    if (event.isBase64Encoded) {
      rawBody = Buffer.from(rawBody, 'base64').toString('utf-8');
    }
    body = JSON.parse(rawBody);
  } catch (_) {}

  const { url: bodyUrl, token: bodyToken } = body;
  const url = (bodyUrl || process.env.TURSO_DATABASE_URL || '').trim().replace(/^libsql:\/\//, 'https://');
  const token = (bodyUrl ? (bodyToken || '') : (bodyToken || process.env.TURSO_AUTH_TOKEN || '')).replace(/\s+/g, '');

  if (!url || !token) return { statusCode: 500, headers: cors, body: JSON.stringify({ ok: false, error: 'Database configuration missing.' }) };

  try {
    const result = await tursoQuery(url, token, [
      { type: 'execute', stmt: { sql: `CREATE TABLE IF NOT EXISTS meta (id INTEGER PRIMARY KEY, last_modified INTEGER NOT NULL DEFAULT 0)` } },
      { type: 'execute', stmt: { sql: `INSERT OR IGNORE INTO meta (id, last_modified) VALUES (1, 0)` } },
      { type: 'execute', stmt: { sql: `SELECT last_modified FROM meta WHERE id = 1` } }
    ]);
    const ts = result?.results?.[2]?.response?.result?.rows?.[0]?.[0]?.value ?? 0;
    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: true, last_modified: Number(ts) }) };
  } catch (err) {
    return { statusCode: 200, headers: cors, body: JSON.stringify({ ok: false, error: err?.message || 'Poll failed.' }) };
  }
};
