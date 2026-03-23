import { useState } from 'react'
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

export default function Landing() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [docsOpen, setDocsOpen] = useState(false)

  if (user) {
    navigate('/chat', { replace: true })
    return null
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
      {/* ===== NAVBAR ===== */}
      <nav style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '16px 40px',
        borderBottom: '1px solid var(--border)',
        background: 'rgba(12, 12, 20, 0.92)',
        backdropFilter: 'blur(12px)',
        position: 'sticky', top: 0, zIndex: 50,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <FiCpu size={22} color="var(--accent)" />
          <span style={{ fontWeight: 700, fontSize: '1.05rem', letterSpacing: '-0.3px' }}>
            Agentic Financial Parser
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
          <button onClick={() => setDocsOpen(true)} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: '0.88rem', cursor: 'pointer' }}>Documentation</button>
          <a href="#architecture" style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>Architecture</a>
          <a href="#depth" style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>Engineering</a>
          <a href="#engineer" style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>About</a>
          <a href={GOOGLE_AUTH_URL} className="btn-ghost" style={{
            padding: '8px 18px', fontSize: '0.84rem',
          }}>
            Sign In
          </a>
          {import.meta.env.DEV && (
            <button
              className="btn-ghost"
              style={{
                padding: '8px 18px', fontSize: '0.84rem',
                background: 'var(--accent)', color: '#000',
                border: 'none', borderRadius: '8px', cursor: 'pointer',
                fontWeight: 600,
              }}
              onClick={async () => {
                try {
                  const res = await fetch('http://localhost:8000/auth/dev-login', { method: 'POST' })
                  const data = await res.json()
                  if (data.access_token) {
                    login(data.access_token, data.user)
                    navigate('/chat')
                  }
                } catch (e) {
                  alert('Backend not running! Start: uvicorn app.main:app --port 8000')
                }
              }}
            >
              Dev Login
            </button>
          )}
        </div>
      </nav>

      {/* ===== HERO ===== */}
      <section style={{
        padding: '100px 40px 60px',
        textAlign: 'center',
        maxWidth: 920,
        margin: '0 auto',
        position: 'relative',
      }}>
        {/* Warm glow */}
        <div style={{
          position: 'absolute', top: '-80px', left: '50%', transform: 'translateX(-50%)',
          width: 500, height: 500,
          background: 'radial-gradient(circle, rgba(212,165,116,0.05) 0%, transparent 70%)',
          pointerEvents: 'none',
        }} />

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
          Parse Union Budget, Finance Bill, Tax Laws, PF/Pension Schemes, RBI KYC &amp;
          Constitution of India with an 8-node agentic RAG powered by LangGraph StateGraph —
          cross-questioning, hallucination guard, and human-in-the-loop chunk review.
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
          <button onClick={() => setDocsOpen(true)} className="btn-ghost" style={{ fontSize: '0.95rem', padding: '13px 28px' }}>
            View Architecture Docs
          </button>
          <a href="#architecture" className="btn-ghost" style={{ fontSize: '0.95rem', padding: '13px 28px' }}>
            Inside System
          </a>
        </div>
      </section>

      {/* ===== TECH STRIP ===== */}
      <section style={{
        display: 'flex', justifyContent: 'center', flexWrap: 'wrap',
        gap: '32px', padding: '30px 40px 50px',
      }}>
        {[
          'LangGraph StateGraph', 'Jina v3 MRL (256-dim)', 'Pinecone Serverless',
          'LlamaParse 3-Tier', 'FastAPI + Uvicorn', 'Circuit Breaker (pybreaker)'
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
              { icon: FiLayers, name: 'Retriever', desc: 'Dual Pinecone search with metadata filtering: core brain (is_temporary=false) + user temp (uploaded_by=email). Parent-Child Recursive Retrieval.', color: 'var(--accent)' },
              { icon: FiCpu, name: 'Generator', desc: 'LLM with parent-text context injection. Strict citation rules: every claim must reference [Source ID]. Confidence scoring.', color: 'var(--green)' },
              { icon: FiActivity, name: 'Hallucination Guard', desc: 'Post-generation check: is the answer grounded in retrieved chunks? If not → fallback. Confidence < 40% → reject.', color: 'var(--red)' },
              { icon: FiGitBranch, name: 'PostProcess', desc: 'Save Q&A to MongoDB (sliding window), log to Langfuse, cache response in Redis (1hr TTL). Feedback tracking.', color: 'var(--amber)' },
              { icon: FiZap, name: 'Fallback', desc: 'Circuit breaker (pybreaker): 3 API failures → circuit opens → graceful fallback message. No crash, no hang.', color: 'var(--text-muted)' },
            ].map(node => (
              <div key={node.name} className="glass-card" style={{ padding: '22px 20px' }}>
                <node.icon size={22} color={node.color} style={{ marginBottom: 10 }} />
                <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 6 }}>{node.name}</h4>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>{node.desc}</p>
              </div>
            ))}
          </div>
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

      {/* ===== ENGINEER ===== */}
      <section id="engineer" style={{
        padding: '80px 40px',
        borderTop: '1px solid var(--border)',
        textAlign: 'center',
      }}>
        <div style={{ maxWidth: 720, margin: '0 auto' }}>
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
        padding: '24px 40px',
        borderTop: '1px solid var(--border)',
        textAlign: 'center',
      }}>
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
        @media (max-width: 768px) {
          nav { padding: 12px 16px !important; }
          nav > div:last-child a:not(.btn-ghost) { display: none; }
          section { padding-left: 16px !important; padding-right: 16px !important; }
          h1 { font-size: 1.8rem !important; }
          div[style*='grid-template-columns: 1fr 1fr'] { grid-template-columns: 1fr !important; }
          div[style*='repeat(auto-fit'] { grid-template-columns: 1fr 1fr !important; }
        }
        @media (max-width: 480px) {
          div[style*='repeat(auto-fit'] { grid-template-columns: 1fr !important; }
          div[style*='gap: "24px"'] { gap: 12px !important; }
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
