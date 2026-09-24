import { createClient } from '@libsql/client/web';
const url = 'https://pos-business-success.aws-ap-northeast-1.turso.io';
const token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODI2MDY1NzUsImlkIjoiMDE5ZjBiYTEtOTgwMS03NmIxLWFmNzktZDY4OTYxMjViODZmIiwicmlkIjoiN2ZhNGZmMDctOGFjYy00Y2QwLWFhMTAtMWUyODBjMzUzODU0In0.2aZaazbaKWyB2FbgKUiIDGb6G_v4Yqw8EdTgjJr9v-DWUCckA8gWgF1uuL_BjhQtptKKVvj-As2UsklApcFmDA';

const client = createClient({ url, authToken: token });

async function run() {
  try {
    const res = await client.execute('SELECT * FROM mpesa_transactions');
    console.log("MPESA Transactions:", res.rows);
  } catch (err) {
    console.error("Error reading from Turso:", err.message);
  }
}

run();
