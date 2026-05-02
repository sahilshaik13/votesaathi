import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

/**
 * Send a chat message to the VoteSaathi backend.
 * @param {string} message
 * @param {string} sessionId
 * @returns {Promise<{reply: string, sources: Array, session_id: string}>}
 */
export async function postChat(message, sessionId) {
  const { data } = await api.post('/chat', { message, session_id: sessionId })
  return data
}

/**
 * Fetch election timeline phases.
 * @param {'general'|'state'} type
 * @returns {Promise<{phases: Array}>}
 */
export async function getTimeline(type = 'general') {
  const { data } = await api.get('/timeline', { params: { type } })
  return data
}
