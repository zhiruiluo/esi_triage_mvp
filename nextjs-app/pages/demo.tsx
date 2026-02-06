import { useMemo, useState } from "react";

type SampleCase = {
  id: string;
  esi: number;
  title: string;
  text: string;
  expectedDecision?: string;
};

const SAMPLE_CASES: SampleCase[] = [
  {
    id: "esi1-airway",
    esi: 1,
    title: "Severe respiratory distress",
    text: "70-year-old with severe shortness of breath, cyanosis, SpO2 82%, RR 34. Using accessory muscles.",
    expectedDecision: "ESI-1: immediate life-saving intervention likely needed.",
  },
  {
    id: "esi1-shock",
    esi: 1,
    title: "Hemodynamic shock",
    text: "46-year-old with massive GI bleed, SBP 78, HR 132, altered mental status.",
    expectedDecision: "ESI-1: shock/unstable vitals.",
  },
  {
    id: "esi2-chest",
    esi: 2,
    title: "Chest pain with red flags",
    text: "58-year-old with crushing chest pain radiating to left arm, diaphoretic. BP 160/95, HR 98.",
    expectedDecision: "ESI-2: high-risk chest pain.",
  },
  {
    id: "esi2-ams",
    esi: 2,
    title: "Altered mental status",
    text: "32-year-old found confused and disoriented, vomiting, family reports sudden onset.",
    expectedDecision: "ESI-2: altered mental status.",
  },
  {
    id: "esi3-abd",
    esi: 3,
    title: "Abdominal pain, multiple resources",
    text: "25-year-old with severe abdominal pain, fever 101.8F. Needs labs and CT abdomen.",
    expectedDecision: "ESI-3: stable but 2+ resources.",
  },
  {
    id: "esi3-sob",
    esi: 3,
    title: "SOB, stable vitals",
    text: "40-year-old with shortness of breath, SpO2 94%, RR 22, CXR and labs ordered.",
    expectedDecision: "ESI-3: stable, multiple resources.",
  },
  {
    id: "esi4-lac",
    esi: 4,
    title: "Simple laceration",
    text: "29-year-old with 2 cm finger laceration, bleeding controlled, vitals normal. Needs sutures.",
    expectedDecision: "ESI-4: one resource.",
  },
  {
    id: "esi4-uti",
    esi: 4,
    title: "UTI symptoms",
    text: "52-year-old with dysuria and frequency, no fever, vitals normal. Needs urinalysis.",
    expectedDecision: "ESI-4: one resource.",
  },
  {
    id: "esi5-rx",
    esi: 5,
    title: "Medication refill",
    text: "56-year-old requests blood pressure medication refill, no acute complaints, vitals normal.",
    expectedDecision: "ESI-5: no resources.",
  },
  {
    id: "esi5-tooth",
    esi: 5,
    title: "Toothache",
    text: "40-year-old with toothache, no fever or swelling, just wants pain control.",
    expectedDecision: "ESI-5: no resources.",
  },
];

