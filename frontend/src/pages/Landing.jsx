import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import {
  FiCpu, FiShield, FiZap, FiLayers, FiGitBranch,
  FiSearch, FiMessageSquare, FiUploadCloud, FiGithub,
  FiLinkedin, FiBookOpen, FiGlobe, FiArrowRight, FiCheck,
  FiFileText, FiDatabase, FiLock, FiHash, FiGrid, FiActivity
} from 'react-icons/fi'
import { FaLinkedin, FaXTwitter, FaMedium, FaGithub } from 'react-icons/fa6'

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

/* ── Fade-In on Scroll ── */
const useFadeIn = (delay = 0) => {
    const [visible, setVisible] = useState(false);
    const ref = useRef(null);
    useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) { setVisible(true); observer.disconnect(); }
        }, { threshold: 0.15 });
        if (ref.current) observer.observe(ref.current);
        return () => observer.disconnect();
    }, []);
    return {
        ref,
        style: {
            opacity: visible ? 1 : 0,
            transform: visible ? 'translateY(0)' : 'translateY(30px)',
            transition: `opacity 0.6s ease ${delay}s, transform 0.6s ease ${delay}s`,
        }
    };
};

const FadeIn = ({ delay = 0, children, style = {} }) => {
    const fade = useFadeIn(delay);
    return <div ref={fade.ref} style={{ ...fade.style, ...style }}>{children}</div>;
};

