import { createClient } from '@libsql/client/web';
const url = 'https://pos-business-success.aws-ap-northeast-1.turso.io';
const token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODI2MDY1NzUsImlkIjoiMDE5ZjBiYTEtOTgwMS03NmIxLWFmNzktZDY4OTYxMjViODZmIiwicmlkIjoiN2ZhNGZmMDctOGFjYy00Y2QwLWFhMTAtMWUyODBjMzUzODU0In0.2aZaazbaKWyB2FbgKUiIDGb6G_v4Yqw8EdTgjJr9v-DWUCckA8gWgF1uuL_BjhQtptKKVvj-As2UsklApcFmDA';

const client = createClient({ url, authToken: token });

async function run() {
  try {
    await client.execute(`CREATE TABLE IF NOT EXISTS mpesa_transactions (id TEXT PRIMARY KEY, transaction_code TEXT, amount REAL, sender TEXT, phone TEXT, timestamp TEXT, status TEXT DEFAULT 'pending')`);
    console.log("Table created.");
  } catch (err) {
    console.error("Error:", err.message);
  }
}
run();
