import { useState, useCallback } from 'react'
import { postChat } from '../services/api'

/**
 * Manages chat state and communication with the VoteSaathi backend.
 */
export function useChat(sessionId) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || !sessionId) return

    const userMsg = { role: 'user', content: text, id: Date.now() }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)
    setError(null)

    try {
      const data = await postChat(text, sessionId)
      const assistantMsg = {
        role: 'assistant',
        content: data.reply,
        sources: data.sources || [],
        id: Date.now() + 1,
      }
      setMessages(prev => [...prev, assistantMsg])
    } catch (err) {
      setError('Something went wrong. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  const clearMessages = () => setMessages([])

  return { messages, sendMessage, isLoading, error, clearMessages }
}
