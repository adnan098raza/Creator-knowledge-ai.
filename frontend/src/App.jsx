import { ArrowDown, ArrowUp, AudioLines, Check, ChevronDown, ChevronRight, Copy, FileText, Menu, Search, Send, Sparkles, X, Zap } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import GeometricLoader from "./GeometricLoader";
import { useEffect, useMemo, useState } from "react";
import "./App.css";

const prompts = [
  ["Summarize this episode", Sparkles],
  ["What are the key takeaways?", Zap],
  ["What did they say about Taiwan?", Search],
  ["Explain the economic implications", AudioLines],
];

const time = (v) => {
  const n = Math.max(0, Math.floor(Number(v) || 0));
  return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, "0")}`;
};

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [menu, setMenu] = useState(false);
  const [theme, setTheme] = useState(() => {
    try { return localStorage.getItem("signal-theme") || "dark"; }
    catch { return "dark"; }
  });
  const [sourcesOpen, setSourcesOpen] = useState(true);
  const [copied, setCopied] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const updateScroll = () => {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      setScrollProgress(
        maxScroll > 0 ? Math.min(1, Math.max(0, window.scrollY / maxScroll)) : 0
      );
    };
    window.addEventListener("scroll", updateScroll, { passive: true });
    window.addEventListener("resize", updateScroll);
    updateScroll();
    return () => {
      window.removeEventListener("scroll", updateScroll);
      window.removeEventListener("resize", updateScroll);
    };
  }, []);

  const paragraphs = useMemo(
    () => answer.split(/\n{2,}|\n(?=•|- |\d+\.)/).map((x) => x.trim()).filter(Boolean),
    [answer]
  );

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try { localStorage.setItem("signal-theme", next); } catch { /* storage may be unavailable */ }
  }

  async function ask(value = question) {
    const q = value.trim();
    if (!q || loading) return;
    setQuestion(q); setLoading(true); setError("");
    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      if (!response.ok) throw new Error(`Request failed (${response.status})`);
      const data = await response.json();
      setAnswer(typeof data.answer === "string" ? data.answer : "The backend returned no answer.");
      setSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (e) {
      console.error(e); setAnswer(""); setSources([]);
      setError("I couldn't reach the backend. Make sure FastAPI is running at http://127.0.0.1:8000, then try again.");
    } finally { setLoading(false); }
  }

  async function copyAnswer() {
    try {
      await navigator.clipboard.writeText(answer);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      setError("Copy failed. Please select the answer and copy it manually.");
    }
  }

  return (
    <div className={`signal-app theme-${theme}`}>
      <header className="top-nav">
        <a className="brand" href="#top">
          <span className="brand-mark"><AudioLines size={19} /></span>
          <span className="brand-copy"><strong>SIGNAL<span>.</span></strong><small>PODCAST INTELLIGENCE</small></span>
        </a>
        <nav className={menu ? "nav-links open" : "nav-links"}>
          <a href="#ask" onClick={() => setMenu(false)}>Explore</a>
          <a href="#answer" onClick={() => setMenu(false)}>Answers</a>
          <a href="#sources" onClick={() => setMenu(false)}>Sources</a>
        </nav>
        <div className="nav-actions">
          <span className="status-pill"><i /> KNOWLEDGE ENGINE READY</span>
          
          <a className="nav-cta" href="#ask">Ask a question <ArrowDown size={15} /></a>
          <button className="menu-button" onClick={() => setMenu(!menu)} aria-label="Toggle menu">{menu ? <X size={20} /> : <Menu size={20} />}</button>
        </div>
      </header>

      <main id="top">
        <section className="hero-section">
          <div
            className="studio-backdrop"
            style={{
              "--studio-blur": `${Math.min(scrollProgress * 8, 8)}px`,
            }}
            aria-hidden="true"
          />
          <div className="hero-grid" />
          <div className="hero-topline">
            <span className="hero-topline-left"><i /> LISTEN CLOSER <b>·</b> YOUR PODCAST. DECODED.</span>
            <span>IDEAS IN. INSIGHT OUT.</span>
          </div>
          <div className="hero-copy">
            <motion.p className="hero-subtitle" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0, transition: { delay: 0.12 } }}>
              Ask the conversation anything. Get grounded answers, discover key ideas, and trace every insight back to its source.
            </motion.p>
            <motion.h1 initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
              THINK DEEPER.<br /><span>FIND THE SIGNAL.</span>
            </motion.h1>
            
          </div>
          <div className="lens-stage">
            <div className="lens-aura" />
            <GeometricLoader />
            <span className="lens-label top">WITT</span>
            <span className="lens-label left">DUE DILIGENCE</span>
            <span className="lens-label right">INNOVATION</span>
            <span className="orbit orbit-a" />
            <span className="orbit orbit-b" />
          </div>
          <div className="hero-bottomline" aria-hidden="true" />
        </section>

        <section className="ask-section" id="ask">

          <div className="kicker conversation-cta">
            <span>01</span> START A CONVERSATION
          </div>


          <div className="section-heading">
            <div>
              <h2>WHAT DO YOU WANT<br />TO <em>UNDERSTAND?</em></h2>
              <p>Ask a specific question or start with a prompt below.</p>
            </div>
            <span className="side-note"><AudioLines size={16} /> GROUNDED IN YOUR EPISODE</span>
          </div>

          <form className="composer" onSubmit={(e) => { e.preventDefault(); ask(); }}>
            <div className="composer-main">
              <Sparkles size={18} />
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ask(); } }}
                placeholder="Ask about an idea, argument, person, or moment in the episode…"
                rows={2}
                aria-label="Ask a podcast question"
              />
            </div>
            <div className="composer-footer">
              <span><i /> Answers include supporting transcript sources</span>
              <button className="send-button" disabled={loading || !question.trim()}>
                {loading ? <span className="spinner" /> : <>Ask Signal <ArrowUp size={17} /></>}
              </button>
            </div>
          </form>

          <div className="prompt-grid">
            {prompts.map(([label, Icon], i) => (
              <motion.button
                className="prompt-chip"
                key={label}
                onClick={() => { setQuestion(label); document.querySelector(".composer textarea")?.focus(); }}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
              >
                <Icon size={16} /><span>{label}</span><ArrowUp size={13} />
              </motion.button>
            ))}
          </div>

          {error && <div className="error-banner" role="alert">{error}</div>}
        </section>

        <AnimatePresence>
          {(answer || loading) && (
            <motion.section className="answer-section" id="answer" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <div className="kicker"><span>02</span> THE RESPONSE</div>
              <div className="section-heading answer-heading">
                <div>
                  <div className="answer-label"><Sparkles size={15} /> SIGNAL / AI ANALYSIS</div>
                  <h2>HERE’S THE <em>SIGNAL.</em></h2>
                </div>
                {answer && (
                  <button className="copy-button" onClick={copyAnswer}>
                    {copied ? <Check size={15} /> : <Copy size={15} />} {copied ? "Copied" : "Copy answer"}
                  </button>
                )}
              </div>

              <div className="answer-layout">
                <article className="answer-panel">
                  {loading ? (
                    <div className="loading-state">
                      <span className="spinner big" />
                      <div>
                        <strong>Searching the conversation</strong>
                        <p>Finding relevant passages and assembling an answer…</p>
                      </div>
                    </div>
                  ) : (
                    <div className="answer-body">{paragraphs.map((p, i) => <p key={i}>{p}</p>)}</div>
                  )}
                  <div className="answer-foot">
                    <span><i /> {sources.length} supporting source{sources.length === 1 ? "" : "s"} returned</span>
                    <span>AI-GENERATED · VERIFY WITH SOURCES</span>
                  </div>
                </article>

                <aside className="evidence-panel" id="sources">
                  <button className="evidence-head" onClick={() => setSourcesOpen(!sourcesOpen)}>
                    <span><FileText size={16} /> EVIDENCE <b>{sources.length}</b></span>
                    <ChevronDown size={16} className={sourcesOpen ? "" : "closed"} />
                  </button>
                  <AnimatePresence initial={false}>
                    {sourcesOpen && (
                      <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="source-list">
                        {sources.length ? sources.map((s, i) => {
                          const id = s.chunk_index ?? s.part_index ?? i + 1;
                          const start = s.start_time ?? s.start ?? 0;
                          const end = s.end_time ?? s.end ?? 0;
                          const text = s.english_text ?? s.text ?? s.original_text ?? s.content ?? "";
                          return (
                            <div className="source-item" key={`${id}-${start}-${i}`}>
                              <div className="source-meta">
                                <span>SOURCE {String(i + 1).padStart(2, "0")}</span>
                                <time>{time(start)} — {time(end)}</time>
                              </div>
                              <strong>Passage {id}</strong>
                              {text && <p>{text}</p>}
                              <div className="source-bottom"><span><i /> TRANSCRIPT MATCH</span><ChevronRight size={15} /></div>
                            </div>
                          );
                        }) : (
                          <div className="empty-sources">Supporting transcript passages will appear here when the backend returns sources.</div>
                        )}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </aside>
              </div>
            </motion.section>
          )}
        </AnimatePresence>
      </main>

      <footer className="site-footer">
        <a className="brand" href="#top">
          <span className="brand-mark"><AudioLines size={18} /></span>
          <span className="brand-copy"><strong>SIGNAL<span>.</span></strong><small>PODCAST INTELLIGENCE</small></span>
        </a>
        <span>LESS NOISE. MORE MEANING.</span>
        <a href="#top" className="back-top">BACK TO TOP <ArrowUp size={14} /></a>
      </footer>
    </div>
  );
}
