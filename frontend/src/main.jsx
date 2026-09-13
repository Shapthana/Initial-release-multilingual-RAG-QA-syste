import React, {useState} from "react";
import {createRoot} from "react-dom/client";
import "./style.css";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  async function ask() {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({query, k:5, use_reranker:false})
      });
      const data = await res.json();
      setAnswer(data.answer || "");
      setSources(data.sources || []);
    } finally { setLoading(false); }
  }

  return <main>
    <h1>Multilingual Document QA</h1>
    <p>English · Sinhala · Tamil</p>
    <textarea value={query} onChange={e=>setQuery(e.target.value)}
      placeholder="Ask a question about your documents..." />
    <button onClick={ask} disabled={!query || loading}>{loading ? "Searching..." : "Ask"}</button>
    <section><h2>Answer</h2><div className="answer">{answer}</div></section>
    <section><h2>Retrieved Sources</h2>{sources.map((s,i)=>
      <article key={s.id || i}><b>{s.source}</b><small> score: {(s.hybrid_score ?? 0).toFixed(3)}</small><p>{s.text}</p></article>
    )}</section>
  </main>
}
createRoot(document.getElementById("root")).render(<App />);
