import Link from "next/link";

export default function Home() {
  return (
    <div
      style={{
        fontFamily: "system-ui",
        padding: "3rem 2rem",
        maxWidth: 960,
        margin: "0 auto",
        color: "#0f172a",
      }}
    >
      <header style={{ marginBottom: "2rem" }}>
        <p style={{ color: "#6366f1", fontWeight: 600, letterSpacing: "0.08em" }}>
          AI TRIAGE ASSISTANT
        </p>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>
          Faster, Safer Triage Decisions with Explainable AI
        </h1>
        <p style={{ color: "#475569", fontSize: "1.1rem", maxWidth: 720 }}>
          We combine clinical guidelines, retrieval-augmented evidence, and cost-efficient AI to
          help clinicians prioritize patients with confidence—transparent signals, auditable
          reasoning, and lower operational load.
        </p>
      </header>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        {[
          "Evidence-backed ESI recommendations in seconds",
          "Clear signals: vitals, red flags, resources, guideline citations",
          "Smart routing to keep costs low without sacrificing accuracy",
          "Built for clinical workflows and auditability",
        ].map((item) => (
          <div
            key={item}
            style={{
              background: "#f8fafc",
              border: "1px solid #e2e8f0",
              borderRadius: 12,
              padding: "1rem",
              minHeight: 110,
            }}
          >
            <strong style={{ display: "block" }}>{item}</strong>
          </div>
        ))}
      </section>

      <section
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          alignItems: "center",
        }}
      >
        <Link
          href="/demo"
          style={{
            padding: "0.75rem 1.5rem",
            background: "#4f46e5",
            color: "white",
            borderRadius: 999,
            textDecoration: "none",
            fontWeight: 600,
          }}
        >
          Open Demo
        </Link>
        <span style={{ color: "#64748b" }}>Explore sample cases and trust signals.</span>
      </section>
    </div>
  );
}