export default function Landing() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [docsOpen, setDocsOpen] = useState(false)
  const [legalModal, setLegalModal] = useState(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [showBackToTop, setShowBackToTop] = useState(false)
  const [scrollProgress, setScrollProgress] = useState(0)
  const [uptimeData, setUptimeData] = useState(null)

  useEffect(() => {
      const handleScroll = () => {
          setShowBackToTop(window.scrollY > 600)
          const totalScroll = document.documentElement.scrollTop
          const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight
          const scroll = totalScroll / windowHeight * 100
          setScrollProgress(scroll)
      }
      window.addEventListener('scroll', handleScroll, { passive: true })
      return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
      fetch('/api/uptime')
          .then(res => res.json())
          .then(data => {
              if (data && data.uptime) {
                  setUptimeData(data)
              } else {
                  setUptimeData({ uptime: '--%', latency: '--' })
              }
          })
          .catch(err => {
              console.error("Failed to fetch uptime:", err)
              setUptimeData({ uptime: '--%', latency: '--' })
          })
  }, [])

  if (user) {
    navigate('/chat', { replace: true })
    return null
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
      {/* ===== SCROLL PROGRESS BAR ===== */}
      <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          height: '3px',
          background: 'rgba(255, 255, 255, 0.05)',
          zIndex: 10000,
          pointerEvents: 'none',
      }}>
          <div style={{
              height: '100%',
              width: `${scrollProgress}%`,
              background: '#dc2626',
              boxShadow: '0 0 10px #dc2626, 0 0 5px #dc2626',
              transition: 'width 0.1s ease-out'
          }} />
      </div>
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
        @keyframes blueprint-red-glow {
          0%   { box-shadow: 0 0 0px rgba(255,0,0,0), 0 0 0px rgba(255,0,0,0); }
          35%  { box-shadow: 0 0 0px rgba(255,0,0,0), 0 0 0px rgba(255,0,0,0); }
          50%  { box-shadow: 0 0 20px rgba(255,0,0,0.6), 0 0 40px rgba(255,0,0,0.4), 0 0 60px rgba(255,0,0,0.2); }
          65%  { box-shadow: 0 0 0px rgba(255,0,0,0), 0 0 0px rgba(255,0,0,0); }
          100% { box-shadow: 0 0 0px rgba(255,0,0,0), 0 0 0px rgba(255,0,0,0); }
        }
        @keyframes golden-border-glow {
          0%   { border-color: rgba(251,191,36,0.3); }
          50%  { border-color: rgba(251,191,36,0.9); }
          100% { border-color: rgba(251,191,36,0.3); }
        }
        .arch-btn-wrapper {
          position: relative;
          display: inline-flex;
          border-radius: 10px;
          animation: blueprint-red-glow 5s ease-in-out infinite;
        }
        .arch-btn-wrapper:hover {
          transform: translateY(-2px);
          box-shadow: 0 0 30px rgba(255,0,0,0.6), 0 0 50px rgba(255,0,0,0.4), 0 0 80px rgba(255,0,0,0.25) !important;
        }
        .arch-btn-inner {
          display: inline-flex; align-items: center; gap: 8px;
          padding: 12px 26px;
          background: #000000;
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 10px;
          color: #ffffff;
          font-size: 0.9rem; font-weight: 600;
          letter-spacing: 0.5px;
          text-decoration: none;
          font-family: inherit;
          transition: background 0.3s, border-color 0.3s;
        }
        .arch-btn-inner:hover { background: #0a0a0a; border-color: rgba(255,255,255,0.3); }
        .arch-btn-inner svg { opacity: 0.9; }
      `}</style>

      {/* ===== TOP STATUS BANNER ===== */}
      <div style={{ background: 'rgba(255,51,51,0.08)', borderBottom: '1px solid rgba(255,51,51,0.15)', padding: '8px 16px', textAlign: 'center', fontSize: '10px', fontWeight: 500, color: 'var(--accent)', letterSpacing: '0.02em', position: 'relative', zIndex: 100, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', gap: '4px', lineHeight: '1.5' }}>
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
          {uptimeData ? `${uptimeData.uptime} • ${uptimeData.latency}` : 'System Status'}
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
            <span style={{ fontSize: '0.65rem', color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>By Ambuj Kumar Tripathi</span>
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

        {/* ===== MOBILE MENU (inside nav, top:100% = always below navbar) ===== */}
        {mobileMenuOpen && (
          <div style={{ position: 'absolute', top: '100%', left: '0', right: '0', margin: '8px 16px 0', background: 'var(--bg-secondary, #111)', border: '1px solid var(--border, #222)', borderRadius: '16px', padding: '24px', zIndex: 9998, boxShadow: '0 20px 40px rgba(0,0,0,0.8)', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <button onClick={() => { document.getElementById('architecture')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>Architecture</button>
            <button onClick={() => { document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>Live Demo</button>
            <button onClick={() => { document.getElementById('depth')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>Engineering</button>
            <button onClick={() => { document.getElementById('opensource')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>qLoRA Fine-Tuned Models</button>
            <button onClick={() => { document.getElementById('engineer')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false); }} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '15px', fontWeight: 500, textAlign: 'left', padding: '0' }}>About</button>
            <div style={{ height: '1px', background: 'var(--border, #222)' }} />
            <a href="https://ambuj-rag-docs.netlify.app" target="_blank" rel="noreferrer" style={{ color: 'var(--accent, var(--accent))', textDecoration: 'none', fontSize: '15px' }}>📄 Documentation</a>
            <a href={GOOGLE_AUTH_URL} style={{ color: '#ccc', textDecoration: 'none', fontSize: '15px' }}>🔐 Sign In</a>
            <button onClick={() => setMobileMenuOpen(false)} style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.4)', color: '#ef4444', cursor: 'pointer', fontSize: '14px', fontWeight: 600, padding: '12px', borderRadius: '8px', textAlign: 'center' }}>✕ Close Menu</button>
          </div>
        )}
      </nav>

      {/* ===== HERO ===== */}
      <section style={{
        padding: '120px 40px 100px',
        textAlign: 'center',
        maxWidth: 1000,
        margin: '0 auto',
        position: 'relative',
      }}>
        {/* Deep Red Black Spotlight Background (Pexio Style) */}
        <div style={{ position: 'absolute', top: -50, left: '50%', transform: 'translateX(-50%)', width: '900px', height: '700px', background: 'radial-gradient(circle at center, rgba(220, 10, 10, 0.25) 0%, rgba(150, 0, 0, 0.1) 40%, transparent 70%)', filter: 'blur(60px)', pointerEvents: 'none', zIndex: 0 }} />

        {/* Top Banner (Simplify your workflow style) */}
        <div style={{
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: 16,
          marginBottom: 32, textAlign: 'center', position: 'relative', zIndex: 2
        }}>
          <div style={{ width: '40px', height: '1px', background: 'linear-gradient(90deg, transparent, rgba(255,51,51,0.5))' }}></div>
          <div style={{ 
            padding: '6px 20px', borderRadius: '30px', 
            background: 'rgba(255, 51, 51, 0.08)', 
            border: '1px solid rgba(255, 51, 51, 0.3)',
            boxShadow: '0 0 20px rgba(255, 51, 51, 0.2), inset 0 0 10px rgba(255, 51, 51, 0.1)',
            fontSize: '0.8rem', color: '#e0e0e0', fontWeight: 500, letterSpacing: '0.5px'
          }}>
            <FiZap size={12} style={{ display: 'inline', marginRight: '6px', color: 'var(--accent)' }} />
            Adaptive ReAct • 9-Node LangGraph • Live Web Search • WhatsApp Omnichannel
          </div>
          <div style={{ width: '40px', height: '1px', background: 'linear-gradient(270deg, transparent, rgba(255,51,51,0.5))' }}></div>
        </div>

        <h1 style={{
          fontSize: 'clamp(2.5rem, 5vw, 4rem)',
          fontWeight: 700,
          lineHeight: 1.15,
          letterSpacing: '-1px',
          marginBottom: 24,
          position: 'relative',
          zIndex: 2,
          color: '#ffffff'
        }}>
          Adaptive ReAct Agentic RAG for<br />
          <span style={{ color: 'var(--accent)' }}>Legal & Financial Workflows</span>
        </h1>

        <p style={{
          fontSize: '1.05rem', color: 'var(--text-secondary)',
          maxWidth: 600, margin: '0 auto 40px', lineHeight: 1.6,
          position: 'relative', zIndex: 2
        }}>
          Parse Indian Constitution, Union Budgets, Finance Acts, and RBI KYC with a <strong>9-Node Agentic RAG</strong>. 
          Featuring parallel vector retrieval, Autonomous Web Search Fallback, multi-version synthesis, and a strict hallucination guard.
        </p>

        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14, alignItems: 'center', position: 'relative', zIndex: 2 }}>
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
          <button id="hero-docs" onClick={() => setDocsOpen(true)} className="btn-ghost hero-docs-btn" style={{ fontSize: '0.95rem', padding: '13px 28px', borderRadius: 'var(--radius-sm)' }}>
            View Architecture Docs
          </button>
          <a href="#architecture" className="btn-ghost" style={{ fontSize: '0.95rem', padding: '13px 28px', borderRadius: 'var(--radius-sm)' }}>
            Inside System
          </a>
          <a href="/architecture.html" target="_blank" rel="noreferrer" className="arch-btn-wrapper" style={{ textDecoration: 'none' }}>
            <span className="arch-btn-inner" style={{ borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '16px' }}>🏗️</span>
              System Blueprint
            </span>
          </a>
        </div>

        {/* Model Badges */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '60px', flexWrap: 'wrap', position: 'relative', zIndex: 2 }}>
          <a href="https://tavily.com" target="_blank" rel="noreferrer" style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
            textDecoration: 'none', transition: 'transform 0.2s',
          }} onMouseOver={(e) => e.currentTarget.style.transform='translateY(-3px)'} onMouseOut={(e) => e.currentTarget.style.transform='translateY(0)'}>
            <div style={{
              width: '52px', height: '52px', borderRadius: '14px',
              background: '#0a0a0a', border: '1px solid var(--border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '24px', transition: 'all 0.2s', boxShadow: '0 0 15px rgba(0,0,0,0.5)'
            }} onMouseOver={(e) => { e.currentTarget.style.borderColor='var(--border-active)'; e.currentTarget.style.boxShadow='0 0 20px var(--accent-glow)' }} onMouseOut={(e) => { e.currentTarget.style.borderColor='var(--border)'; e.currentTarget.style.boxShadow='0 0 15px rgba(0,0,0,0.5)' }}>
              🌐
            </div>
            <span style={{ color: 'var(--accent)', fontSize: '11px', fontFamily: 'var(--font-mono)', letterSpacing: '0.5px', fontWeight: 600 }}>Live Web Agent ›</span>
          </a>

          <a href="https://huggingface.co/invincibleambuj/Ambuj-Tripathi-Indian-Legal-Llama-GGUF" target="_blank" rel="noreferrer" style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
            textDecoration: 'none', transition: 'transform 0.2s',
          }} onMouseOver={(e) => e.currentTarget.style.transform='translateY(-3px)'} onMouseOut={(e) => e.currentTarget.style.transform='translateY(0)'}>
            <div style={{
              width: '52px', height: '52px', borderRadius: '14px',
              background: '#0a0a0a', border: '1px solid var(--border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '24px', transition: 'border-color 0.2s',
            }} onMouseOver={(e) => e.currentTarget.style.borderColor='var(--border-active)'} onMouseOut={(e) => e.currentTarget.style.borderColor='var(--border)'}>
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
              background: '#0a0a0a', border: '1px solid var(--border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '24px', transition: 'border-color 0.2s',
            }} onMouseOver={(e) => e.currentTarget.style.borderColor='var(--border-active)'} onMouseOut={(e) => e.currentTarget.style.borderColor='var(--border)'}>
              🖥️
            </div>
            <span style={{ color: '#888', fontSize: '11px', fontFamily: 'var(--font-mono)', letterSpacing: '0.5px' }}>LM Studio ›</span>
          </a>
        </div>
      </section>

      {/* ===== ANIMATED STATS STRIP ===== */}
      <section style={{
        padding: '60px 40px',
        borderTop: '1px solid rgba(255,51,51, 0.1)',
        borderBottom: '1px solid rgba(255,51,51, 0.1)',
        background: 'linear-gradient(90deg, rgba(22,27,38,0.3) 0%, rgba(255,51,51,0.03) 50%, rgba(22,27,38,0.3) 100%)',
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

      {/* ===== CORE ARSENAL MARQUEE (MERCOR STYLE) ===== */}
      <style>{`
          @keyframes marquee-scroll {
              0% { transform: translateX(0); }
              100% { transform: translateX(-50%); }
          }
          .marquee-wrapper {
              position: relative;
              background: var(--bg-primary);
              border-top: 1px solid rgba(255,51,51, 0.05);
              border-bottom: 1px solid rgba(255,51,51, 0.05);
              overflow: hidden;
          }
          .marquee-container {
              display: flex;
              align-items: center;
              padding: 18px 0;
              position: relative;
          }
          .marquee-label-box {
              position: absolute;
              left: 0;
              top: 0;
              bottom: 0;
              display: flex;
              align-items: center;
              padding: 0 40px;
              background: linear-gradient(90deg, var(--bg-primary) 80%, transparent 100%);
              z-index: 10;
          }
          .marquee-label-text {
              font-size: 11px;
              color: var(--text-secondary);
              text-transform: uppercase;
              letter-spacing: 0.25em;
              font-weight: 700;
          }
          .marquee-track {
              display: flex;
              width: max-content;
              animation: marquee-scroll 45s linear infinite;
              padding-left: 200px;
          }
          .marquee-track:hover { animation-play-state: paused; }
          .marquee-item {
              display: inline-flex;
              align-items: center;
              gap: 8px;
              margin: 0 24px;
              font-size: 14px;
              font-weight: 600;
              white-space: nowrap;
              transition: opacity 0.2s;
              cursor: default;
          }
          .marquee-item:hover { opacity: 0.7; }
          .marquee-icon { display: flex; align-items: center; font-size: 16px; }
          .marquee-icon img { height: 16px; width: auto; object-fit: contain; }
          .marquee-gradient-right {
              position: absolute;
              right: 0;
              top: 0;
              bottom: 0;
              width: 60px;
              background: linear-gradient(-90deg, var(--bg-primary) 0%, transparent 100%);
              z-index: 10;
              pointer-events: none;
          }
      `}</style>
      <section className="marquee-wrapper" style={{ zIndex: 10 }}>
          <div className="marquee-container">
              <div className="marquee-label-box">
                  <span className="marquee-label-text">Core Arsenal</span>
              </div>
              <div className="marquee-gradient-right"></div>
              
              <div className="marquee-track">
                  {[...Array(2)].map((_, setIdx) => (
                      [
                          { name: 'FastAPI', emoji: '⚡', color: '#009688' },
                          { name: 'LangGraph', emoji: '🕸️', color: '#A855F7' },
                          { name: 'Qdrant', emoji: '🔴', color: '#EF4444' },
                          { name: 'Pinecone', emoji: '🌲', color: '#D1D5DB' },
                          { name: 'Redis', icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original.svg', color: '#FF4438' },
                          { name: 'MongoDB', icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original.svg', color: '#47A248' },
                          { name: 'Supabase', emoji: '⚡', color: '#3ECF8E' },
                          { name: 'React', icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg', color: '#61DAFB' },
                          { name: 'Vite', icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vitejs/vitejs-original.svg', color: '#646CFF' },
                          { name: 'Docker', icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg', color: '#2496ED' },
                          { name: 'Python', icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg', color: '#3776AB' },
                          { name: 'Jina AI', emoji: '🧬', color: '#009193' },
                          { name: 'Presidio', emoji: '🛡️', color: '#0078D4' },
                          { name: 'Langfuse', emoji: '📈', color: '#F59E0B' },
                      ].map((tech, i) => (
                          <span className="marquee-item" key={`${setIdx}-${i}`} style={{ color: tech.color }}>
                              <span className="marquee-icon">
                                  {tech.icon ? <img src={tech.icon} alt={tech.name} /> : tech.emoji}
                              </span>
                              {tech.name}
                          </span>
                      ))
                  ))}
              </div>
          </div>
      </section>

      {/* ===== 9-NODE ARCHITECTURE ===== */}
      <section id="architecture" style={{
        padding: '80px 40px',
        borderTop: '1px solid var(--border)',
      }}>
        <div style={{ maxWidth: 1040, margin: '0 auto' }}>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 700, textAlign: 'center', marginBottom: 12 }}>
            9-Node <span style={{ color: 'var(--accent)' }}>LangGraph StateGraph</span>
          </h2>
          <p style={{
            textAlign: 'center', color: 'var(--text-secondary)',
            maxWidth: 650, margin: '0 auto 48px', fontSize: '0.93rem',
          }}>
            Not API wrapping. A full state machine with conditional edges,
            self-correction loops, cross-questioning, web search fallback, and hallucination detection —
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
              { icon: FiGlobe, name: 'Web Search Fallback', desc: 'Autonomous internet search via Tavily API for out-of-domain queries, triggered after Human-in-the-Loop permission.', color: '#38bdf8' },
              { icon: FiCpu, name: 'Generator', desc: 'LLM with multi-version synthesis: compares 1961 vs 2025 Act provisions. Cautious RAG policy with banned-phrase guardrails. Confidence scoring.', color: 'var(--green)' },
              { icon: FiActivity, name: 'Hallucination Guard', desc: 'Post-generation check: is the answer grounded in retrieved chunks? If not → fallback. Confidence < 40% → reject.', color: 'var(--red)' },
              { icon: FiGitBranch, name: 'PostProcess', desc: 'Save Q&A to MongoDB (sliding window), log to Langfuse, cache response in Redis (1hr TTL). Feedback tracking.', color: 'var(--amber)' },
              { icon: FiZap, name: 'Fallback', desc: 'Circuit breaker (pybreaker): 3 API failures → circuit opens → graceful fallback message. No crash, no hang.', color: 'var(--text-muted)' },
            ].map((node, i) => (
              <FadeIn key={node.name} delay={i * 0.1}>
              <div className="glass-card" style={{ padding: '24px 20px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
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
              </FadeIn>
            ))}
          </div>
        </div>
      </section>

      {/* ===== OMNICHANNEL DEPLOYMENT ===== */}
      <section id="omnichannel" style={{ padding: '80px 40px', borderTop: '1px solid var(--border)' }}>
        <FadeIn delay={0}>
        <div style={{ maxWidth: 960, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '6px 16px', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--accent)', border: '1px solid rgba(255,51,51,0.2)', borderRadius: '100px', marginBottom: '20px', background: 'rgba(255,51,51,0.05)' }}>
              <FiGlobe size={12} /> Decoupled Architecture
            </span>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '12px' }}>Omnichannel <span style={{ color: 'var(--accent)' }}>Deployment</span></h2>
            <p style={{ fontSize: '0.93rem', color: 'var(--text-secondary)', maxWidth: '520px', margin: '0 auto', lineHeight: 1.6 }}>A single headless Agentic Brain serving users seamlessly across multiple interfaces.</p>
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
            {/* Web Interface */}
            <div className="glass-card" style={{ padding: '32px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
              <div style={{ background: 'rgba(56, 189, 248, 0.1)', padding: '16px', borderRadius: '50%', marginBottom: '20px' }}>
                <FiGrid size={28} color="#38bdf8" />
              </div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '12px' }}>React Web Interface</h3>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>Secure React SPA with Google OAuth 2.0. Features streaming responses, interactive markdown rendering, citation links, and Human-in-the-Loop chunk reviewing.</p>
            </div>

            {/* WhatsApp Integration */}
            <div className="glass-card" style={{ padding: '32px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', border: '1px solid rgba(37, 211, 102, 0.2)' }}>
              <div style={{ background: 'rgba(37, 211, 102, 0.1)', padding: '16px', borderRadius: '50%', marginBottom: '20px' }}>
                <FiMessageSquare size={28} color="#25D366" />
              </div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '12px' }}>WhatsApp Integration (Webhook)</h3>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>Asynchronous native WhatsApp API webhooks. Retains full multi-turn conversational memory, confidence-aware routing, and adaptive fallback logic on mobile.</p>
            </div>
          </div>
        </div>
        </FadeIn>
      </section>

      {/* ===== LIVE DEMO VIDEO ===== */}
      <section id="demo" style={{ padding: '80px 40px', borderTop: '1px solid var(--border)' }}>
        <FadeIn delay={0}>
        <div style={{ maxWidth: 960, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '6px 16px', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--accent)', border: '1px solid rgba(255,51,51,0.2)', borderRadius: '100px', marginBottom: '20px', background: 'var(--accent-glow)' }}>
              <span style={{ fontSize: '12px' }}>▶</span> Live Demo
            </span>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '12px' }}>See It In <span style={{ color: 'var(--accent)' }}>Action</span></h2>
            <p style={{ fontSize: '0.93rem', color: 'var(--text-secondary)', maxWidth: '520px', margin: '0 auto', lineHeight: 1.6 }}>Watch the AI parse legal and financial queries in real-time with streaming responses and source-grounded citations.</p>
          </div>
          <div style={{ position: 'relative', borderRadius: '16px', border: '1px solid rgba(255,51,51,0.15)', background: 'linear-gradient(180deg, rgba(22,27,38,0.5) 0%, rgba(10,13,18,0.9) 100%)', padding: '6px', boxShadow: '0 0 60px rgba(255,51,51,0.06), 0 20px 60px rgba(0,0,0,0.5)', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', top: 0, left: '15%', right: '15%', height: '1px', background: 'radial-gradient(circle, rgba(255,51,51,0.3) 0%, transparent 100%)', zIndex: 2 }} />
            <div style={{ position: 'relative', width: '100%', paddingBottom: '56.25%', height: 0, borderRadius: '12px', overflow: 'hidden' }}>
              <iframe src="https://player.cloudinary.com/embed/?cloud_name=dra6lzzb9&public_id=bot_response_k79sbj" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none', borderRadius: '12px', display: 'block' }} allow="autoplay; fullscreen; encrypted-media; picture-in-picture" allowFullScreen frameBorder="0" title="Live Bot Response Demo" />
            </div>
          </div>
          <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '0.78rem', color: 'var(--text-muted)', letterSpacing: '0.5px' }}>Real-time RAG pipeline response · Streaming · Source verification against PDF</p>
        </div>
        </FadeIn>
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
            <FadeIn delay={0.1}>
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
            </FadeIn>

            {/* Parent-Child Chunking */}
            <FadeIn delay={0.2}>
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
            </FadeIn>

            {/* MRL Embeddings */}
            <FadeIn delay={0.3}>
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
            </FadeIn>

            {/* SHA-256 + Deterministic IDs */}
            <FadeIn delay={0.4}>
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
            </FadeIn>

            {/* Backend Security */}
            <FadeIn delay={0.5}>
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
            </FadeIn>

            {/* HITL */}
            <FadeIn delay={0.6}>
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
            </FadeIn>
          </div>
        </div>
      </section>

      {/* ===== OPEN SOURCE MODEL ===== */}
      <section id="opensource" className="opensource-section" style={{ padding: '80px 40px', background: '#0a0a0a', borderTop: '1px solid #2a2a2a' }}>
        <div style={{ maxWidth: '900px', margin: '0 auto' }}>
          
          <p style={{ color: 'var(--accent)', fontSize: '12px', letterSpacing: '3px', textTransform: 'uppercase', marginBottom: '12px' }}>qLoRA Fine-Tuned By Ambuj Kumar Tripathi</p>
          <h2 style={{ color: '#ffffff', fontSize: '36px', fontWeight: '700', marginBottom: '8px' }}>Indian Legal LLM</h2>
          <p style={{ color: '#a3a3a3', fontSize: '13px', marginBottom: '16px', letterSpacing: '1px' }}>Designed & Fine-tuned by <span style={{ color: 'var(--accent)' }}>Ambuj Kumar Tripathi</span> · invincibleambuj</p>
          <p style={{ color: '#f3f4f6', fontSize: '15px', marginBottom: '48px', lineHeight: '1.6', maxWidth: '680px' }}>Fine-tuned a family of Llama 3 models (1B, 3B, and 8B) on 14,543 Indian Legal examples — IPC, CrPC & Constitution of India using 2x NVIDIA T4 GPUs. Open-source and highly optimized for consumer hardware.</p>

          <div className="opensource-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginBottom: '32px' }}>
            
            <a href="https://huggingface.co/invincibleambuj" target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '24px' }} onMouseOver={(e) => e.currentTarget.style.borderColor='var(--accent)'} onMouseOut={(e) => e.currentTarget.style.borderColor='#222'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span style={{ fontSize: '16px' }}>🤗</span>
                  <span style={{ color: 'var(--accent)', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase' }}>Hugging Face</span>
                </div>
                <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', margin: '0 0 8px 0' }}>Model Collection</h3>
                <p style={{ color: '#555', fontSize: '13px', margin: '0 0 16px 0', lineHeight: '1.5' }}>Access all 1B, 3B, and 8B fine-tuned legal models directly.</p>
                <span style={{ color: 'var(--accent)', fontSize: '12px' }}>View on Hugging Face →</span>
              </div>
            </a>

            <a href="https://huggingface.co/invincibleambuj/Ambuj-Tripathi-Indian-Legal-Llama-GGUF" target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '24px' }} onMouseOver={(e) => e.currentTarget.style.borderColor='var(--accent)'} onMouseOut={(e) => e.currentTarget.style.borderColor='#222'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span style={{ fontSize: '16px' }}>📦</span>
                  <span style={{ color: 'var(--accent)', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase' }}>GGUF</span>
                </div>
                <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', margin: '0 0 8px 0' }}>Run Locally</h3>
                <p style={{ color: '#555', fontSize: '13px', margin: '0 0 16px 0', lineHeight: '1.5' }}>Download & run on CPU. No GPU needed. 807 MB.</p>
                <span style={{ color: 'var(--accent)', fontSize: '12px' }}>Download GGUF →</span>
              </div>
            </a>

            <a href="https://lmstudio.ai" target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '24px' }} onMouseOver={(e) => e.currentTarget.style.borderColor='var(--accent)'} onMouseOut={(e) => e.currentTarget.style.borderColor='#222'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span style={{ fontSize: '16px' }}>🖥️</span>
                  <span style={{ color: 'var(--accent)', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase' }}>LM Studio</span>
                </div>
                <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', margin: '0 0 8px 0' }}>Desktop App</h3>
                <p style={{ color: '#555', fontSize: '13px', margin: '0 0 16px 0', lineHeight: '1.5' }}>Search & chat locally. No code required.</p>
                <span style={{ color: 'var(--accent)', fontSize: '12px' }}>Open in LM Studio →</span>
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

          <p style={{ color: '#aaa', fontSize: '12px', marginTop: '20px', textAlign: 'center', letterSpacing: '0.5px' }}>Built with Llama 3.2 · Fine-tuned by <strong style={{ color: 'var(--accent)' }}>Ambuj Kumar Tripathi</strong> · Llama 3.2 Community License</p>

          <div style={{ marginTop: '60px', borderTop: '1px solid #1e1e1e', paddingTop: '40px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '24px' }}>
              <span style={{ fontSize: '20px' }}>🐦</span>
              <h3 style={{ color: '#fff', fontSize: '18px', fontWeight: '600', letterSpacing: '1px' }}>Recognized by Hugging Face</h3>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
              <blockquote className="twitter-tweet" data-theme="dark">
                <p lang="en" dir="ltr">Meet Ambuj-Tripathi-Indian-Legal-Llama-GGUF: a specialized AI model fine-tuned for Indian law. This isn&#39;t just another chatbot. It&#39;s a legal assistant trained to understand the nuances of Indian statutes, case law, and legal language. A game-changer for legal tech in India. <a href="https://t.co/SkLzeaDgpE">pic.twitter.com/SkLzeaDgpE</a></p>&mdash; Hugging Models (@HuggingModels) <a href="https://x.com/HuggingModels/status/2044027666324697451?ref_src=twsrc%5Etfw">April 14, 2026</a>
              </blockquote>
            </div>
          </div>
        </div>
      </section>


      <section id="engineer" style={{
        padding: '80px 40px',
        borderTop: '1px solid rgba(255,51,51, 0.1)',
        textAlign: 'center',
        position: 'relative',
        background: '#0a0a0a',
        overflow: 'hidden',
      }}>
        {/* Accent Gradients (Matched to Hero Deep Red) */}
        <div style={{ position: 'absolute', top: 0, left: '50%', transform: 'translateX(-50%)', width: '120vw', height: '100%', background: 'radial-gradient(circle at 50% 0%, rgba(220, 38, 38, 0.28) 0%, transparent 65%)', filter: 'blur(60px)', pointerEvents: 'none' }} />
        
        <div style={{ maxWidth: 720, margin: '0 auto', position: 'relative', zIndex: 2 }}>
          <div style={{
            display: 'inline-block', padding: '6px 16px', borderRadius: 20,
            background: 'var(--accent-glow)', border: '1px solid rgba(255,51,51,0.2)',
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
            <a href="https://ambuj-ai-portfolio.vercel.app" target="_blank" rel="noreferrer"
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

      {/* ══════════════════ FAT FOOTER ══════════════════ */}
      <footer id="about" style={{ padding: '5rem 4rem 3rem 4rem', background: '#0a0a0a', borderTop: '1px solid rgba(255,51,51, 0.2)', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', gap: '3rem' }}>
              
              {/* Left Column: Logo & Copyright */}
              <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '300px', flex: 1.5, minWidth: '250px' }}>
                  <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: 700, fontSize: '1.4rem', color: '#fff', letterSpacing: '-0.5px' }}>FinancialParser<span style={{ color: 'var(--accent)' }}>AI</span></span>
                      </div>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.5rem', letterSpacing: '0.5px' }}>
                        Adaptive ReAct • LangGraph • LLMOps
                      </p>
                      <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                          <a href="https://www.linkedin.com/in/ambuj-tripathi-042b4a118/" target="_blank" rel="noreferrer" style={{ color: '#a1a1aa', transition: 'color 0.2s' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='#a1a1aa'}><FaLinkedin size={22} /></a>
                          <a href="https://x.com/Ambuj_KTripathi" target="_blank" rel="noreferrer" style={{ color: '#a1a1aa', transition: 'color 0.2s' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='#a1a1aa'}><FaXTwitter size={22} /></a>
                          <a href="https://github.com/Ambuj123-lab" target="_blank" rel="noreferrer" style={{ color: '#a1a1aa', transition: 'color 0.2s' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='#a1a1aa'}><FaGithub size={22} /></a>
                          <a href="https://medium.com/@ambuj_tripathi" target="_blank" rel="noreferrer" style={{ color: '#a1a1aa', transition: 'color 0.2s' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='#a1a1aa'}><FaMedium size={22} /></a>
                      </div>
                  </div>

                  <div style={{ marginTop: 'auto' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '1rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                          <span style={{ color: 'var(--text-secondary)' }}>Version: <span style={{ color: '#fff' }}>v2.0</span></span>
                          <span style={{ color: 'var(--text-secondary)' }}>Deployment: <span style={{ color: '#fff' }}>Render / AWS</span></span>
                          <span style={{ color: 'var(--text-secondary)' }}>Last Updated: <span style={{ color: '#fff' }}>July 2026</span></span>
                          <span style={{ color: 'var(--text-secondary)' }}>API Uptime: <a href="https://stats.uptimerobot.com/4tYmSQnuBE" target="_blank" rel="noreferrer" style={{ color: 'var(--accent)', textDecoration: 'none' }} onMouseOver={e=>e.target.style.textDecoration='underline'} onMouseOut={e=>e.target.style.textDecoration='none'}>{uptimeData ? `${uptimeData.uptime} • ${uptimeData.latency}` : '--%'}</a></span>
                      </div>
                      <p style={{ marginBottom: '1rem', fontSize: '0.85rem' }}>&copy; Designed & Engineered by Ambuj Kumar Tripathi</p>
                  </div>
              </div>

              {/* Columns Container */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '2rem', flex: 3 }}>
                  {/* Column 1 */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <h4 style={{ color: '#fff', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.95rem' }}>Platform</h4>
                      <a href="#pipeline" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Union Budget Parsing</a>
                      <a href="#pipeline" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>RBI & Tax Laws</a>
                      <a href="#pipeline" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Vector Embeddings</a>
                  </div>

                  {/* Column 2 */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <h4 style={{ color: '#fff', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.95rem' }}>Solutions</h4>
                      <a href="#" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Researchers</a>
                      <a href="#" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Legal Professionals</a>
                      <a href="#" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Finance Students</a>
                  </div>
                  
                  {/* Column - Ecosystem */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <h4 style={{ color: '#fff', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.95rem' }}>Ecosystem</h4>
                      <a href="https://indian-legal-ai-expert.onrender.com/" target="_blank" rel="noreferrer" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Indian Legal AI Expert</a>
                      <a href="https://citizen-safety-ai-assistant.vercel.app/" target="_blank" rel="noreferrer" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Citizen Safety AI</a>
                      <a href="https://ambuj-ai-portfolio.vercel.app" target="_blank" rel="noreferrer" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>AI Portfolio Hub</a>
                  </div>

                  {/* Column 3 */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <h4 style={{ color: '#fff', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.95rem' }}>Resources</h4>
                      <a href="https://github.com/Ambuj123-lab" target="_blank" rel="noreferrer" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>GitHub</a>
                      <a href="https://ambuj-rag-docs.netlify.app/" target="_blank" rel="noreferrer" style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Documentation</a>
                  </div>

                  {/* Column 4 */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <h4 style={{ color: '#fff', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.95rem' }}>Legal</h4>
                      <a href="#legal" onClick={(e) => { e.preventDefault(); setLegalModal('PRIVACY'); }} style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Privacy Policy</a>
                      <a href="#legal" onClick={(e) => { e.preventDefault(); setLegalModal('TOS'); }} style={{ color: 'inherit', textDecoration: 'none' }} onMouseOver={e=>e.target.style.color='#fff'} onMouseOut={e=>e.target.style.color='var(--text-muted)'}>Terms of Service</a>
                  </div>
              </div>
          </div>
      </footer>

      {/* ══════════════════ LEGAL MODALS ══════════════════ */}
      {legalModal && (
          <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', zIndex: 100000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1.5rem', backdropFilter: 'blur(5px)' }} onClick={() => setLegalModal(null)}>
              <div className="legal-modal-container" style={{ background: '#0a0a0a', border: '1px solid rgba(255,51,51, 0.2)', borderRadius: '12px', padding: '0', width: '100%', maxWidth: '800px', maxHeight: '85vh', overflowY: 'auto', position: 'relative', color: '#e5e7eb', boxShadow: '0 20px 40px rgba(0,0,0,0.7)' }} onClick={(e) => e.stopPropagation()}>
                  
                  <div style={{ position: 'sticky', top: 0, right: 0, display: 'flex', justifyContent: 'flex-end', padding: '1rem', background: 'linear-gradient(to bottom, #0a0a0a 80%, transparent)', zIndex: 10 }}>
                      <button onClick={() => setLegalModal(null)} style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: 'var(--text-muted)', width: '32px', height: '32px', borderRadius: '50%', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', transition: 'all 0.2s' }} onMouseOver={e=>{e.target.style.background='rgba(255,255,255,0.1)'; e.target.style.color='#fff'}} onMouseOut={e=>{e.target.style.background='rgba(255,255,255,0.05)'; e.target.style.color='var(--text-muted)'}}>
                          &times;
                      </button>
                  </div>
                  
                  <div style={{ padding: '0 2rem 3rem 2rem' }}>
                      {legalModal === 'TOS' && (
                          <div>
                              <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                                  <h2 style={{ fontSize: '2rem', fontWeight: 700, color: '#fff', marginBottom: '0.5rem', letterSpacing: '-0.5px' }}>Terms of Service</h2>
                                  <p style={{ color: 'var(--accent)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '1rem' }}>Effective July 2026</p>
                              </div>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'rgba(255,255,255,0.05)', borderRadius: '12px', overflow: 'hidden' }}>
                                  <div style={{ background: '#111', padding: '1.5rem 2rem' }}>
                                      <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>🚫 Not Financial Advice</h3>
                                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>This platform provides AI-driven analysis of SEC filings and earnings calls for educational and research purposes only. The insights generated do not constitute financial, investment, or trading advice.</p>
                                  </div>
                                  <div style={{ background: '#111', padding: '1.5rem 2rem' }}>
                                      <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>🎓 Learning & Development Use Only</h3>
                                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>This platform is provided exclusively for educational and learning purposes. There is no exchange of money or commercial service involved. Users must verify all AI-generated financial data with official SEC sources.</p>
                                  </div>
                              </div>
                          </div>
                      )}

                      {legalModal === 'PRIVACY' && (
                          <div>
                              <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                                  <h2 style={{ fontSize: '2rem', fontWeight: 700, color: '#fff', marginBottom: '0.5rem', letterSpacing: '-0.5px' }}>Privacy Policy</h2>
                                  <p style={{ color: 'var(--accent)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '1rem' }}>Effective July 2026</p>
                              </div>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'rgba(255,255,255,0.05)', borderRadius: '12px', overflow: 'hidden' }}>
                                  <div style={{ background: '#111', padding: '1.5rem 2rem' }}>
                                      <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>📊 Financial Query Processing</h3>
                                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>When you query the Financial Parser regarding stocks or companies, the queries are processed securely. We do not link these queries to your real identity or track your personal investment interests.</p>
                                  </div>
                                  <div style={{ background: '#111', padding: '1.5rem 2rem' }}>
                                      <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>🗑️ No Retention Policy</h3>
                                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>We do not permanently store your chat history or financial analysis prompts. Data is processed in-memory for RAG retrieval and instantly discarded.</p>
                                  </div>
                              </div>
                          </div>
                      )}
                  </div>
              </div>
          </div>
      )}

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
        
        /* ═══ TABLET (max 768px) ═══ */
        @media (max-width: 768px) {
          nav { padding: 12px 16px !important; }
          .desktop-nav { display: none !important; }
          .hamburger-btn { display: block !important; }

          /* Hero */
          section { padding-left: 16px !important; padding-right: 16px !important; }
          h1 { font-size: clamp(1.8rem, 6vw, 2.5rem) !important; line-height: 1.2 !important; }
          h2 { font-size: 1.5rem !important; }

          /* Grids → single column */
          div[style*='grid-template-columns: 1fr 1fr'] { grid-template-columns: 1fr !important; }
          div[style*='repeat(auto-fit'] { grid-template-columns: 1fr !important; }
          .opensource-grid { grid-template-columns: 1fr !important; }

          /* Stats row */
          div[style*='space-around'] { gap: 16px !important; }
          div[style*='space-around'] > div > div:first-child { font-size: 1.8rem !important; }

          /* Footer */
          footer { padding: 2.5rem 1.2rem 2rem 1.2rem !important; }
          footer > div { flex-direction: column !important; gap: 2rem !important; }

          /* Top badge banner */
          div[style*='inline-flex'][style*='gap: 16'] { flex-direction: column !important; gap: 8px !important; }
          div[style*='width: 40px'][style*='height: 1px'] { display: none !important; }
        }

        /* ═══ SMALL PHONES (max 480px) ═══ */
        @media (max-width: 480px) {
          h1 { font-size: 1.6rem !important; letter-spacing: -0.5px !important; }
          h2 { font-size: 1.3rem !important; }
          section { padding-top: 48px !important; padding-bottom: 48px !important; }

          /* Hero buttons stack */
          div[style*='gap: 14'][style*='flex-wrap'] { flex-direction: column !important; width: 100% !important; }
          div[style*='gap: 14'][style*='flex-wrap'] > a,
          div[style*='gap: 14'][style*='flex-wrap'] > button { width: 100% !important; text-align: center !important; justify-content: center !important; }

          /* Model badges row */
          div[style*='gap: 16px'][style*='marginTop: 60px'] { gap: 12px !important; margin-top: 32px !important; }
          div[style*='gap: 16px'][style*='marginTop: 60px'] > a > div:first-child { width: 40px !important; height: 40px !important; font-size: 18px !important; }

          /* Stats */
          div[style*='space-around'] { flex-direction: column !important; gap: 20px !important; }
        }
        .hero-docs-btn:target {
          animation: highlightBlink 2s ease-in-out;
        }
        @keyframes highlightBlink {
          0%, 100% { box-shadow: 0 0 0 0 transparent; }
          20%, 60% { box-shadow: 0 0 0 8px rgba(255,51,51, 0.4); border-color: var(--accent); }
        }
      `}</style>
      {/* ===== BACK TO TOP BUTTON ===== */}
      <button
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          style={{
              position: 'fixed',
              bottom: '24px',
              right: '24px',
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: 'rgba(220, 38, 38, 0.1)',
              border: '1px solid rgba(220, 38, 38, 0.3)',
              color: '#dc2626',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              zIndex: 9999,
              opacity: showBackToTop ? 1 : 0,
              visibility: showBackToTop ? 'visible' : 'hidden',
              transform: showBackToTop ? 'scale(1)' : 'scale(0.8)',
              transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
              boxShadow: '0 8px 32px rgba(220, 38, 38, 0.1)',
              backdropFilter: 'blur(8px)',
          }}
          onMouseOver={(e) => {
              e.currentTarget.style.background = 'rgba(220, 38, 38, 0.2)';
              e.currentTarget.style.transform = 'scale(1.1)';
          }}
          onMouseOut={(e) => {
              e.currentTarget.style.background = 'rgba(220, 38, 38, 0.1)';
              e.currentTarget.style.transform = 'scale(1)';
          }}
          aria-label="Back to Top"
      >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 19V5M5 12l7-7 7 7"/>
          </svg>
      </button>

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
