import React, { useState } from 'react'
import './InputBar.css'
import { useLanguage } from '../context/LanguageContext'

export default function InputBar({ onSend, disabled }) {
  const [text, setText] = useState('')
  const { t, lang } = useLanguage()
  const [isListening, setIsListening] = useState(false)

  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser.")
      return
    }

    const recognition = new SpeechRecognition()
    recognition.lang = lang === 'en' ? 'en-IN' : 
                       lang === 'hi' ? 'hi-IN' : 
                       lang === 'bn' ? 'bn-IN' : 
                       lang === 'ta' ? 'ta-IN' : 
                       lang === 'te' ? 'te-IN' : 
                       lang === 'mr' ? 'mr-IN' : 'en-IN'
    
    recognition.onstart = () => setIsListening(true)
    recognition.onend = () => setIsListening(false)
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      setText(transcript)
    }

    recognition.start()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!text.trim() || disabled) return
    onSend(text)
    setText('')
  }

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <button 
        type="button" 
        className={`voice-btn ${isListening ? 'listening' : ''}`} 
        onClick={handleVoiceInput}
        aria-label="Voice input"
      >
        {isListening ? '🛑' : '🎙️'}
      </button>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={t('ask_placeholder')}
        disabled={disabled}
        aria-label="Chat input"
        autoFocus
      />
      <button 
        type="submit" 
        className="send-btn"
        disabled={!text.trim() || disabled}
        aria-label="Send message"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </form>
  )
}
