import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import {
  FiSend, FiMenu, FiLogOut, FiUploadCloud, FiTrash2,
  FiThumbsUp, FiThumbsDown, FiCpu, FiSettings, FiFile,
  FiChevronRight, FiDatabase, FiBookOpen
} from 'react-icons/fi'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [docsOpen, setDocsOpen] = useState(false)
  const [nodeSteps, setNodeSteps] = useState([])
  const [sourcesExpanded, setSourcesExpanded] = useState({})
  const [stats, setStats] = useState(null)
  const [statsExpanded, setStatsExpanded] = useState(false)
  const chatEndRef = useRef(null)

  // Auto-close sidebar on mobile load
  useEffect(() => {
    if (window.innerWidth <= 768) setSidebarOpen(false)
  }, [])

  // Fetch stats and history on load
  useEffect(() => {
    api.get('/common/stats')
      .then(res => setStats(res.data))
      .catch(() => {})

    api.get('/chat/history')
      .then(res => {
        if (res.data?.history?.length > 0) {
          setMessages(res.data.history.map(m => ({
            role: m.role,
            content: m.content,
            sources: m.sources || [],
            timestamp: m.timestamp,
            confidence: m.confidence || 0,
            pii_detected: m.pii_detected || false,
            pii_entities: m.pii_entities || []
          })))
        }
      })
      .catch(() => {})
  }, [])

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = async (overrideText) => {
    const textToSubmit = typeof overrideText === 'string' ? overrideText.trim() : input.trim()
    if (!textToSubmit || loading) return
    const question = textToSubmit
    setInput('')

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setLoading(true)

    try {
      // Use SSE streaming endpoint
      const token = localStorage.getItem('token')
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ question }),
      })

      if (!response.ok) {
        throw new Error(response.statusText || 'Request failed')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      // Create placeholder bot message that we'll update as tokens arrive
      const botMsg = {
        role: 'assistant',
        content: '',
        sources: [],
        confidence: 0,
        _question: question,
        _streaming: true,
      }
      setMessages(prev => [...prev, botMsg])
      setLoading(false) // Hide thinking dots, show streaming text

      let fullAnswer = ''
      let sources = []
      let confidence = 0
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() // Keep incomplete line in buffer

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const dataStr = line.slice(6).trim()
          if (dataStr === '[DONE]') continue

          try {
            const event = JSON.parse(dataStr)

            if (event.type === 'node') {
              // Node Highlighter — show pipeline step progress
              setNodeSteps(prev => {
                const existing = prev.find(n => n.id === event.id)
                if (existing) {
                  return prev.map(n => n.id === event.id ? { ...n, status: event.status } : n)
                }
                return [...prev, { id: event.id, label: event.label, icon: event.icon, status: event.status }]
              })
            } else if (event.type === 'meta') {
              sources = event.sources || []
              confidence = event.confidence || 0
              const pii_detected = event.pii_detected || false
              const pii_entities = event.pii_entities || []
              setNodeSteps([]) // Clear node steps when answer starts
              setMessages(prev => {
                const updated = [...prev]
                const last = updated[updated.length - 1]
                if (last?.role === 'assistant') {
                  updated[updated.length - 1] = {
                    ...last,
                    sources,
                    confidence,
                    pii_detected,
                    pii_entities,
                    showPiiLogs: false
                  }
                }
                return updated
              })
            } else if (event.type === 'token') {
              fullAnswer += event.content
              // Update the last message in-place for smooth rendering
              setMessages(prev => {
                const updated = [...prev]
                const last = updated[updated.length - 1]
                if (last?.role === 'assistant') {
                  updated[updated.length - 1] = {
                    ...last,
                    content: fullAnswer,
                  }
                }
                return updated
              })
            } else if (event.type === 'cached' || event.type === 'complete') {
              // Instant display for cached/non-RAG responses
              fullAnswer = event.answer || ''
              sources = event.sources || []
              confidence = event.confidence || 0
              const pii_detected = event.pii_detected || false
              const pii_entities = event.pii_entities || []
              setNodeSteps([]) // Clear node steps when answer starts for quick/fallback routes
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  content: fullAnswer,
                  sources,
                  confidence,
                  pii_detected,
                  pii_entities,
                  showPiiLogs: false,
                  _streaming: false,
                }
                return updated
              })
            } else if (event.type === 'done') {
              // Mark streaming complete
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  _streaming: false,
                }
                return updated
              })
            }
          } catch (e) { /* skip malformed JSON */ }
        }
      }

      // Final cleanup — ensure streaming flag is off
      setMessages(prev => {
        const updated = [...prev]
        if (updated[updated.length - 1]?.role === 'assistant') {
          updated[updated.length - 1]._streaming = false
        }
        return updated
      })

    } catch (err) {
      setLoading(false)
      const detail = err.message || 'Something went wrong. Please try again.'
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `⚠️ ${detail}`,
        sources: [], confidence: 0,
      }])
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleFeedback = async (msg, rating) => {
    try {
      await api.post('/feedback', {
        question: msg._question || '',
        response: msg.content.substring(0, 500),
        rating
      })
      setMessages(prev => prev.map(m =>
        m === msg ? { ...m, feedbackGiven: rating } : m
      ))
    } catch (e) { /* ignore */ }
  }

  const clearHistory = async () => {
    try {
      await api.delete('/chat/history')
      setMessages([])
    } catch (e) { /* ignore */ }
  }

  return (
    <div className="app-layout">
      {/* ===== SIDEBAR ===== */}
      {sidebarOpen && (
        <div className="mobile-overlay hide-desktop" onClick={() => setSidebarOpen(false)} />
      )}
      <aside className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
        {/* Logo */}
        <div style={{
          padding: '18px 20px', borderBottom: '1px solid var(--border)',
          display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <FiCpu size={20} color="var(--accent)" />
          <span style={{ fontWeight: 700, fontSize: '0.9rem' }}>AFP</span>
        </div>

        {/* User Info */}
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: 36, height: 36, borderRadius: '50%', background: 'var(--accent)', color: '#000',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600, fontSize: '1.1rem',
            overflow: 'hidden', flexShrink: 0
          }}>
            {user?.picture ? (
              <img src={user.picture} alt="DP" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              user?.name ? user.name[0].toUpperCase() : 'U'
            )}
          </div>
          <div style={{ overflow: 'hidden' }}>
            <p style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: 2, whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
              {user?.name || 'User'}
            </p>
            <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
              {user?.email || ''}
            </p>
            {user?.is_admin && (
              <span className="tag tag-approved" style={{ marginTop: 6, display: 'inline-block' }}>
                Admin
              </span>
            )}
          </div>
        </div>

        {/* Actions */}
        <div style={{ padding: '12px 16px', flex: 1, display: 'flex', flexDirection: 'column', gap: 4 }}>
          {/* Knowledge Base Health Accordion */}
          <div style={{ marginBottom: 12, borderBottom: '1px solid var(--border)', paddingBottom: 12 }}>
            <button 
              onClick={() => setStatsExpanded(!statsExpanded)}
              style={{
                width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                background: 'transparent', border: 'none', color: 'var(--text-secondary)',
                padding: '6px 0', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 600
              }}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <FiDatabase size={14} color="var(--accent)" /> Knowledge Base Health
              </span>
              <FiChevronRight size={14} style={{ transform: statsExpanded ? 'rotate(90deg)' : 'none', transition: '0.2s' }} />
            </button>
            {statsExpanded && stats && (
              <div style={{ padding: '8px 0 0 20px', fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: 6 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Total Documents:</span> <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stats.total_files}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Total Vectors:</span> <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stats.total_chunks.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>System Status:</span> <span style={{ color: 'var(--success, #34A853)', fontWeight: 600 }}>● Active</span>
                </div>
              </div>
            )}
          </div>


          <SidebarBtn icon={FiUploadCloud} label="Upload PDF" onClick={() => document.getElementById('file-upload').click()} />
          <FileUploader />

          {user?.is_admin && (
            <SidebarBtn icon={FiSettings} label="Admin Panel" onClick={() => navigate('/admin')} />
          )}

          <SidebarBtn icon={FiBookOpen} label="Architecture Docs" onClick={() => setDocsOpen(true)} />

          <SidebarBtn icon={FiTrash2} label="Clear History" onClick={clearHistory} />
        </div>

        {/* Logout */}
        <div style={{ padding: '12px 16px', borderTop: '1px solid var(--border)' }}>
          <SidebarBtn icon={FiLogOut} label="Logout" onClick={logout} />
        </div>
      </aside>

      {/* ===== MAIN CHAT ===== */}
      <div className="main-content">
        {/* Top bar */}
        <div style={{
          padding: '12px 20px',
          borderBottom: '1px solid var(--border)',
          display: 'flex', alignItems: 'center', gap: 12,
          background: 'var(--bg-secondary)',
        }}>
          <button onClick={() => setSidebarOpen(!sidebarOpen)} style={{
            background: 'none', border: 'none', color: 'var(--text-secondary)',
            cursor: 'pointer', padding: 4,
          }}>
            <FiMenu size={20} />
          </button>
          <span style={{ fontWeight: 600, fontSize: '0.92rem' }}>Agentic Financial Parser</span>
          <span className="hide-mobile" style={{ fontSize: '0.75rem', color: 'var(--primary)', marginLeft: 'auto', fontFamily: 'var(--font-mono)', fontWeight: 600, letterSpacing: '0.3px', background: 'var(--bg-tertiary)', padding: '4px 10px', borderRadius: '4px', border: '1px solid var(--border)' }}>
            Agentic 8-Node RAG StateGraph | Engineered by Ambuj Kumar Tripathi
          </span>
        </div>

        {/* Messages Area */}
        <div style={{
          flex: 1, overflowY: 'auto', padding: '24px 20px',
          display: 'flex', flexDirection: 'column',
        }}>
          {messages.length === 0 && !loading && (
            <EmptyState onQuestionClick={(q) => sendMessage(q)} />
          )}

          {messages.map((msg, i) => (
            <div key={i}>
              {msg.role === 'user' ? (
                <div className="msg-user">{msg.content}</div>
              ) : (
                <div className={`msg-bot${msg._streaming ? ' streaming' : ''}`}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>

                  {/* Source Citations (Expandable) */}
                  {msg.sources?.length > 0 && (
                    <div style={{ marginTop: 12 }}>
                      <button
                        onClick={() => setSourcesExpanded(prev => ({ ...prev, [i]: !prev[i] }))}
                        className="sources-toggle"
                      >
                        <FiFile size={12} />
                        {msg.sources.length} source{msg.sources.length > 1 ? 's' : ''} cited
                        <FiChevronRight
                          size={12}
                          style={{
                            transform: sourcesExpanded[i] ? 'rotate(90deg)' : 'rotate(0)',
                            transition: 'transform 0.2s',
                          }}
                        />
                      </button>
                      {sourcesExpanded[i] && (
                        <div className="sources-expanded">
                          {msg.sources.map((s, j) => (
                            <span key={j} className="source-badge">
                              <FiFile size={11} /> {s}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Confidence Bar */}
                  {msg.confidence > 0 && (
                    <div style={{ marginTop: 12 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 4 }}>
                        <span>Confidence Score</span>
                        <span style={{ 
                          fontWeight: 600, 
                          color: msg.confidence >= 70 ? 'var(--green)' : msg.confidence >= 40 ? 'var(--amber)' : 'var(--red)'
                        }}>
                          {Math.round(msg.confidence)}%
                        </span>
                      </div>
                      <div className="confidence-bar">
                        <div className="confidence-fill" style={{
                          width: `${msg.confidence}%`,
                          background: msg.confidence >= 70 ? 'var(--green)' : msg.confidence >= 40 ? 'var(--amber)' : 'var(--red)',
                        }} />
                      </div>
                    </div>
                  )}

                  {/* PII Badge */}
                  {msg.pii_detected && (
                    <div style={{ marginTop: 12 }}>
                      <span
                        className="pii-badge clickable"
                        onClick={() => {
                          setMessages(prev => prev.map((m, idx) => idx === i ? { ...m, showPiiLogs: !m.showPiiLogs } : m))
                        }}
                        title="Click to view PII detection logs"
                        style={{ display: 'inline-block', marginBottom: msg.showPiiLogs ? 8 : 0 }}
                      >
                        🔒 PII Protected {msg.showPiiLogs ? '▲' : '▼'}
                      </span>
                      {msg.showPiiLogs && msg.pii_entities?.length > 0 && (
                        <div className="pii-logs-dropdown">
                          <div className="pii-logs-title">🛡️ Detection Logs</div>
                          {msg.pii_entities.map((entity, idx) => (
                            <div key={idx} className="pii-log-entry">
                              <span className="pii-entity-type">{entity.type}</span>
                              <span className="pii-entity-score">{Math.round((entity.score || 1) * 100)}% confidence</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Feedback Buttons */}
                  {msg.role === 'assistant' && !msg.feedbackGiven && !msg.is_fallback && (
                    <div className="feedback-row">
                      <button
                        className="feedback-btn"
                        onClick={() => handleFeedback(msg, 'helpful')}
                      >
                        <FiThumbsUp size={13} /> Helpful
                      </button>
                      <button
                        className="feedback-btn"
                        onClick={() => handleFeedback(msg, 'not_helpful')}
                      >
                        <FiThumbsDown size={13} /> Not helpful
                      </button>
                    </div>
                  )}

                  {msg.feedbackGiven && (
                    <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 6 }}>
                      ✓ Feedback recorded
                    </p>
                  )}
                </div>
              )}
            </div>
          ))}

          {/* Node Highlighter — pipeline step progress */}
          {(loading || nodeSteps.length > 0) && (
            <div className="msg-bot" style={{ minHeight: 60 }}>
              {nodeSteps.length > 0 ? (
                <div className="node-steps">
                  {nodeSteps.map(step => (
                    <div key={step.id} className={`node-step ${step.status}`}>
                      <span className="node-icon">{step.status === 'done' ? '✅' : step.icon}</span>
                      <span className="node-label">{step.label}</span>
                      {step.status === 'running' && (
                        <span className="node-spinner" />
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="thinking-indicator">
                  <div className="thinking-dots">
                    <span /><span /><span />
                  </div>
                  <span>Initializing pipeline...</span>
                </div>
              )}
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="chat-input-wrap">
          <input
            className="chat-input"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about Budget, Tax, PF, KYC, Constitution..."
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={!input.trim() || loading}
          >
            <FiSend size={18} />
          </button>
        </div>
      </div>

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


/* ===== SUB-COMPONENTS ===== */

function SidebarBtn({ icon: Icon, label, onClick }) {
  return (
    <button onClick={onClick} style={{
      display: 'flex', alignItems: 'center', gap: 10,
      padding: '10px 12px', borderRadius: 'var(--radius-sm)',
      background: 'transparent', border: 'none',
      color: 'var(--text-secondary)', cursor: 'pointer',
      fontSize: '0.85rem', width: '100%', textAlign: 'left',
      transition: 'background 0.2s',
    }}
      onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-tertiary)'}
      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
    >
      <Icon size={16} /> {label}
    </button>
  )
}

function FileUploader() {
  const handleUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await api.post('/upload/temp', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      alert(res.data.is_duplicate
        ? `⚡ Already indexed: ${file.name}`
        : `✅ Uploaded: ${file.name} — ${res.data.chunk_count} chunks for review`
      )
    } catch (err) {
      alert(`❌ Upload failed: ${err.response?.data?.detail || err.message || 'Unknown error'}`)
    }
  }

  return (
    <input
      id="file-upload"
      type="file"
      accept=".pdf"
      style={{ display: 'none' }}
      onChange={handleUpload}
    />
  )
}

function EmptyState({ onQuestionClick }) {
  return (
    <div style={{
      flex: 1, display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      textAlign: 'center', padding: 40,
    }}>
      <FiCpu size={48} color="var(--accent)" style={{ marginBottom: 20, opacity: 0.6 }} />
      <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 8, opacity: 0.8 }}>
        Agentic Financial Parser
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: 400, marginBottom: 28 }}>
        Parse and query Indian financial documents with an 8-node
        agentic RAG — cross-questioning, hallucination guard, HITL review.
      </p>
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10,
        maxWidth: 440,
      }}>
        {[
          'What are the new tax slabs in Budget 2026?',
          'Compare old vs new PF pension scheme',
          'RBI KYC rules for NRIs?',
          'Budget allocation for education sector'
        ].map(q => (
          <div key={q} onClick={() => onQuestionClick && onQuestionClick(q)} className="glass-card" style={{
            padding: '12px 14px', cursor: 'pointer',
            display: 'flex', alignItems: 'center', gap: 8,
            fontSize: '0.82rem', color: 'var(--text-secondary)',
          }}>
            <FiChevronRight size={13} color="var(--accent)" style={{ flexShrink: 0 }} />
            {q}
          </div>
        ))}
      </div>
    </div>
  )
}
