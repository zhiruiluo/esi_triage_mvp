import Link from "next/link";
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
    id: "esi1-mastitis",
    esi: 1,
    title: "Postpartum fever and breast pain",
    text: "“My right breast is so sore, my nipples are cracked, and now I have a fever. Do you think I will have to stop nursing my baby?” asks a tearful postpartum patient.",
    expectedDecision: "ESI-1: immediate life-saving intervention required.",
  },
  {
    id: "esi1-sah",
    esi: 1,
    title: "Sudden severe headache",
    text: "26-year-old female is transported by EMS to the ED because she experienced the sudden onset of a severe headache that began after she moved.",
    expectedDecision: "ESI-1: immediate life-saving intervention required.",
  },
  {
    id: "esi2-sob",
    esi: 2,
    title: "Shortness of breath",
    text: "A 32-year-old female presents to the emergency department complaining of shortness of breath for several hours. No past medical history, +smoker.",
    expectedDecision: "ESI-2: high risk.",
  },
  {
    id: "esi2-warfarin-fall",
    esi: 2,
    title: "Elderly fall on warfarin",
    text: "EMS arrives with an 87-year-old male who fell and hit his head. He is awake, alert, and oriented and remembers the fall. He has a past medical history of atrial fibrillation and takes warfarin.",
    expectedDecision: "ESI-2: high risk due to anticoagulation.",
  },
  {
    id: "esi3-bike-accident",
    esi: 3,
    title: "Bike accident with laceration",
    text: "A 41-year-old male involved in a bicycle accident walks into the emergency department with his right arm in a sling. He fell off his bike and landed on his right arm. He has pain in the wrist and a 2-centimeter laceration on his left elbow.",
    expectedDecision: "ESI-3: two or more resources.",
  },
  {
    id: "esi3-foot-infection",
    esi: 3,
    title: "Swollen painful foot",
    text: "A 60-year-old man requests to see a doctor because his right foot hurts. The great toe and foot skin are red, warm, swollen, and tender.",
    expectedDecision: "ESI-3: two or more resources.",
  },
  {
    id: "esi4-uti",
    esi: 4,
    title: "UTI symptoms",
    text: "A 52-year-old female requests to see a doctor for a possible urinary tract infection (UTI). She is complaining of dysuria and frequency.",
    expectedDecision: "ESI-4: one resource.",
  },
  {
    id: "esi4-dysuria",
    esi: 4,
    title: "Dysuria without fever",
    text: "“It hurts so much when I urinate,” reports an otherwise healthy 25-year-old. She denies fever, chills, abdominal pain, or vaginal discharge.",
    expectedDecision: "ESI-4: one resource.",
  },
  {
    id: "esi5-refill",
    esi: 5,
    title: "Medication refill",
    text: "“I ran out of my blood pressure medicine, and my doctor is on vacation. Can someone here write me a prescription?” requests a 56-year-old male with a history of HTN. Vital signs: BP 128/84, HR 76, RR 16, T 97˚F.",
    expectedDecision: "ESI-5: no resources.",
  },
  {
    id: "esi5-pain-refill",
    esi: 5,
    title: "Pain medication refill",
    text: "“I just need another prescription for pain medication. I was here 10 days ago and ran out,” a 27-year-old male tells you. “I hurt my back at work.”",
    expectedDecision: "ESI-5: no resources.",
  },
];

