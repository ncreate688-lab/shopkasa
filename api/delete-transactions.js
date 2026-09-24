import { createClient } from "@libsql/client/web";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { url, token } = req.body;

    if (!url || !token) {
      return res.status(400).json({ error: "Missing database credentials" });
    }

    const db = createClient({ url, authToken: token });

    await db.execute("DELETE FROM mpesa_transactions");

    return res.status(200).json({ ok: true, message: "Transactions deleted" });
  } catch (error) {
    console.error("Error deleting transactions:", error);
    return res.status(500).json({ error: "Failed to delete transactions" });
  }
}
