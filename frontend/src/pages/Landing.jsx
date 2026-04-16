import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import {
  FiCpu, FiShield, FiZap, FiLayers, FiGitBranch,
  FiSearch, FiMessageSquare, FiUploadCloud, FiGithub,
  FiLinkedin, FiBookOpen, FiGlobe, FiArrowRight, FiCheck,
  FiFileText, FiDatabase, FiLock, FiHash, FiGrid, FiActivity
} from 'react-icons/fi'

const GOOGLE_AUTH_URL = '/auth/login'

/* Google "G" logo SVG — actual brand icon */
function GoogleLogo({ size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
    </svg>
  )
}

function TypewriterCodeBlock() {
  const [displayText, setDisplayText] = useState('');
  const codeText = `from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "invincibleambuj/llama-3.2-1b-legal-india-qlora",
    load_in_4bit = True,
)

inputs = tokenizer(
    "### Instruction:\\nWhat is IPC Section 302?\\n\\n### Response:\\n",
    return_tensors="pt"
)

outputs = model.generate(**inputs, max_new_tokens=200, repetition_penalty=1.3)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))`;

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setDisplayText(codeText.slice(0, index));
      index++;
      if (index > codeText.length) clearInterval(interval);
    }, 12);
    return () => clearInterval(interval);
  }, [codeText]);

  const highlightCode = (code) => {
    return code
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/(".*?")/g, '<span style="color: #a5d6ff">$1</span>')
      .replace(/\b(from|import|True|return_tensors|max_new_tokens|repetition_penalty|skip_special_tokens)\b/g, '<span style="color: #ff7b72">$1</span>')
      .replace(/\b(FastLanguageModel|model|tokenizer|inputs|outputs)\b/g, '<span style="color: #79c0ff">$1</span>')
      .replace(/\b(print)\b/g, '<span style="color: #d2a8ff">$1</span>');
  };

  return (
    <pre style={{ margin: '0', padding: '24px', fontFamily: "'JetBrains Mono', monospace", fontSize: '12px', lineHeight: '1.8', color: '#888', overflowX: 'auto', minHeight: '340px' }} dangerouslySetInnerHTML={{ __html: highlightCode(displayText) }}></pre>
  );
}

function AnimatedNumber({ end, suffix = '', duration = 2000 }) {
  const [count, setCount] = useState(0)
  const nodeRef = useRef(null)
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          let startTimestamp = null
          const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp
            const progress = Math.min((timestamp - startTimestamp) / duration, 1)
            const easeOutQuart = 1 - Math.pow(1 - progress, 4)
            setCount(Math.floor(easeOutQuart * end))
            if (progress < 1) window.requestAnimationFrame(step)
          }
          window.requestAnimationFrame(step)
          observer.disconnect()
        }
      },
      { threshold: 0.1 }
    )
    if (nodeRef.current) observer.observe(nodeRef.current)
    return () => observer.disconnect()
  }, [end, duration])

  return <span ref={nodeRef}>{count.toLocaleString()}{suffix}</span>
}

