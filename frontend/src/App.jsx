import React, { useState } from 'react'
import { useSession } from './hooks/useSession'
import { useChat } from './hooks/useChat'
import { useLanguage } from './context/LanguageContext'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import SuggestionChips from './components/SuggestionChips'
import TimelineView from './components/TimelineView'
import SessionSidebar from './components/SessionSidebar'
import LiveDashboard from './components/LiveDashboard'
import AboutPage from './components/AboutPage'
import './App.css'

export default function App() {
  const { sessionId, userId, token, resetSession, switchSession } = useSession()
  const { messages, setMessages, sendMessage, isLoading, error, clearMessages } = useChat(sessionId, userId)
  const { lang, setLang, t } = useLanguage()
  
  const [currentView, setCurrentView] = useState('about') // 'about', 'dashboard', 'chat'
  const [timelineType, setTimelineType] = useState(null)
  const [showHistory, setShowHistory] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [highContrast, setHighContrast] = useState(false)

  const toggleHighContrast = () => {
    setHighContrast(!highContrast)
    document.body.classList.toggle('high-contrast')
  }

  const handleNewChat = () => {
    resetSession()
    clearMessages()
    setShowHistory(false)
    setCurrentView('chat')
  }

  const handleSelectSession = (id, history) => {
    switchSession(id)
    // History from backend lacks IDs, which breaks React keys
    const historyWithIds = (history || []).map((msg, index) => ({
      ...msg,
      id: msg.id || `${Date.now()}-${index}`
    }))
    setMessages(historyWithIds)
    setShowHistory(false)
    setCurrentView('chat')
  }

  // Map short codes to full names for the AI instructions
  const langMap = {
    'en': 'English',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi'
  }
  const currentLangName = langMap[lang] || 'English'

  const handleSendMessage = (text) => {
    sendMessage(text, currentLangName)
  }

  return (
    <div className={`app-container ${isMobileMenuOpen ? 'menu-open' : ''}`}>
      <header className="app-header">
        <div className="header-brand">
          <img 
            src="/logo.png" 
            alt="VoteSaathi Logo" 
            className="brand-logo" 
          />
          <div className="brand-text">
            <h1>VoteSaathi</h1>
            <span className="brand-tagline">AI Election Intelligence</span>
          </div>
        </div>
        
        <div className="header-right">
          <select 
            className="lang-select" 
            value={lang} 
            onChange={(e) => setLang(e.target.value)}
          >
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="bn">বাংলা</option>
            <option value="ta">தமிழ்</option>
            <option value="te">తెలుగు</option>
            <option value="mr">मराठी</option>
          </select>

          <button 
            className="accessibility-btn" 
            onClick={toggleHighContrast}
            title="Toggle High Contrast"
            aria-label="Toggle High Contrast"
          >
            {highContrast ? '☀️' : '👁️'}
          </button>

          <button 
            className="mobile-menu-toggle"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>

        <nav className={`header-actions ${isMobileMenuOpen ? 'open' : ''}`}>
          <button 
            className={`nav-btn ${currentView === 'about' ? 'active' : ''}`}
            onClick={() => { setCurrentView('about'); setIsMobileMenuOpen(false); }}
          >
            🏠 {t('about') || 'Home'}
          </button>
          <button 
            className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => { setCurrentView('dashboard'); setIsMobileMenuOpen(false); }}
          >
            📊 {t('dashboard')}
          </button>
          <button 
            className={`nav-btn ${currentView === 'chat' ? 'active' : ''}`}
            onClick={() => { setCurrentView('chat'); setIsMobileMenuOpen(false); }}
          >
            💬 {t('assistant')}
          </button>
          <button 
            className="nav-btn"
            onClick={() => { setShowHistory(!showHistory); setIsMobileMenuOpen(false); }}
          >
            📜 {t('history')}
          </button>
          <button 
            className="nav-btn primary-btn"
            onClick={() => { handleNewChat(); setIsMobileMenuOpen(false); }}
          >
            ✨ {t('new_chat')}
          </button>
        </nav>
      </header>

      <main className="app-main">
        {currentView === 'about' ? (
          <AboutPage onGoToDashboard={() => setCurrentView('dashboard')} />
        ) : currentView === 'dashboard' ? (
          <LiveDashboard />
        ) : (
          <div className="chat-view-container">
            {messages.length === 0 ? (
              <SuggestionChips onSelect={handleSendMessage} />
            ) : (
              <ChatWindow messages={messages} isLoading={isLoading} />
            )}
          </div>
        )}
      </main>

      {currentView === 'chat' && (
        <footer className="app-footer">
          <InputBar onSend={handleSendMessage} disabled={isLoading} />
        </footer>
      )}

      {timelineType && (
        <TimelineView 
          type={timelineType} 
          onClose={() => setTimelineType(null)} 
        />
      )}

      {showHistory && (
        <SessionSidebar 
          userId={userId} 
          currentSessionId={sessionId} 
          onSelect={handleSelectSession} 
          onClose={() => setShowHistory(false)} 
        />
      )}
    </div>
  )
}
