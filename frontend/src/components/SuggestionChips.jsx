import React from 'react'
import './SuggestionChips.css'
import { useLanguage } from '../context/LanguageContext'

const SUGGESTIONS = [
  { icon: '📝', key: 'q_register', text: 'How do I register to vote?' },
  { icon: '🛡️', key: 'q_mcc', text: 'What is the Model Code of Conduct?' },
  { icon: '📄', key: 'q_documents', text: 'What documents do I need at the booth?' },
  { icon: '📍', key: 'q_booth', text: 'How do I find my polling booth?' },
  { icon: '📅', key: 'q_phase', text: 'When is the next election phase?' },
  { icon: '🌍', key: 'q_nri', text: 'Can NRIs vote in Indian elections?' },
  { icon: '🗳️', key: 'q_evm', text: 'How does the EVM machine work?' },
  { icon: '✅', key: 'q_eligibility', text: 'Am I eligible to vote? I am 17.' },
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
            <span className="chip-text">{t(item.key)}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
