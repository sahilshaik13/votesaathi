import { useState, useEffect } from 'react'

/**
 * Manages a persistent session ID using localStorage.
 */
export function useSession() {
  const [sessionId, setSessionId] = useState(null)

  useEffect(() => {
    let id = localStorage.getItem('vs_session_id')
    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('vs_session_id', id)
    }
    setSessionId(id)
  }, [])

  const resetSession = () => {
    const id = crypto.randomUUID()
    localStorage.setItem('vs_session_id', id)
    setSessionId(id)
  }

  return { sessionId, resetSession }
}
