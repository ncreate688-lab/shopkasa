const url = 'https://pos-business-success.aws-ap-northeast-1.turso.io/v2/pipeline';
const token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODI2MDY1NzUsImlkIjoiMDE5ZjBiYTEtOTgwMS03NmIxLWFmNzktZDY4OTYxMjViODZmIiwicmlkIjoiN2ZhNGZmMDctOGFjYy00Y2QwLWFhMTAtMWUyODBjMzUzODU0In0.2aZaazbaKWyB2FbgKUiIDGb6G_v4Yqw8EdTgjJr9v-DWUCckA8gWgF1uuL_BjhQtptKKVvj-As2UsklApcFmDA';

const payload = {
  "requests": [
    {
      "type": "execute",
      "stmt": {
        "sql": "CREATE TABLE IF NOT EXISTS mpesa_transactions (id TEXT PRIMARY KEY, transaction_code TEXT, amount REAL, sender TEXT, phone TEXT, timestamp TEXT, status TEXT DEFAULT 'pending')"
      }
    },
    {
      "type": "execute",
      "stmt": {
        "sql": "INSERT INTO mpesa_transactions (id, transaction_code, amount, sender, phone, timestamp, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        "args": [
          {"type": "text", "value": "test-1"},
          {"type": "text", "value": "UGE2A00EV7"},
          {"type": "float", "value": 1.0},
          {"type": "text", "value": "ZIPPORAH MURUNGA"},
          {"type": "text", "value": "0701***580"},
          {"type": "text", "value": "2026-07-14T12:24:00Z"},
          {"type": "text", "value": "pending"}
        ]
      }
    }
  ]
};

fetch(url, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
}).then(r => r.json()).then(console.log).catch(console.error);
