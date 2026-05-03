import axios from 'axios'

let API_URL = import.meta.env.VITE_API_URL || '';

// Ensure production URL doesn't have a trailing slash before appending /api
if (API_URL.endsWith('/')) {
  API_URL = API_URL.slice(0, -1);
}

export const api = axios.create({
  baseURL: API_URL ? `${API_URL}/api` : '/api',
  headers: { 'Content-Type': 'application/json' },
})

let SCRAPER_URL = import.meta.env.VITE_SCRAPER_URL || API_URL;
if (SCRAPER_URL.endsWith('/')) {
  SCRAPER_URL = SCRAPER_URL.slice(0, -1);
}

export const scraperApi = axios.create({
  baseURL: SCRAPER_URL ? `${SCRAPER_URL}/api` : '/api',
  headers: { 'Content-Type': 'application/json' },
})

// Add JWT to every request if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('vs_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/**
 * Send a chat message to the VoteSaathi backend.
 * @param {string} message
 * @param {string} sessionId
 * @param {string} userId
 * @returns {Promise<{reply: string, sources: Array, session_id: string}>}
 */
export async function postChat(message, sessionId, userId, lang = 'English') {
  const { data } = await api.post('/chat', { 
    message, 
    session_id: sessionId,
    user_id: userId,
    lang: lang
  })
  return data
}

/**
 * Fetch all sessions for a user.
 * @param {string} userId
 */
export async function getUserSessions(userId) {
  const { data } = await api.get(`/user/sessions/${userId}`)
  return data.sessions
}

/**
 * Fetch a single session's history.
 * @param {string} sessionId
 */
export async function getSession(sessionId) {
  const { data } = await api.get(`/session/${sessionId}`)
  return data.history
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
