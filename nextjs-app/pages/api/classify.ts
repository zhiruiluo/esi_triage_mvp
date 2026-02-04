import type { NextApiRequest, NextApiResponse } from "next";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { case_text } = req.body || {};

  if (!case_text) {
    return res.status(400).json({ error: "case_text is required" });
  }

  try {
    const response = await fetch(`${API_URL}/classify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ case_text }),
    });

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (err: any) {
    return res.status(500).json({ error: err?.message || "API error" });
  }
}
