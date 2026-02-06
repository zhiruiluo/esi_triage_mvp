import Link from "next/link";

export default function Home() {
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
            marginBottom: "2rem",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
            <div
              style={{
                width: 38,
                height: 38,
                borderRadius: 12,
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
              <strong style={{ fontSize: "1.1rem" }}>ESI Triage</strong>
              <div style={{ color: "#64748b", fontSize: "0.85rem" }}>
                Clinical decision support
              </div>
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
            marginBottom: "2rem",
            padding: "2.5rem",
            borderRadius: 20,
            background: "white",
            border: "1px solid #e2e8f0",
            boxShadow: "0 20px 60px rgba(15, 23, 42, 0.08)",
          }}
        >
          <p style={{ color: "#2563eb", fontWeight: 600, letterSpacing: "0.12em" }}>
            AI TRIAGE ASSISTANT
          </p>
          <h1 style={{ fontSize: "2.6rem", marginBottom: "0.75rem" }}>
            Faster, Safer Triage Decisions with Explainable AI
          </h1>
          <p style={{ color: "#475569", fontSize: "1.05rem", maxWidth: 720 }}>
            We combine clinical guidelines, retrieval-augmented evidence, and cost-efficient AI to
            help clinicians prioritize patients with confidence—transparent signals, auditable
            reasoning, and lower operational load.
          </p>
          <div style={{ display: "flex", gap: "1rem", marginTop: "1.5rem" }}>
            <Link
              href="/demo"
              style={{
                padding: "0.75rem 1.5rem",
                background: "#2563eb",
                color: "white",
                borderRadius: 999,
                textDecoration: "none",
                fontWeight: 600,
              }}
            >
              Open Demo
            </Link>
            <span style={{ alignSelf: "center", color: "#64748b" }}>
              Explore sample cases and trust signals.
            </span>
          </div>
        </header>

        <section
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "1rem",
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
                background: "white",
                border: "1px solid #e2e8f0",
                borderRadius: 16,
                padding: "1.25rem",
                minHeight: 120,
                boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
              }}
            >
              <strong style={{ display: "block" }}>{item}</strong>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
