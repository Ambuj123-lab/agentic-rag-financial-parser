import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'
import {
  FiRefreshCw, FiTrash2, FiCheck, FiX, FiBarChart2,
  FiUsers, FiDatabase, FiThumbsUp, FiArrowLeft, FiFile,
  FiCpu, FiActivity
} from 'react-icons/fi'

export default function Admin() {
  const { user, logout } = useAuth()
  const [stats, setStats] = useState(null)
  const [chunks, setChunks] = useState([])
  const [syncing, setSyncing] = useState(false)
  const [syncResult, setSyncResult] = useState(null)
  const [tab, setTab] = useState('dashboard')  // dashboard | chunks

  useEffect(() => {
    loadStats()
    loadChunks()
  }, [])

  const loadStats = async () => {
    try {
      const res = await api.get('/admin/stats')
      setStats(res.data)
    } catch (e) { /* ignore */ }
  }

  const loadChunks = async () => {
    try {
      const res = await api.get('/admin/chunks')
      setChunks(res.data)
    } catch (e) { /* ignore */ }
  }

  const runSync = async () => {
    setSyncing(true)
    setSyncResult(null)
    try {
      const res = await api.post('/admin/sync')
      setSyncResult(res.data.results)
      loadStats()
    } catch (e) {
      setSyncResult({ errors: [e.response?.data?.detail || 'Sync failed'] })
    } finally {
      setSyncing(false)
    }
  }

  const handleChunkAction = async (chunkId, action) => {
    try {
      await api.post('/admin/chunks/approve', { chunk_id: chunkId, action })
      setChunks(prev => prev.filter(c => c.chunk_id !== chunkId))
      loadStats()
    } catch (e) { /* ignore */ }
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
      {/* Top Bar */}
      <div style={{
        padding: '14px 28px',
        borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', gap: 14,
        background: 'var(--bg-secondary)',
      }}>
        <a href="/chat" style={{ color: 'var(--text-secondary)', display: 'flex' }}>
          <FiArrowLeft size={18} />
        </a>
        <FiCpu size={20} color="var(--accent)" />
        <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>Admin Panel</span>
        <span style={{
          fontSize: '0.72rem', color: 'var(--text-muted)',
          marginLeft: 'auto', fontFamily: 'var(--font-mono)',
        }}>
          {user?.email}
        </span>
      </div>

      <div style={{ maxWidth: 1000, margin: '0 auto', padding: '28px 20px' }}>
        {/* Tab Switcher */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 28 }}>
          {['dashboard', 'chunks'].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: '8px 20px', borderRadius: 'var(--radius-sm)',
              background: tab === t ? 'var(--accent-glow)' : 'transparent',
              border: `1px solid ${tab === t ? 'var(--border-active)' : 'var(--border)'}`,
              color: tab === t ? 'var(--accent)' : 'var(--text-secondary)',
              cursor: 'pointer', fontSize: '0.85rem', fontWeight: 500,
              textTransform: 'capitalize',
            }}>
              {t === 'dashboard' ? <><FiBarChart2 size={14} style={{ marginRight: 6, verticalAlign: 'middle' }} /> Dashboard</> :
               <><FiDatabase size={14} style={{ marginRight: 6, verticalAlign: 'middle' }} /> Pending Chunks</>}
            </button>
          ))}
        </div>

        {/* DASHBOARD TAB */}
        {tab === 'dashboard' && (
          <>
            {/* Stats Cards */}
            <div style={{
              display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: 14, marginBottom: 28,
            }}>
              <StatCard icon={FiUsers} label="Active Users" value={stats?.active_users ?? '—'} color="var(--accent)" />
              <StatCard icon={FiDatabase} label="Total Chunks" value={stats?.total_chunks ?? '—'} color="var(--green)" />
              <StatCard icon={FiActivity} label="Pending Review" value={stats?.pending_review ?? '—'} color="var(--amber)" />
              <StatCard icon={FiThumbsUp} label="Helpful Feedback" value={stats?.helpful_feedback ?? '—'} color="var(--purple)" />
            </div>

            {/* Sync Engine UI has been removed to prevent user confusion. Syncing will be handled strictly locally via run_sync.py */}
          </>
        )}

        {/* CHUNKS TAB */}
        {tab === 'chunks' && (
          <>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: 16 }}>
              Pending Chunks ({chunks.length})
            </h3>

            {chunks.length === 0 && (
              <div className="glass-card" style={{
                padding: 40, textAlign: 'center',
                color: 'var(--text-muted)',
              }}>
                ✅ No pending chunks. All clear!
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {chunks.map(chunk => (
                <div key={chunk.chunk_id} className="glass-card" style={{ padding: 18 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
                    <div>
                      <span className="source-badge" style={{ marginBottom: 6 }}>
                        <FiFile size={11} /> {chunk.source_file}
                      </span>
                      <span className="tag tag-pending" style={{ marginLeft: 8 }}>
                        {chunk.status}
                      </span>
                    </div>
                    <div style={{ display: 'flex', gap: 6 }}>
                      <button
                        className="btn-ghost"
                        style={{ padding: '6px 14px', fontSize: '0.78rem', color: 'var(--green)', borderColor: 'var(--green)' }}
                        onClick={() => handleChunkAction(chunk.chunk_id, 'approve')}
                      >
                        <FiCheck size={14} /> Approve
                      </button>
                      <button
                        className="btn-ghost"
                        style={{ padding: '6px 14px', fontSize: '0.78rem', color: 'var(--red)', borderColor: 'var(--red)' }}
                        onClick={() => handleChunkAction(chunk.chunk_id, 'reject')}
                      >
                        <FiX size={14} /> Reject
                      </button>
                    </div>
                  </div>
                  <p style={{
                    fontSize: '0.82rem', color: 'var(--text-secondary)',
                    lineHeight: 1.6, whiteSpace: 'pre-wrap',
                  }}>
                    {chunk.text}
                  </p>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Spin animation for sync button */}
      <style>{`
        .spin { animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  )
}


function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="glass-card" style={{
      padding: '20px 18px', display: 'flex', flexDirection: 'column', gap: 8,
    }}>
      <Icon size={20} color={color} />
      <span style={{ fontSize: '1.6rem', fontWeight: 700, color }}>{value}</span>
      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
        {label}
      </span>
    </div>
  )
}
