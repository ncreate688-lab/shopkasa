import fs from 'fs';

const url = 'https://pos-business-success.aws-ap-northeast-1.turso.io/v2/pipeline';
const token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODI2MDY1NzUsImlkIjoiMDE5ZjBiYTEtOTgwMS03NmIxLWFmNzktZDY4OTYxMjViODZmIiwicmlkIjoiN2ZhNGZmMDctOGFjYy00Y2QwLWFhMTAtMWUyODBjMzUzODU0In0.2aZaazbaKWyB2FbgKUiIDGb6G_v4Yqw8EdTgjJr9v-DWUCckA8gWgF1uuL_BjhQtptKKVvj-As2UsklApcFmDA';

const payload = {
  "requests": [
    {
      "type": "execute",
      "stmt": {
        "sql": "SELECT id, transaction_code, amount, sender FROM mpesa_transactions ORDER BY timestamp DESC LIMIT 1"
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
}).then(r => r.json()).then(res => {
  console.log(JSON.stringify(res, null, 2));
}).catch(console.error);
