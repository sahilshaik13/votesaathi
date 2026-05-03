import React from 'react'
import './SuggestionChips.css'
import { useLanguage } from '../context/LanguageContext'

const SUGGESTIONS = [
  { icon: '📝', text: 'How do I register to vote?' },
  { icon: '🛡️', text: 'What is the Model Code of Conduct?' },
  { icon: '📄', text: 'What documents do I need at the booth?' },
  { icon: '📍', text: 'How do I find my polling booth?' },
  { icon: '📅', text: 'When is the next election phase?' },
  { icon: '🌍', text: 'Can NRIs vote in Indian elections?' },
  { icon: '🗳️', text: 'How does the EVM machine work?' },
  { icon: '✅', text: 'Am I eligible to vote? I am 17.' },
]

export default function SuggestionChips({ onSelect }) {
  const { t } = useLanguage()
  return (
    <div className="suggestion-container">
      <div className="welcome-banner">
        <img 
          src="/logo.png" 
          alt="VoteSaathi Logo" 
          className="welcome-logo" 
        />
        <h2>{t('welcome_title')}</h2>
        <p>{t('welcome_subtitle')}</p>
      </div>

      <div className="chips-grid" role="list">
        {SUGGESTIONS.map((item, i) => (
          <button 
            key={i} 
            className="chip-btn"
            onClick={() => onSelect(item.text)}
          >
            <span className="chip-icon">{item.icon}</span>
            <span className="chip-text">{item.text}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
