import React from 'react'
import './SuggestionChips.css'

export default function SuggestionChips({ onSelect }) {
  const suggestions = [
    "How do I register to vote?",
    "What is the Model Code of Conduct?",
    "What documents do I need at the booth?",
    "How do I find my polling booth?",
    "When is the next election phase?",
    "Can NRIs vote?"
  ]

  return (
    <div className="suggestion-container">
      <div className="welcome-banner">
        <h2>Welcome to VoteSaathi 🗳️</h2>
        <p>Your AI companion for the Indian Election Process.</p>
      </div>
      <div className="chips-grid">
        {suggestions.map((text, i) => (
          <button 
            key={i} 
            className="chip-btn" 
            onClick={() => onSelect(text)}
          >
            {text}
          </button>
        ))}
      </div>
    </div>
  )
}
