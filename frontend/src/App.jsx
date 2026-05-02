import React, { useState } from 'react'
import { useSession } from './hooks/useSession'
import { useChat } from './hooks/useChat'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import SuggestionChips from './components/SuggestionChips'
import TimelineView from './components/TimelineView'
import './App.css'

export default function App() {
  const { sessionId, resetSession } = useSession()
  const { messages, sendMessage, isLoading, clearMessages } = useChat(sessionId)
  
  const [timelineType, setTimelineType] = useState(null) // null, 'general', 'state'

  const handleNewChat = () => {
    resetSession()
    clearMessages()
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand">
          <span className="logo">🗳️</span>
          <h1>VoteSaathi</h1>
        </div>
        <div className="header-actions">
          <button onClick={() => setTimelineType('general')} className="action-btn">
            Lok Sabha Timeline
          </button>
          <button onClick={() => setTimelineType('state')} className="action-btn">
            State Timeline
          </button>
          <button onClick={handleNewChat} className="action-btn primary">
            New Chat
          </button>
        </div>
      </header>

      <main className="app-main">
        {messages.length === 0 ? (
          <SuggestionChips onSelect={sendMessage} />
        ) : (
          <ChatWindow messages={messages} isLoading={isLoading} />
        )}
      </main>

      <footer className="app-footer">
        <InputBar onSend={sendMessage} disabled={isLoading} />
      </footer>

      {timelineType && (
        <TimelineView 
          type={timelineType} 
          onClose={() => setTimelineType(null)} 
        />
      )}
    </div>
  )
}
