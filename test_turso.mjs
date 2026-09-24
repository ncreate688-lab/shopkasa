import { createClient } from '@libsql/client/web';
import fs from 'fs';

const url = 'https://pos-business-success.aws-ap-northeast-1.turso.io';
const token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODI2MDY1NzUsImlkIjoiMDE5ZjBiYTEtOTgwMS03NmIxLWFmNzktZDY4OTYxMjViODZmIiwicmlkIjoiN2ZhNGZmMDctOGFjYy00Y2QwLWFhMTAtMWUyODBjMzUzODU0In0.2aZaazbaKWyB2FbgKUiIDGb6G_v4Yqw8EdTgjJr9v-DWUCckA8gWgF1uuL_BjhQtptKKVvj-As2UsklApcFmDA';

const client = createClient({ url, authToken: token });

async function run() {
  const products = [];
  for (let i = 0; i < 180; i++) {
    products.push({
      id: `prod-${i}`,
      name: `Product ${i}`,
      price: 10 + i,
      costPrice: 5 + i,
      barcode: `1000${i}`,
      expiryDate: '2027-01-01',
      quantity: 50,
      category: 'Test',
      full_json: JSON.stringify({ dummy: 'data' })
    });
  }

  const key = 'products';
  const tableConfigs = {
    products: { cols: ['id', 'name', 'price', 'costPrice', 'barcode', 'expiryDate', 'quantity', 'category', 'full_json'], getArgs: (item, id) => [id, item.name||'', item.price||0, item.costPrice||0, item.barcode||'', item.expiryDate||'', item.quantity||0, item.category||'', JSON.stringify(item)] },
  };

  const config = tableConfigs[key];
  const stmts = [];
  stmts.push({ sql: `DELETE FROM ${key}`, args: [] });

  const BATCH_SIZE = 40;
  for (let i = 0; i < products.length; i += BATCH_SIZE) {
    const chunk = products.slice(i, i + BATCH_SIZE);
    const placeholders = chunk.map(() => `(${config.cols.map(() => '?').join(', ')})`).join(', ');
    const args = [];
    chunk.forEach((item, idx) => {
      const id = String(item.id || item.date || (i + idx));
      args.push(...config.getArgs(item, id));
    });
    stmts.push({
      sql: `INSERT INTO ${key} (${config.cols.join(', ')}) VALUES ${placeholders}`,
      args
    });
  }

  console.log(`Sending ${stmts.length} statements...`);
  try {
    const res = await client.batch(stmts, 'write');
    console.log("Success!", res.length);
  } catch (err) {
    console.error("Failed:", err.message);
  }
}

run();
