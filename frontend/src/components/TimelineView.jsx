import React, { useState, useEffect } from 'react'
import { getTimeline } from '../services/api'
import './TimelineView.css'

export default function TimelineView({ type = 'general', onClose }) {
  const [phases, setPhases] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getTimeline(type).then(data => {
      setPhases(data.phases || [])
      setLoading(false)
    })
  }, [type])

  return (
    <div className="timeline-overlay">
      <div className="timeline-modal">
        <div className="timeline-header">
          <h3>{type === 'general' ? 'Lok Sabha' : 'State Assembly'} Election Timeline</h3>
          <button className="close-btn" onClick={onClose} aria-label="Close timeline">×</button>
        </div>
        
        {loading ? (
          <div className="timeline-loading">Loading phases...</div>
        ) : (
          <div className="timeline-content">
            {phases.map((phase, i) => (
              <div key={i} className="timeline-node">
                <div className="node-marker"></div>
                <div className="node-details">
                  <span className="node-duration">{phase.duration}</span>
                  <h4 className="node-title">{phase.name}</h4>
                  <p className="node-desc">{phase.description}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
