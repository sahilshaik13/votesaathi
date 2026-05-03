import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import SourcePanel from './SourcePanel'
import './MessageBubble.css'

/**
 * Renders a single chat message, including optional RAG source citations.
 * Assistant messages are rendered as markdown for rich formatting.
 */
export default function MessageBubble({ message }) {
  const [showSources, setShowSources] = useState(false)
  const isUser = message.role === 'user'

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      {!isUser && (
        <div className="avatar" aria-hidden="true">🗳️</div>
      )}
      <div className="bubble-content">
        <div className="bubble-text">
          {isUser ? (
            message.content
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>
        {!isUser && message.sources?.length > 0 && (
          <button
            className="sources-toggle"
            onClick={() => setShowSources(!showSources)}
            aria-expanded={showSources}
            aria-label={`${showSources ? 'Hide' : 'Show'} ${message.sources.length} source${message.sources.length > 1 ? 's' : ''}`}
          >
            📄 {message.sources.length} source{message.sources.length > 1 ? 's' : ''}
            <span className="toggle-arrow">{showSources ? '▲' : '▼'}</span>
          </button>
        )}
        {showSources && <SourcePanel sources={message.sources} />}
      </div>
    </div>
  )
}
