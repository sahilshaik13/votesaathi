import React, { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import './ChatWindow.css'

/**
 * Renders the full message thread and auto-scrolls on new messages.
 */
export default function ChatWindow({ messages, isLoading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="chat-window" role="log" aria-live="polite" aria-label="Conversation">
      {messages.map(msg => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      {isLoading && (
        <div className="typing-indicator" aria-label="VoteSaathi is typing">
          <span></span><span></span><span></span>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  )
}
