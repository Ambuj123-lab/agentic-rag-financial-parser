import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FiCpu } from 'react-icons/fi'

export default function AuthCallback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { login } = useAuth()

  useEffect(() => {
    const token = searchParams.get('token')
    if (token) {
      try {
        const payloadStr = atob(token.split('.')[1])
        const user = JSON.parse(payloadStr)
        
        login(token, {
          email: user.sub || user.email,
          name: user.name || 'User',
          picture: user.picture || null,
          is_admin: user.is_admin || false
        })
        navigate('/chat', { replace: true })
      } catch (err) {
        console.error('Invalid token payload', err)
        navigate('/?error=invalid_token', { replace: true })
      }
    } else {
      navigate('/', { replace: true })
    }
  }, [searchParams, navigate, login])

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', color: 'var(--accent)' }}>
      <FiCpu size={50} style={{ animation: 'pulse 1.5s infinite ease-in-out' }} />
      <p style={{ marginTop: 20, fontWeight: 600 }}>Authenticating...</p>
    </div>
  )
}