export default function Landing() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [docsOpen, setDocsOpen] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  if (user) {
    navigate('/chat', { replace: true })
    return null
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
      {/* ===== STATUS BADGE ANIMATIONS ===== */}
      <style>{`
        @keyframes sonar-ping { 0% { transform: scale(1); opacity: 0.8; } 70% { transform: scale(3.5); opacity: 0; } 100% { transform: scale(3.5); opacity: 0; } }
        @keyframes shimmer-sweep { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
        @keyframes ecg-draw { 0% { stroke-dashoffset: 60; } 100% { stroke-dashoffset: -60; } }
        @keyframes red-heartbeat-glow {
          0%   { box-shadow: 0 0 0px rgba(185, 28, 28, 0); border-color: rgba(255, 255, 255, 0.1); }
          30%  { box-shadow: 0 0 0px rgba(185, 28, 28, 0); border-color: rgba(255, 255, 255, 0.1); }
          40%  { box-shadow: 0 0 25px rgba(185, 28, 28, 0.8), inset 0 0 8px rgba(153, 27, 27, 0.4); border-color: rgba(185, 28, 28, 0.9); }
          45%  { box-shadow: 0 0 8px rgba(185, 28, 28, 0.3); border-color: rgba(185, 28, 28, 0.4); }
          55%  { box-shadow: 0 0 40px rgba(153, 27, 27, 1), inset 0 0 15px rgba(153, 27, 27, 0.8); border-color: #dc2626; }
          70%  { box-shadow: 0 0 0px rgba(185, 28, 28, 0); border-color: rgba(255, 255, 255, 0.1); }
          100% { box-shadow: 0 0 0px rgba(185, 28, 28, 0); border-color: rgba(255, 255, 255, 0.1); }
        }
        .afp-status-badge {
          display: inline-flex; align-items: center; gap: 6px;
          margin-left: 12px; padding: 4px 12px;
          background: #000000;
          animation: red-heartbeat-glow 4s ease-in-out infinite;
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 6px; text-decoration: none; color: #ffffff;
          font-size: 10px; font-weight: 600; letter-spacing: 0.04em;
          cursor: pointer; white-space: nowrap;
          transition: border-color 0.3s;
        }
      `}</style>

      {/* ===== TOP STATUS BANNER ===== */}
      <div style={{ background: 'rgba(212,165,116,0.08)', borderBottom: '1px solid rgba(212,165,116,0.15)', padding: '8px 16px', textAlign: 'center', fontSize: '10px', fontWeight: 500, color: 'var(--accent)', letterSpacing: '0.02em', position: 'relative', zIndex: 100, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', gap: '4px', lineHeight: '1.5' }}>
        <span style={{ fontSize: '13px' }}>⚠️</span>
        <span><strong>Disclaimer:</strong> Experimental AI platform by Ambuj Kumar Tripathi. Not financial advice.</span>
        <a href="https://stats.uptimerobot.com/4tYmSQnuBE" target="_blank" rel="noreferrer" className="afp-status-badge">
          <span style={{ position: 'relative', width: '8px', height: '8px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ position: 'absolute', width: '8px', height: '8px', borderRadius: '50%', background: 'rgba(185, 28, 28, 0.4)', animation: 'sonar-ping 2s ease-out infinite' }} />
            <span style={{ position: 'relative', width: '6px', height: '6px', borderRadius: '50%', background: '#b91c1c', boxShadow: '0 0 6px rgba(185, 28, 28, 0.6)' }} />
          </span>
          <svg width="28" height="12" viewBox="0 0 28 12" style={{ overflow: 'visible', marginLeft: '-2px' }}>
            <path d="M0,6 L6,6 L8,2 L10,10 L12,4 L14,8 L16,6 L28,6" fill="none" stroke="#dc2626" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" style={{ strokeDasharray: '30', strokeDashoffset: '0', animation: 'ecg-draw 2s linear infinite' }} />
          </svg>
          System Status
        </a>
      </div>

      {/* ===== NAVBAR ===== */}
      <nav style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '16px 40px',
        borderBottom: '1px solid var(--border)',
        background: 'rgba(12, 12, 20, 0.92)',
        backdropFilter: 'blur(12px)',
        position: 'sticky', top: 0, zIndex: 9999,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <FiCpu size={22} color="var(--accent)" />
          <span style={{ fontWeight: 700, fontSize: '1.05rem', letterSpacing: '-0.3px' }}>
            Agentic Financial Parser
          </span>
        </div>
        <div className="desktop-nav" style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
          <a href="https://ambuj-rag-docs.netlify.app" target="_blank" rel="noreferrer" className="nav-link nav-docs-btn">Documentation</a>
          <a href="#architecture" className="nav-link">Architecture</a>
          <a href="#demo" className="nav-link">Live Demo</a>
          <a href="#depth" className="nav-link">Engineering</a>
          <a href="#opensource" className="nav-link" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', lineHeight: '1.2', gap: '2px' }}>
            <span>qLoRA Fine-Tuned</span>
            <span style={{ fontSize: '0.65rem', color: '#c9a84c', textTransform: 'uppercase', letterSpacing: '0.5px' }}>By Ambuj Kumar Tripathi</span>
          </a>
          <a href="#engineer" className="nav-link">About</a>
          <a href={GOOGLE_AUTH_URL} className="btn-ghost" style={{ padding: '8px 18px', fontSize: '0.84rem' }}>Sign In</a>
          {import.meta.env.DEV && (
            <button className="btn-ghost" style={{ padding: '8px 18px', fontSize: '0.84rem', background: 'var(--accent)', color: '#000', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600 }}
              onClick={async () => {
                try {
                  const res = await fetch('http://localhost:8000/auth/dev-login', { method: 'POST' })
                  const data = await res.json()
                  if (data.access_token) { login(data.access_token, data.user); navigate('/chat') }
                } catch (e) { alert('Backend not running!') }
              }}>Dev Login</button>
          )}
        </div>
        <button className="hamburger-btn" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} style={{ display: 'none', background: 'none', border: 'none', cursor: 'pointer', padding: '8px' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" strokeWidth="2" strokeLinecap="round">
            {mobileMenuOpen ? <><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></> : <><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></>}
          </svg>
        </button>
      </nav>

      {/* ===== MOBILE MENU ===== */}
      {mobileMenuOpen && (
        <div style={{ position: 'fixed', top: '80px', left: '16px', right: '16px', background: 'var(--bg-secondary, #111)', border: '1px solid var(--border, #222)', borderRadius: '16px', padding: '24px', zIndex: 9998, boxShadow: '0 20px 40px rgba(0,0,0,0.8)', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <button onClick={() => { document.getElementById('architecture')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>Architecture</button>
          <button onClick={() => { document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>Live Demo</button>
          <button onClick={() => { document.getElementById('depth')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>Engineering</button>
          <button onClick={() => { document.getElementById('opensource')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>qLoRA Fine-Tuned Models</button>
          <button onClick={() => { document.getElementById('engineer')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>About</button>
          <div style={{ height: '1px', background: 'var(--border, #222)' }} />
          <a href="https://ambuj-rag-docs.netlify.app" target="_blank" rel="noreferrer" style={{ color: 'var(--accent, #c9a84c)', textDecoration: 'none', fontSize: '15px' }}>📄 Documentation</a>
          <a href={GOOGLE_AUTH_URL} style={{ color: '#ccc', textDecoration: 'none', fontSize: '15px' }}>🔐 Sign In</a>
        </div>
      )}

      {/* ===== HERO ===== */}
      <section style={{
        padding: '100px 40px 60px',
        textAlign: 'center',
        maxWidth: 920,
        margin: '0 auto',
        position: 'relative',
      }}>
        {/* Deep Red Black Spotlight Background */}
        <div style={{ position: 'absolute', top: -100, left: '50%', transform: 'translateX(-50%)', width: '800px', height: '600px', background: 'radial-gradient(circle at center, rgba(220, 38, 38, 0.15) 0%, transparent 60%)', filter: 'blur(70px)', pointerEvents: 'none', zIndex: 0 }} />

        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: 8,
          padding: '6px 16px', borderRadius: 20,
          background: 'var(--accent-glow)', border: '1px solid rgba(212,165,116,0.2)',
          fontSize: '0.78rem', color: 'var(--accent)', fontWeight: 500,
          marginBottom: 28,
        }}>
          <FiZap size={13} /> 8-Node LangGraph StateGraph • Production-Grade Agentic RAG
        </div>

        <h1 style={{
          fontSize: 'clamp(2.2rem, 5vw, 3.4rem)',
          fontWeight: 800,
          lineHeight: 1.1,
          letterSpacing: '-1.5px',
          marginBottom: 20,
        }}>
          Financial Intelligence,{' '}
          <span style={{
            background: 'linear-gradient(135deg, var(--accent), #e8c49a)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>Engineered.</span>
        </h1>

        <p style={{
          fontSize: '1.05rem', color: 'var(--text-secondary)',
          maxWidth: 660, margin: '0 auto 36px', lineHeight: 1.7,
        }}>
          Parse Union Budget, Finance Bill, Tax Laws (1961 & 2025), PF/Pension Schemes, RBI KYC &amp;
          Constitution of India with an 8-node agentic RAG — parallel vector retrieval,
          Cohere neural reranking, multi-version synthesis, and hallucination guard.
        </p>

        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14 }}>
          <a href={GOOGLE_AUTH_URL} style={{
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: 10,
            padding: '14px 32px', borderRadius: 'var(--radius-sm)',
            background: '#fff', color: '#333', fontWeight: 500, fontSize: '1rem',
            border: '1px solid rgba(0,0,0,0.1)',
            transition: 'box-shadow 0.2s',
            textDecoration: 'none',
          }}>
            <GoogleLogo size={20} /> Get Started with Google
          </a>
          <button id="hero-docs" onClick={() => setDocsOpen(true)} className="btn-ghost hero-docs-btn" style={{ fontSize: '0.95rem', padding: '13px 28px' }}>
            View Architecture Docs
          </button>
          <a href="#architecture" className="btn-ghost" style={{ fontSize: '0.95rem', padding: '13px 28px' }}>
            Inside System
          </a>
        </div>

        {/* Model Badges */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '28px', flexWrap: 'wrap' }}>
          <a href="https://huggingface.co/invincibleambuj/Ambuj-Tripathi-Indian-Legal-Llama-GGUF" target="_blank" rel="noreferrer" style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
            textDecoration: 'none', transition: 'transform 0.2s',
          }} onMouseOver={(e) => e.currentTarget.style.transform='translateY(-3px)'} onMouseOut={(e) => e.currentTarget.style.transform='translateY(0)'}>
            <div style={{
              width: '52px', height: '52px', borderRadius: '14px',
              background: '#111', border: '1px solid #2a2a2a',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '24px', transition: 'border-color 0.2s',
            }} onMouseOver={(e) => e.currentTarget.style.borderColor='#c9a84c'} onMouseOut={(e) => e.currentTarget.style.borderColor='#2a2a2a'}>
              🤗
            </div>
            <span style={{ color: '#888', fontSize: '11px', fontFamily: 'var(--font-mono)', letterSpacing: '0.5px' }}>Hugging Face ›</span>
          </a>

          <a href="https://lmstudio.ai" target="_blank" rel="noreferrer" style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
            textDecoration: 'none', transition: 'transform 0.2s',
          }} onMouseOver={(e) => e.currentTarget.style.transform='translateY(-3px)'} onMouseOut={(e) => e.currentTarget.style.transform='translateY(0)'}>
            <div style={{
              width: '52px', height: '52px', borderRadius: '14px',
              background: '#111', border: '1px solid #2a2a2a',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '24px', transition: 'border-color 0.2s',
            }} onMouseOver={(e) => e.currentTarget.style.borderColor='#c9a84c'} onMouseOut={(e) => e.currentTarget.style.borderColor='#2a2a2a'}>
              🖥️
            </div>
            <span style={{ color: '#888', fontSize: '11px', fontFamily: 'var(--font-mono)', letterSpacing: '0.5px' }}>LM Studio ›</span>
          </a>
        </div>
      </section>

      {/* ===== ANIMATED STATS STRIP ===== */}
      <section style={{
        padding: '60px 40px',
        borderTop: '1px solid rgba(212, 165, 116, 0.1)',
        borderBottom: '1px solid rgba(212, 165, 116, 0.1)',
        background: 'linear-gradient(90deg, rgba(22,27,38,0.3) 0%, rgba(212,165,116,0.03) 50%, rgba(22,27,38,0.3) 100%)',
      }}>
        <div style={{
          maxWidth: 1040, margin: '0 auto', display: 'flex', flexWrap: 'wrap',
          justifyContent: 'space-around', gap: '30px', textAlign: 'center'
        }}>
          <div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--accent)', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>
              <AnimatedNumber end={31528} suffix="+" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Total Chunks</div>
          </div>
          <div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#fff', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>
              <AnimatedNumber end={28352} suffix="+" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Child Vectors</div>
          </div>
          <div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#fff', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>
              <AnimatedNumber end={3176} suffix="+" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Parent Nodes</div>
          </div>
          <div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--accent)', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>
              <AnimatedNumber end={256} suffix="-dim" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>MRL Embedding</div>
          </div>
        </div>
      </section>

      {/* ===== TECH STRIP ===== */}
      <section style={{
        display: 'flex', justifyContent: 'center', flexWrap: 'wrap',
        gap: '32px', padding: '30px 40px 50px',
      }}>
        {[
          'LangGraph StateGraph', 'Jina v3 MRL (256-dim)', 'Pinecone Serverless',
          'Cohere Reranker', 'LlamaParse 3-Tier', 'FastAPI + Uvicorn'
        ].map(t => (
          <span key={t} style={{
            fontFamily: 'var(--font-mono)', fontSize: '0.76rem',
            color: 'var(--text-muted)', letterSpacing: '0.5px',
            textTransform: 'uppercase',
          }}>
            {t}
          </span>
        ))}
      </section>

      {/* ===== 8-NODE ARCHITECTURE ===== */}
      <section id="architecture" style={{
        padding: '80px 40px',
        borderTop: '1px solid var(--border)',
      }}>
        <div style={{ maxWidth: 1040, margin: '0 auto' }}>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 700, textAlign: 'center', marginBottom: 12 }}>
            8-Node <span style={{ color: 'var(--accent)' }}>LangGraph StateGraph</span>
          </h2>
          <p style={{
            textAlign: 'center', color: 'var(--text-secondary)',
            maxWidth: 650, margin: '0 auto 48px', fontSize: '0.93rem',
          }}>
            Not API wrapping. A full state machine with conditional edges,
            self-correction loops, cross-questioning, and hallucination detection —
            built on LangGraph's <code style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent)', fontSize: '0.85rem' }}>StateGraph(AgentState)</code>.
          </p>

          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: 14,
          }}>
            {[
              { icon: FiSearch, name: 'Classifier', desc: 'Intent detection via LLM: RAG query, Greeting, Abusive, Vague, or Out-of-scope. Routes to correct node via conditional edges.', color: 'var(--accent)' },
              { icon: FiMessageSquare, name: 'CrossQuestioner', desc: 'Vague query? Asks clarifying question (max 2 rounds). Prevents hallucinated answers on ambiguous inputs.', color: 'var(--purple)' },
              { icon: FiShield, name: 'Reject Node', desc: 'Blocks abusive/harmful queries with professional response. PII masking applied before any processing.', color: 'var(--red)' },
              { icon: FiLayers, name: 'Retriever', desc: 'Parallel intent-based Pinecone search across multiple law versions. Cohere neural reranker filters top 10 golden chunks from 100+ candidates. Parent-Child Recursive Retrieval.', color: 'var(--accent)' },
              { icon: FiCpu, name: 'Generator', desc: 'LLM with multi-version synthesis: compares 1961 vs 2025 Act provisions. Cautious RAG policy with banned-phrase guardrails. Confidence scoring.', color: 'var(--green)' },
              { icon: FiActivity, name: 'Hallucination Guard', desc: 'Post-generation check: is the answer grounded in retrieved chunks? If not → fallback. Confidence < 40% → reject.', color: 'var(--red)' },
              { icon: FiGitBranch, name: 'PostProcess', desc: 'Save Q&A to MongoDB (sliding window), log to Langfuse, cache response in Redis (1hr TTL). Feedback tracking.', color: 'var(--amber)' },
              { icon: FiZap, name: 'Fallback', desc: 'Circuit breaker (pybreaker): 3 API failures → circuit opens → graceful fallback message. No crash, no hang.', color: 'var(--text-muted)' },
            ].map(node => (
              <div key={node.name} className="glass-card" style={{ padding: '24px 20px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                <div style={{
                    position: 'relative', width: '48px', height: '48px', borderRadius: '50%', marginBottom: '20px'
                }}>
                    <div style={{
                        position: 'absolute', inset: 0, borderRadius: '50%',
                        background: node.color, opacity: 0.9, filter: 'blur(6px)'
                    }} />
                    <div style={{
                        position: 'relative', width: '100%', height: '100%', borderRadius: '50%',
                        background: '#05070A', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1
                    }}>
                        <node.icon size={20} color="#fff" />
                    </div>
                </div>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 8 }}>{node.name}</h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>{node.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== LIVE DEMO VIDEO ===== */}
      <section id="demo" style={{ padding: '80px 40px', borderTop: '1px solid var(--border)' }}>
        <div style={{ maxWidth: 960, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '6px 16px', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--accent)', border: '1px solid rgba(212,165,116,0.2)', borderRadius: '100px', marginBottom: '20px', background: 'var(--accent-glow)' }}>
              <span style={{ fontSize: '12px' }}>▶</span> Live Demo
            </span>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '12px' }}>See It In <span style={{ color: 'var(--accent)' }}>Action</span></h2>
            <p style={{ fontSize: '0.93rem', color: 'var(--text-secondary)', maxWidth: '520px', margin: '0 auto', lineHeight: 1.6 }}>Watch the AI parse legal and financial queries in real-time with streaming responses and source-grounded citations.</p>
          </div>
          <div style={{ position: 'relative', borderRadius: '16px', border: '1px solid rgba(212,165,116,0.15)', background: 'linear-gradient(180deg, rgba(22,27,38,0.5) 0%, rgba(10,13,18,0.9) 100%)', padding: '6px', boxShadow: '0 0 60px rgba(212,165,116,0.06), 0 20px 60px rgba(0,0,0,0.5)', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', top: 0, left: '15%', right: '15%', height: '1px', background: 'radial-gradient(circle, rgba(212,165,116,0.3) 0%, transparent 100%)', zIndex: 2 }} />
            <iframe src="https://player.cloudinary.com/embed/?cloud_name=dra6lzzb9&public_id=bot_response_k79sbj" width="640" height="360" style={{ height: 'auto', width: '100%', aspectRatio: '640 / 360', borderRadius: '12px', display: 'block', border: 'none' }} allow="autoplay; fullscreen; encrypted-media; picture-in-picture" allowFullScreen frameBorder="0" title="Live Bot Response Demo" />
          </div>
          <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '0.78rem', color: 'var(--text-muted)', letterSpacing: '0.5px' }}>Real-time RAG pipeline response · Streaming · Source verification against PDF</p>
        </div>
      </section>


      
      {/* ===== ENGINEERING DEPTH ===== */}
      <section id="depth" style={{
        padding: '80px 40px',
        borderTop: '1px solid var(--border)',
      }}>
        <div style={{ maxWidth: 1040, margin: '0 auto' }}>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 700, textAlign: 'center', marginBottom: 48 }}>
            Engineering <span style={{ color: 'var(--accent)' }}>Depth</span>
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18 }}>
            {/* LlamaParse */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)', marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiFileText size={16} /> LlamaParse 3-Tier Hybrid Parsing
              </h4>
              {[
                'Premium Tier: Complex tables, infographics, math formulas (₹ crore charts, tax slabs)',
                'Standard Tier: Dense structured text (Acts, Sections, Schedules)',
                'Free Tier (PyMuPDF): Plain-text PDFs (temp user uploads — saves LlamaParse credits)',
                'Auto-tier selection based on table density & image count',
                'Custom parsing instructions tuned for Indian financial vocabulary',
              ].map(item => (
                <div key={item} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8 }}>
                  <FiCheck size={13} color="var(--green)" style={{ marginTop: 4, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{item}</span>
                </div>
              ))}
            </div>

            {/* Parent-Child Chunking */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)', marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiGrid size={16} /> Parent-Child Chunking & Recursive Retrieval
              </h4>
              {[
                'Parent chunks (1500 tokens): Full context for LLM generation',
                'Child chunks (300 tokens): Small, precise units for embedding search',
                'Search hits child → retrieves parent → LLM sees full surrounding context',
                'MarkdownHeaderSplitter for LlamaParse output (preserves entire tables)',
                'RecursiveCharacterTextSplitter for PyMuPDF (with overlap for coherence)',
              ].map(item => (
                <div key={item} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8 }}>
                  <FiCheck size={13} color="var(--green)" style={{ marginTop: 4, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{item}</span>
                </div>
              ))}
            </div>

            {/* MRL Embeddings */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)', marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiDatabase size={16} /> Matryoshka Representation Learning (MRL)
              </h4>
              {[
                'Jina Embeddings v3: 1024-dim native → truncated to 256-dim',
                'MRL: Like Russian nesting dolls — first 256 dims capture 95% of semantic meaning',
                '75% storage saved on Pinecone (free tier: 2GB limit)',
                'Cosine similarity search quality nearly identical to full 1024-dim',
                'Batch embedding with exponential backoff + circuit breaker on Jina API',
              ].map(item => (
                <div key={item} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8 }}>
                  <FiCheck size={13} color="var(--green)" style={{ marginTop: 4, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{item}</span>
                </div>
              ))}
            </div>

            {/* SHA-256 + Deterministic IDs */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)', marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiHash size={16} /> SHA-256 Sync & Deterministic Chunk IDs
              </h4>
              {[
                'SHA-256 hash per PDF → detect new / changed / deleted / unchanged',
                'Deterministic IDs: MD5(file_hash + parentIdx + childIdx) — not random UUIDs',
                'Same PDF = same chunk IDs → Pinecone upsert is idempotent (no duplicates ever)',
                'Incremental indexing: only re-embed changed files (saves Jina API credits)',
                'Surgical deletion: remove old vectors before re-embedding changed files',
              ].map(item => (
                <div key={item} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8 }}>
                  <FiCheck size={13} color="var(--green)" style={{ marginTop: 4, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{item}</span>
                </div>
              ))}
            </div>

            {/* Backend Security */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)', marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiLock size={16} /> Backend Security (7 Layers + API Protection)
              </h4>
              {[
                'Magic bytes validation (%PDF header) + MIME type check',
                'Chunked 1MB streaming upload (prevents OOM on 512MB RAM)',
                'PDF bomb guard: max 500 pages per file',
                'SHA-256 dedup: same file uploaded twice → skip, no re-indexing',
                'Circuit Breaker (pybreaker): 3 failures → open → fallback response',
                'Rate limiting: 10 req/min per user (Redis-backed)',
                'PII masking + abusive content filter on all queries',
                'JWT auth (Google OAuth 2.0) + admin-only endpoints',
              ].map(item => (
                <div key={item} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8 }}>
                  <FiCheck size={13} color="var(--green)" style={{ marginTop: 4, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{item}</span>
                </div>
              ))}
            </div>

            {/* HITL */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)', marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiUploadCloud size={16} /> Human-in-the-Loop (HITL) Chunk Review
              </h4>
              {[
                'User uploads PDF → parsed → chunked → stored as "pending_review"',
                'User sees every chunk before embedding (approve / reject / edit)',
                'Rejected chunks = zero Jina API call (no quota waste)',
                'Only approved chunks get embedded into Pinecone temp namespace',
                'Logout → all temp vectors auto-deleted from Pinecone',
                'Admin can review chunks from all users via /admin panel',
              ].map(item => (
                <div key={item} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8 }}>
                  <FiCheck size={13} color="var(--green)" style={{ marginTop: 4, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ===== OPEN SOURCE MODEL ===== */}
      <section id="opensource" className="opensource-section" style={{ padding: '80px 40px', background: '#0a0a0a', borderTop: '1px solid #2a2a2a' }}>
        <div style={{ maxWidth: '900px', margin: '0 auto' }}>
          
          <p style={{ color: '#c9a84c', fontSize: '12px', letterSpacing: '3px', textTransform: 'uppercase', marginBottom: '12px' }}>qLoRA Fine-Tuned By Ambuj Kumar Tripathi</p>
          <h2 style={{ color: '#ffffff', fontSize: '36px', fontWeight: '700', marginBottom: '8px' }}>Indian Legal LLM</h2>
          <p style={{ color: '#a3a3a3', fontSize: '13px', marginBottom: '16px', letterSpacing: '1px' }}>Designed & Fine-tuned by <span style={{ color: '#c9a84c' }}>Ambuj Kumar Tripathi</span> · invincibleambuj</p>
          <p style={{ color: '#f3f4f6', fontSize: '15px', marginBottom: '48px', lineHeight: '1.6', maxWidth: '680px' }}>Fine-tuned a family of Llama 3 models (1B, 3B, and 8B) on 14,543 Indian Legal examples — IPC, CrPC & Constitution of India using 2x NVIDIA T4 GPUs. Open-source and highly optimized for consumer hardware.</p>

          <div className="opensource-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginBottom: '32px' }}>
            
            <a href="https://huggingface.co/invincibleambuj" target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '24px' }} onMouseOver={(e) => e.currentTarget.style.borderColor='#c9a84c'} onMouseOut={(e) => e.currentTarget.style.borderColor='#222'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span style={{ fontSize: '16px' }}>🤗</span>
                  <span style={{ color: '#c9a84c', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase' }}>Hugging Face</span>
                </div>
                <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', margin: '0 0 8px 0' }}>Model Collection</h3>
                <p style={{ color: '#555', fontSize: '13px', margin: '0 0 16px 0', lineHeight: '1.5' }}>Access all 1B, 3B, and 8B fine-tuned legal models directly.</p>
                <span style={{ color: '#c9a84c', fontSize: '12px' }}>View on Hugging Face →</span>
              </div>
            </a>

            <a href="https://huggingface.co/invincibleambuj/Ambuj-Tripathi-Indian-Legal-Llama-GGUF" target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '24px' }} onMouseOver={(e) => e.currentTarget.style.borderColor='#c9a84c'} onMouseOut={(e) => e.currentTarget.style.borderColor='#222'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span style={{ fontSize: '16px' }}>📦</span>
                  <span style={{ color: '#c9a84c', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase' }}>GGUF</span>
                </div>
                <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', margin: '0 0 8px 0' }}>Run Locally</h3>
                <p style={{ color: '#555', fontSize: '13px', margin: '0 0 16px 0', lineHeight: '1.5' }}>Download & run on CPU. No GPU needed. 807 MB.</p>
                <span style={{ color: '#c9a84c', fontSize: '12px' }}>Download GGUF →</span>
              </div>
            </a>

            <a href="https://lmstudio.ai" target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '24px' }} onMouseOver={(e) => e.currentTarget.style.borderColor='#c9a84c'} onMouseOut={(e) => e.currentTarget.style.borderColor='#222'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span style={{ fontSize: '16px' }}>🖥️</span>
                  <span style={{ color: '#c9a84c', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase' }}>LM Studio</span>
                </div>
                <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', margin: '0 0 8px 0' }}>Desktop App</h3>
                <p style={{ color: '#555', fontSize: '13px', margin: '0 0 16px 0', lineHeight: '1.5' }}>Search & chat locally. No code required.</p>
                <span style={{ color: '#c9a84c', fontSize: '12px' }}>Open in LM Studio →</span>
              </div>
            </a>

          </div>

          <div style={{ background: '#0d0d0d', border: '1px solid #1e1e1e', borderRadius: '12px', overflow: 'hidden' }}>
            <div style={{ background: '#111', padding: '10px 20px', borderBottom: '1px solid #1e1e1e', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }}></div>
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }}></div>
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27c93f' }}></div>
              <span style={{ color: '#444', fontSize: '11px', marginLeft: '8px', fontFamily: 'monospace' }}>quick_start.py</span>
            </div>
            <TypewriterCodeBlock />
          </div>

          <p style={{ color: '#aaa', fontSize: '12px', marginTop: '20px', textAlign: 'center', letterSpacing: '0.5px' }}>Built with Llama 3.2 · Fine-tuned by <strong style={{ color: '#c9a84c' }}>Ambuj Kumar Tripathi</strong> · Llama 3.2 Community License</p>

        </div>
      </section>

      {/* ===== TRAINING PIPELINE VIDEO ===== */}
      <section style={{ padding: '80px 40px', borderTop: '1px solid #2a2a2a', background: '#0a0a0a' }}>
        <div style={{ maxWidth: 960, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '6px 16px', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.12em', color: '#c9a84c', border: '1px solid rgba(201,168,76,0.25)', borderRadius: '100px', marginBottom: '20px', background: 'rgba(201,168,76,0.05)' }}>
              <span style={{ fontSize: '12px' }}>▶</span> Training Process
            </span>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '12px', color: '#fff' }}>Training <span style={{ color: '#c9a84c' }}>Pipeline</span></h2>
            <p style={{ fontSize: '0.93rem', color: '#6B7280', maxWidth: '480px', margin: '0 auto', lineHeight: 1.6 }}>Watch the full qLoRA fine-tuning cycle — from training steps and loss convergence to GGUF quantization export.</p>
          </div>
          <div style={{ position: 'relative', borderRadius: '16px', border: '1px solid rgba(201,168,76,0.15)', background: 'linear-gradient(180deg, rgba(22,27,38,0.5) 0%, rgba(10,13,18,0.9) 100%)', padding: '6px', boxShadow: '0 0 60px rgba(201,168,76,0.06), 0 20px 60px rgba(0,0,0,0.5)', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', top: 0, left: '15%', right: '15%', height: '1px', background: 'radial-gradient(circle, rgba(201,168,76,0.3) 0%, transparent 100%)', zIndex: 2 }} />
            <iframe src="https://player.cloudinary.com/embed/?cloud_name=dra6lzzb9&public_id=qlora_training_nsjd7g" width="640" height="360" style={{ height: 'auto', width: '100%', aspectRatio: '640 / 360', borderRadius: '12px', display: 'block', border: 'none' }} allow="autoplay; fullscreen; encrypted-media; picture-in-picture" allowFullScreen frameBorder="0" title="qLoRA Fine-Tuning Training" />
          </div>
          <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '0.78rem', color: '#4B5563', letterSpacing: '0.5px' }}>qLoRA 4-bit training · Loss convergence · GGUF Q4_K_M quantization export</p>
        </div>
      </section>
      <section id="engineer" style={{
        padding: '80px 40px',
        borderTop: '1px solid rgba(212, 165, 116, 0.1)',
        textAlign: 'center',
        position: 'relative',
        background: '#0a0a0a',
        overflow: 'hidden',
      }}>
        {/* Accent Gradients (Matched to Hero Deep Red) */}
        <div style={{ position: 'absolute', top: 0, left: '50%', transform: 'translateX(-50%)', width: '120vw', height: '100%', background: 'radial-gradient(circle at 50% 0%, rgba(220, 38, 38, 0.15) 0%, transparent 60%)', filter: 'blur(60px)', pointerEvents: 'none' }} />
        
        <div style={{ maxWidth: 720, margin: '0 auto', position: 'relative', zIndex: 2 }}>
          <div style={{
            display: 'inline-block', padding: '6px 16px', borderRadius: 20,
            background: 'var(--accent-glow)', border: '1px solid rgba(212,165,116,0.2)',
            fontSize: '0.75rem', color: 'var(--accent)', fontWeight: 600,
            marginBottom: 20, letterSpacing: '1px', textTransform: 'uppercase',
          }}>
            Engineered By
          </div>

          <h2 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: 8, letterSpacing: '-0.5px' }}>
            Ambuj Kumar Tripathi
          </h2>
          <p style={{
            fontSize: '0.95rem', color: 'var(--accent)', fontWeight: 500,
            marginBottom: 18,
          }}>
            AI Engineer · RAG Systems Architect · Production ML
          </p>
          <p style={{
            fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.7,
            marginBottom: 12,
          }}>
            B.Tech in Electrical &amp; Electronics Engineering.
            Specialist in production-grade RAG pipelines, LangGraph orchestration,
            and serverless vector architectures under hard resource constraints.
          </p>
          <p style={{
            fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.6,
            marginBottom: 28,
          }}>
            Built enterprise-grade systems across <strong style={{ color: 'var(--text-secondary)' }}>Global Telecom</strong> and{' '}
            <strong style={{ color: 'var(--text-secondary)' }}>International AdTech</strong> —
            hands-on experience shipping production systems that handle real-world scale.
          </p>

          {/* Certifications */}
          <div style={{
            display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 8,
            marginBottom: 32,
          }}>
            {[
              'NVIDIA RAG Agents', 'Google Cloud (6 Badges)', 'IBM AI Engineering',
              'Anthropic MCP', 'Linux Foundation', 'BCG X GenAI'
            ].map(cert => (
              <span key={cert} style={{
                padding: '4px 12px', borderRadius: 20,
                background: 'var(--bg-tertiary)', border: '1px solid var(--border)',
                fontSize: '0.72rem', color: 'var(--text-secondary)',
                fontFamily: 'var(--font-mono)',
              }}>{cert}</span>
            ))}
          </div>

          {/* Links */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: 14, flexWrap: 'wrap' }}>
            <a href="https://ambuj-portfolio-v2.netlify.app" target="_blank" rel="noreferrer"
              className="btn-ghost" style={{ fontSize: '0.88rem' }}>
              <FiGlobe size={16} /> Portfolio
            </a>
            <a href="https://github.com/Ambuj123-lab" target="_blank" rel="noreferrer"
              className="btn-ghost" style={{ fontSize: '0.88rem' }}>
              <FiGithub size={16} /> GitHub
            </a>
            <a href="https://ambuj-rag-docs.netlify.app" target="_blank" rel="noreferrer"
              className="btn-ghost" style={{ fontSize: '0.88rem' }}>
              <FiBookOpen size={16} /> Engineering Docs
            </a>
            <a href="https://www.linkedin.com/in/ambuj-tripathi-042b4a118/" target="_blank" rel="noreferrer"
              className="btn-ghost" style={{ fontSize: '0.88rem' }}>
              <FiLinkedin size={16} /> LinkedIn
            </a>
          </div>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer style={{
        padding: '40px 40px',
        background: '#0a0a0a',
        textAlign: 'center',
        position: 'relative',
        borderTop: '1px solid rgba(255,255,255,0.02)'
      }}>
        {/* Glowing Gradient Top Border */}
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '1px', background: 'linear-gradient(90deg, transparent, rgba(220, 38, 38, 0.5), transparent)' }} />
        
        <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          © 2026 Agentic Financial Parser — Engineered by{' '}
          <a href="https://ambuj-portfolio-v2.netlify.app" target="_blank" rel="noreferrer">
            Ambuj Kumar Tripathi
          </a>
          . Production RAG, engineered for reality.
        </p>
      </footer>

      {/* Responsive overrides */}
      <style>{`
        .nav-link {
          background: none; border: none; padding: 0;
          color: var(--text-secondary); font-size: 0.88rem;
          cursor: pointer; font-family: inherit;
          text-decoration: none;
        }
        .nav-link:hover { color: var(--text-primary); }
        .hamburger-btn { display: none !important; }
        
        @media (max-width: 768px) {
          nav { padding: 12px 16px !important; }
          .desktop-nav { display: none !important; }
          .hamburger-btn { display: block !important; }
          section { padding-left: 16px !important; padding-right: 16px !important; }
          h1 { font-size: 1.8rem !important; }
          div[style*='grid-template-columns: 1fr 1fr'] { grid-template-columns: 1fr !important; }
          div[style*='repeat(auto-fit'] { grid-template-columns: 1fr 1fr !important; }
        }
        @media (max-width: 480px) {
          div[style*='repeat(auto-fit'] { grid-template-columns: 1fr !important; }
        }
        .hero-docs-btn:target {
          animation: highlightBlink 2s ease-in-out;
        }
        @keyframes highlightBlink {
          0%, 100% { box-shadow: 0 0 0 0 transparent; }
          20%, 60% { box-shadow: 0 0 0 8px rgba(212, 165, 116, 0.4); border-color: var(--accent); }
        }
      `}</style>
      {/* ===== DOCS MODAL ===== */}
      {docsOpen && (
        <div className="docs-modal-overlay" onClick={() => setDocsOpen(false)}>
          <div className="docs-modal-content" onClick={e => e.stopPropagation()}>
            <div className="docs-modal-header">
              <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <FiBookOpen size={18} color="var(--accent)" /> System Architecture Documentation
              </span>
              <button className="docs-modal-close" onClick={() => setDocsOpen(false)}>×</button>
            </div>
            <iframe 
              src="https://ambuj-rag-docs.netlify.app/docs/domain-applications/financial-parser" 
              title="Architecture Documentation"
              className="docs-iframe"
            />
          </div>
        </div>
      )}
    </div>
  )
}
