import Link from "next/link";

export default function Home() {
  return (
    <div style={{ fontFamily: "system-ui", padding: "2rem" }}>
      <h1>ESI Triage Classifier</h1>
      <p>Go to the demo page to classify cases.</p>
      <Link href="/demo">Open Demo</Link>
    </div>
  );
}