export default function DemoPage() {
  const [caseText, setCaseText] = useState("");
  const [selectedSample, setSelectedSample] = useState<SampleCase | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [modelChoice, setModelChoice] = useState("auto");

  const vitalsLabelMap: Record<string, string> = {
    hr: "Heart rate",
    rr: "Respiratory rate",
    sbp: "Systolic BP",
    dbp: "Diastolic BP",
    temp_f: "Temperature (F)",
    spo2: "Oxygen saturation",
  };

  const resourceLabelMap: Record<string, string> = {
    CXR: "Chest X-ray",
    CBC: "Complete blood count",
    ECG: "Electrocardiogram",
    Troponin: "Troponin lab",
    CMP: "Metabolic panel",
    "CT Abdomen": "CT abdomen",
    Sutures: "Suture repair",
    "X-ray": "X-ray",
  };

  const vitalsRangeByAge = (age?: number | null): Record<string, string> => {
    if (age !== undefined && age !== null && age < 1) {
      return {
        hr: "100–160 bpm",
        rr: "30–60 /min",
        sbp: "70–100 mmHg",
        dbp: "50–65 mmHg",
        temp_f: "97.0–99.5 °F",
        spo2: "95–100%",
      };
    }
    if (age !== undefined && age !== null && age < 12) {
      return {
        hr: "70–120 bpm",
        rr: "18–30 /min",
        sbp: "80–110 mmHg",
        dbp: "55–75 mmHg",
        temp_f: "97.0–99.5 °F",
        spo2: "95–100%",
      };
    }
    return {
      hr: "60–100 bpm",
      rr: "12–20 /min",
      sbp: "90–120 mmHg",
      dbp: "60–80 mmHg",
      temp_f: "97.0–99.0 °F",
      spo2: "95–100%",
    };
  };

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
        body: JSON.stringify({ case_text: caseText, model: modelChoice }),
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
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
        background: "#f8fafc",
        color: "#0f172a",
        minHeight: "100vh",
      }}
    >
      <div style={{ maxWidth: 1120, margin: "0 auto", padding: "2rem 1.75rem 3rem" }}>
      <nav
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1.5rem",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              background: "linear-gradient(135deg, #2563eb, #0ea5e9)",
              color: "white",
              display: "grid",
              placeItems: "center",
              fontWeight: 700,
            }}
          >
            ESI
          </div>
          <div>
            <strong style={{ fontSize: "1.05rem" }}>ESI Triage</strong>
            <div style={{ color: "#64748b", fontSize: "0.85rem" }}>Clinical demo</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: "0.75rem" }}>
          {[
            { href: "/", label: "Home" },
            { href: "/demo", label: "Demo" },
            { href: "/admin", label: "Admin" },
          ].map((item) => (
            <Link
              key={item.href}
              href={item.href}
              style={{
                textDecoration: "none",
                color: "#0f172a",
                padding: "0.35rem 0.75rem",
                borderRadius: 999,
                border: "1px solid #e2e8f0",
                background: "white",
                fontSize: "0.95rem",
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>

      <header
        style={{
          marginBottom: "1.5rem",
          background: "white",
          border: "1px solid #e2e8f0",
          borderRadius: 18,
          padding: "1.75rem",
          boxShadow: "0 12px 30px rgba(15, 23, 42, 0.06)",
        }}
      >
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
                background: "white",
                border: "1px solid #e2e8f0",
                borderRadius: 16,
                padding: "0.85rem",
                boxShadow: "0 8px 20px rgba(15, 23, 42, 0.05)",
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
                      background: selectedSample?.id === sample.id ? "#e0f2fe" : "white",
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
            style={{
              width: "100%",
              padding: "0.75rem",
              marginBottom: "0.75rem",
              borderRadius: 12,
              border: "1px solid #cbd5f5",
              background: "white",
            }}
          />

          {selectedSample?.expectedDecision && (
            <div style={{ color: "#475569", marginBottom: "0.75rem" }}>
              Expected: {selectedSample.expectedDecision}
            </div>
          )}

          <div style={{ display: "flex", gap: "0.75rem", marginBottom: "1rem", flexWrap: "wrap" }}>
            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem" }}>
              <span style={{ color: "#475569", fontSize: "0.9rem" }}>Model</span>
              <select
                value={modelChoice}
                onChange={(e) => setModelChoice(e.target.value)}
                style={{
                  padding: "0.5rem",
                  borderRadius: 10,
                  border: "1px solid #cbd5f5",
                  background: "white",
                }}
              >
                <option value="auto">Auto (smart routing)</option>
                <option value="gpt-4-turbo">gpt-4-turbo</option>
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini">gpt-4o-mini</option>
                <option value="gpt-4">gpt-4</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              </select>
            </label>
            <button
              onClick={handleClassify}
              disabled={loading}
              style={{
                padding: "0.6rem 1.25rem",
                borderRadius: 999,
                border: "none",
                background: "#2563eb",
                color: "white",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
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
              style={{
                padding: "0.6rem 1.25rem",
                borderRadius: 999,
                border: "1px solid #cbd5f5",
                background: "white",
                color: "#0f172a",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              Clear
            </button>
          </div>

          {error && <div style={{ color: "crimson", marginBottom: "1rem" }}>{error}</div>}
        </div>

        <div
          style={{
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 16,
            padding: "1.25rem",
            boxShadow: "0 10px 24px rgba(15, 23, 42, 0.05)",
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
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 20,
            padding: "1.75rem",
            boxShadow: "0 16px 36px rgba(15, 23, 42, 0.08)",
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
            <div style={{ background: "#f8fafc", borderRadius: 14, padding: "0.9rem" }}>
              <strong>Cost breakdown</strong>
              <div style={{ color: "#475569", display: "grid", gap: "0.35rem" }}>
                <div>
                  Red-flag layer: ${Number(result.intermediate?.layer_costs?.red_flag || 0).toFixed(4)}
                </div>
                <div>
                  Vitals layer: ${Number(result.intermediate?.layer_costs?.vitals || 0).toFixed(4)}
                </div>
                <div>
                  Resources layer: ${Number(result.intermediate?.layer_costs?.resources || 0).toFixed(4)}
                </div>
                <div>
                  Handbook layer: ${Number(result.intermediate?.layer_costs?.handbook || 0).toFixed(4)}
                </div>
                <div>
                  Final decision: ${Number(result.intermediate?.layer_costs?.final_decision || 0).toFixed(4)}
                </div>
                <div style={{ marginTop: "0.25rem", color: "#0f172a" }}>
                  Total: ${Number(result.cost?.estimated_cost_usd || 0).toFixed(4)}
                </div>
              </div>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 14, padding: "0.9rem" }}>
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

            <div style={{ background: "#f8fafc", borderRadius: 14, padding: "0.9rem" }}>
              <strong>Vitals</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Vitals Critical: {result.intermediate?.vitals?.critical ? "Yes" : "No"}
              </p>
              <div style={{ display: "grid", gap: "0.5rem", color: "#475569" }}>
                {Object.entries(result.intermediate?.vitals?.vitals || {}).length === 0 && (
                  <span>No vitals extracted.</span>
                )}
                {Object.entries(
                  result.intermediate?.vitals?.vitals || {}
                ).map(([key, value]) => (
                    <div key={key}>
                      <strong style={{ color: "#0f172a" }}>
                        {vitalsLabelMap[key] || key}
                      </strong>
                      : {String(value)}
                      <span style={{ color: "#94a3b8" }}>
                        {" "}· Typical range {vitalsRangeByAge(result.intermediate?.extraction?.age)[key] || "n/a"}
                      </span>
                    </div>
                  )
                )}
              </div>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 14, padding: "0.9rem" }}>
              <strong>Resources</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Count: {result.intermediate?.resources?.resource_count ?? 0}
              </p>
              <div style={{ display: "grid", gap: "0.4rem", color: "#475569" }}>
                {(result.intermediate?.resources?.resources || []).length === 0 && (
                  <span>No resources inferred.</span>
                )}
                {(result.intermediate?.resources?.resources || []).map(
                  (item: string, index: number) => (
                    <div key={`${item}-${index}`}>
                      <strong style={{ color: "#0f172a" }}>
                        {resourceLabelMap[item] || item}
                      </strong>
                      {resourceLabelMap[item] ? ` (${item})` : ""}
                    </div>
                  )
                )}
              </div>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 14, padding: "0.9rem" }}>
              <strong>Handbook check</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Confidence: {result.intermediate?.handbook_verification?.confidence ?? "n/a"}
              </p>
              <pre style={{ margin: 0, whiteSpace: "pre-wrap", color: "#475569" }}>
                {JSON.stringify(result.intermediate?.handbook_verification?.rag?.evidence || {}, null, 2)}
              </pre>
            </div>

            <div style={{ background: "#f8fafc", borderRadius: 14, padding: "0.9rem" }}>
              <strong>Model routing</strong>
              <p style={{ margin: "0.25rem 0" }}>
                Mode: {result.intermediate?.routing?.mode || "auto"}
              </p>
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
    </div>
  );
}