export default function DemoPage() {
  const [caseText, setCaseText] = useState("");
  const [selectedSample, setSelectedSample] = useState<SampleCase | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const groupedSamples = useMemo(() => {
    return SAMPLE_CASES.reduce<Record<number, SampleCase[]>>((acc, sample) => {
      acc[sample.esi] = acc[sample.esi] || [];
      acc[sample.esi].push(sample);
      return acc;
    }, {});
  }, []);

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
    <div
      style={{
        fontFamily: "system-ui",
        padding: "2rem",
        maxWidth: 1100,
        margin: "0 auto",
        color: "#0f172a",
      }}
    >
      <header style={{ marginBottom: "1.5rem" }}>
        <h1 style={{ fontSize: "2rem", marginBottom: "0.25rem" }}>
          ESI Triage Demo
        </h1>
        <p style={{ color: "#475569", marginTop: 0 }}>
          Pick a sample by ESI level, run classification, and review the key decision signals
          that explain why the model chose the result.
        </p>
      </header>

      <section style={{ marginBottom: "1.5rem" }}>
        <h2 style={{ fontSize: "1.1rem" }}>Sample cases by ESI level</h2>
        <div style={{ display: "grid", gap: "1rem" }}>
          {[1, 2, 3, 4, 5].map((esi) => (
            <div
              key={esi}
              style={{
                background: "#f8fafc",
                border: "1px solid #e2e8f0",
                borderRadius: 12,
                padding: "0.75rem",
              }}
            >
              <strong style={{ display: "block", marginBottom: "0.5rem" }}>ESI-{esi}</strong>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                {(groupedSamples[esi] || []).map((sample) => (
                  <button
                    key={sample.id}
                    onClick={() => {
                      setSelectedSample(sample);
                      setCaseText(sample.text);
                      setResult(null);
                      setError("");
                    }}
                    style={{
                      padding: "0.5rem 0.75rem",
                      borderRadius: 999,
                      border: "1px solid #cbd5f5",
                      background: selectedSample?.id === sample.id ? "#e0e7ff" : "white",
                      cursor: "pointer",
                    }}
                  >
                    {sample.title}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: "1.5rem" }}>
        <div>
          <h2 style={{ fontSize: "1.1rem" }}>Case description</h2>
          <textarea
            value={caseText}
            onChange={(e) => setCaseText(e.target.value)}
            placeholder="Example: 58-year-old with chest pain and shortness of breath..."
            rows={7}
            style={{ width: "100%", padding: "0.75rem", marginBottom: "0.75rem" }}
          />

          {selectedSample?.expectedDecision && (
            <div style={{ color: "#475569", marginBottom: "0.75rem" }}>
              Expected: {selectedSample.expectedDecision}
            </div>
          )}

          <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
            <button onClick={handleClassify} disabled={loading}>
              {loading ? "Classifying..." : "Classify"}
            </button>
            <button
              onClick={() => {
                setCaseText("");
                setSelectedSample(null);
                setResult(null);
                setError("");
              }}
              disabled={loading}
            >
              Clear
            </button>
          </div>

          {error && <div style={{ color: "crimson", marginBottom: "1rem" }}>{error}</div>}
        </div>

        <div
          style={{
            background: "#f1f5f9",
            border: "1px solid #e2e8f0",
            borderRadius: 12,
            padding: "1rem",
          }}
        >
          <h3 style={{ marginTop: 0 }}>What builds trust?</h3>
          <ul style={{ paddingLeft: "1rem", margin: 0, color: "#475569" }}>
            <li>Clear ESI level with confidence score.</li>
            <li>Explicit red-flag detection and vital sign status.</li>
            <li>Resource count and the resources inferred.</li>
            <li>Handbook verification confidence + evidence snippets.</li>
            <li>Model routing choice for high‑risk vs routine cases.</li>
            <li>Cost / token usage transparency.</li>
          </ul>
        </div>
      </section>

      {result && (
        <section
          style={{
            marginTop: "2rem",
            background: "#ffffff",
            border: "1px solid #e2e8f0",
            borderRadius: 16,
            padding: "1.5rem",
            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.05)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap" }}>
            <div>
              <h2 style={{ marginTop: 0 }}>Result: ESI-{result.esi_level}</h2>
              <p style={{ margin: "0.25rem 0" }}>
                Confidence: {(result.confidence * 100).toFixed(1)}%
              </p>
              <p style={{ color: "#475569", marginTop: 0 }}>{result.reason}</p>
            </div>
            <div style={{ textAlign: "right" }}>
              <p style={{ margin: 0, color: "#475569" }}>Estimated cost</p>
              <strong>${Number(result.cost?.estimated_cost_usd || 0).toFixed(4)}</strong>
              <p style={{ margin: "0.5rem 0 0", color: "#475569" }}>
                Remaining today: {result.queries_remaining}
              </p>
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "1rem",
              marginTop: "1rem",
            }}
          >
            <div style={{ background: "#f8fafc", borderRadius: 12, padding: "0.75rem" }}>
              <strong>Red flags</strong>
              <p style={{ margin: "0.25rem 0" }}>
                {result.intermediate?.has_red_flags ? "Detected" : "None"}
              </p>
              {result.intermediate?.red_flags?.length > 0 && (
                <ul style={{ paddingLeft: "1rem", margin: 0 }}>
                  {result.intermediate.red_flags.map((flag: string, index: number) => (
                    <li key={index}>{flag}</li>
                  ))}
                </ul>
              )}
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 12, padding: "0.75rem" }}>
              <strong>Vitals</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Critical: {result.intermediate?.vitals?.critical ? "Yes" : "No"}
              </p>
              <pre style={{ margin: 0, whiteSpace: "pre-wrap", color: "#475569" }}>
                {JSON.stringify(result.intermediate?.vitals?.vitals || {}, null, 2)}
              </pre>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 12, padding: "0.75rem" }}>
              <strong>Resources</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Count: {result.intermediate?.resources?.resource_count ?? 0}
              </p>
              <pre style={{ margin: 0, whiteSpace: "pre-wrap", color: "#475569" }}>
                {JSON.stringify(result.intermediate?.resources?.resources || [], null, 2)}
              </pre>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 12, padding: "0.75rem" }}>
              <strong>Handbook check</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Confidence: {result.intermediate?.handbook_verification?.confidence ?? "n/a"}
              </p>
              <pre style={{ margin: 0, whiteSpace: "pre-wrap", color: "#475569" }}>
                {JSON.stringify(result.intermediate?.handbook_verification?.rag?.evidence || {}, null, 2)}
              </pre>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 12, padding: "0.75rem" }}>
              <strong>Model routing</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Red-flag model: {result.intermediate?.routing?.red_flag_model || "n/a"}
              </p>
              <p style={{ margin: "0.25rem 0" }}>
                Final model: {result.intermediate?.routing?.final_decision_model || "n/a"}
              </p>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
