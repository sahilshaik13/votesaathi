import React from 'react'
import './SourcePanel.css'

/**
 * Slide-in panel or inline block showing RAG document citations.
 */
export default function SourcePanel({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="source-panel">
      <h4 className="source-title">Extracted from ECI Documents</h4>
      <ul className="source-list">
        {sources.map((src, i) => (
          <li key={i} className="source-item">
            <p className="source-text">"{src.text.trim()}..."</p>
            {src.source_uri && (
              <a href={src.source_uri} target="_blank" rel="noopener noreferrer" className="source-link">
                View Original Document
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
