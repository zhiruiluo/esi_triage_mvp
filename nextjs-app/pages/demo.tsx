import { useState } from "react";

export default function DemoPage() {
  const [caseText, setCaseText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleClassify = async () => {
    if (!caseText.trim()) {
      setError("Please enter a case description.");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await fetch("/api/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_text: caseText }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Classification failed.");
        return;
      }

      setResult(data);
    } catch (err: any) {
      setError(err?.message || "Network error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "system-ui", padding: "2rem", maxWidth: 720, margin: "0 auto" }}>
      <h1>ESI Triage Classifier (MVP)</h1>
      <p>Enter a patient case description to classify red flags (ESI-2).</p>

      <textarea
        value={caseText}
        onChange={(e) => setCaseText(e.target.value)}
        placeholder="Example: 58-year-old with chest pain and shortness of breath..."
        rows={6}
        style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem" }}
      />

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={handleClassify} disabled={loading}>
          {loading ? "Classifying..." : "Classify"}
        </button>
        <button
          onClick={() => {
            setCaseText("");
            setResult(null);
            setError("");
          }}
          disabled={loading}
        >
          Clear
        </button>
      </div>

      {error && <div style={{ color: "crimson", marginBottom: "1rem" }}>{error}</div>}

      {result && (
        <div style={{ background: "#f6f8fa", padding: "1rem", borderRadius: 8 }}>
          <h2>Result: ESI-{result.esi_level}</h2>
          <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          <p>Reason: {result.reason}</p>
          <p>Remaining today: {result.queries_remaining}</p>

          {result.intermediate?.red_flags?.length > 0 && (
            <div>
              <h4>Red flags detected:</h4>
              <ul>
                {result.intermediate.red_flags.map((flag: string, index: number) => (
                  <li key={index}>{flag}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
