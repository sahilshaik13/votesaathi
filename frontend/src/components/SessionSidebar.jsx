import React, { useEffect, useState } from 'react'
import { getUserSessions, getSession } from '../services/api'
import './SessionSidebar.css'

export default function SessionSidebar({ userId, currentSessionId, onSelect, onClose }) {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) return
    const fetchSessions = async () => {
      try {
        const data = await getUserSessions(userId)
        if (data && Array.isArray(data)) {
          // Sort by last updated (newest first)
          setSessions(data.sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated)))
        } else {
          setSessions([])
        }
      } catch (err) {
        console.error('Failed to fetch sessions', err)
      } finally {
        setLoading(false)
      }
    }
    fetchSessions()
  }, [userId])

  const handleSelect = async (sessionId) => {
    try {
      const history = await getSession(sessionId)
      onSelect(sessionId, history)
    } catch (err) {
      console.error('Failed to fetch session history', err)
    }
  }

  return (
    <div className="session-sidebar">
      <div className="sidebar-header">
        <h3>Previous Chats</h3>
        <button onClick={onClose} className="close-btn">×</button>
      </div>
      <div className="session-list">
        {loading ? (
          <div className="sidebar-loader">Loading...</div>
        ) : sessions.length === 0 ? (
          <div className="no-sessions">No previous chats found.</div>
        ) : (
          sessions.map(s => (
            <button
              key={s.session_id}
              className={`session-item ${s.session_id === currentSessionId ? 'active' : ''}`}
              onClick={() => handleSelect(s.session_id)}
            >
              <span className="session-icon">💬</span>
              <div className="session-info">
                <div className="session-id">Session {s.session_id.slice(0, 8)}</div>
                <div className="session-date">{new Date(s.last_updated).toLocaleDateString()}</div>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}
