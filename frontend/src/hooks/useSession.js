import { useState, useEffect } from 'react'
import axios from 'axios'

/**
 * Manages a persistent session ID and a long-lived user ID using localStorage.
 */
export function useSession() {
  const [sessionId, setSessionId] = useState(null)
  const [userId, setUserId] = useState(null)
  const [token, setToken] = useState(null)

  useEffect(() => {
    // 1. Manage User ID
    let uId = localStorage.getItem('vs_user_id')
    if (!uId) {
      uId = crypto.randomUUID()
      localStorage.setItem('vs_user_id', uId)
    }
    setUserId(uId)

    // 2. Manage Session ID
    let sId = localStorage.getItem('vs_session_id')
    if (!sId) {
      sId = crypto.randomUUID()
      localStorage.setItem('vs_session_id', sId)
    }
    setSessionId(sId)

    // 3. Fetch/Manage Token for JWT
    const fetchToken = async (id) => {
      try {
        const storedToken = localStorage.getItem('vs_token')
        if (storedToken) {
          setToken(storedToken)
        } else {
          const { data } = await axios.get(`/api/user/token/${id}`)
          localStorage.setItem('vs_token', data.token)
          setToken(data.token)
        }
      } catch (err) {
        console.error('Failed to fetch auth token', err)
      }
    }
    fetchToken(uId)
  }, [])

  const resetSession = () => {
    const id = crypto.randomUUID()
    localStorage.setItem('vs_session_id', id)
    setSessionId(id)
  }

  const switchSession = (id) => {
    localStorage.setItem('vs_session_id', id)
    setSessionId(id)
  }

  return { sessionId, userId, token, resetSession, switchSession }
}
