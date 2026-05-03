import React, { useEffect, useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import { subscribeToElectionData } from '../firebase'
import './LiveDashboard.css'
import { useLanguage } from '../context/LanguageContext'

export default function LiveDashboard({ onClose }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const { t, lang } = useLanguage()

  const [searchQuery, setSearchQuery] = useState('')
  const [searchResult, setSearchResult] = useState(null)
  const [searching, setSearching] = useState(false)
  const [stateBriefing, setStateBriefing] = useState(null)
  const [fetchingBrief, setFetchingBrief] = useState(false)
  const [activeQuery, setActiveQuery] = useState(null)

  const handleSearch = async (query = searchQuery) => {
    if (!query.trim()) return
    setSearching(true)
    setStateBriefing(null)
    setActiveQuery(query)
    try {
      // 1. Fetch constituency/state basic result
      const resSearch = await axios.get(`/api/dashboard/search?query=${query}`)
      setSearchResult(resSearch.data)
      
      // 2. Fetch specific news and metrics for this query
      const resLive = await axios.get(`/api/dashboard/live?lang=${lang}&query=${query}`)
      setData(resLive.data)
      
      // 3. If it's a state search, fetch deep briefing
      if (resSearch.data.found && resSearch.data.data.state === "India") {
        fetchStateBriefing(resSearch.data.data.name)
      }
    } catch (err) {
      console.error('Search failed', err)
    } finally {
      setSearching(false)
    }
  }

  const fetchStateBriefing = async (stateName) => {
    setFetchingBrief(true)
    try {
      const { data } = await axios.get(`/api/dashboard/state-briefing?state=${stateName}`)
      setStateBriefing(data)
    } catch (err) {
      console.error('Failed to fetch state briefing', err)
    } finally {
      setFetchingBrief(false)
    }
  }

  const handleStateSelect = (stateName) => {
    setSearchQuery(stateName)
    handleSearch(stateName)
  }

  useEffect(() => {
    // 1. Initial Fetch
    const fetchData = async () => {
      try {
        const resLive = await axios.get(`/api/dashboard/live?lang=${lang}`)
        setData(resLive.data)
      } catch (err) {
        console.error('Failed to fetch dashboard data', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()

    // 2. Realtime Subscriptions
    const newsPath = activeQuery ? `live/news/${activeQuery}` : "live/news/general"
    const statsPath = activeQuery ? `live/stats/${activeQuery}` : "live/stats/general"

    const unsubscribeNews = subscribeToElectionData(newsPath, (news) => {
      if (news) setData(prev => ({ ...prev, news }))
    })

    const unsubscribeStats = subscribeToElectionData(statsPath, (stats) => {
      if (stats) setData(prev => ({ ...prev, stats }))
    })

    return () => {
      unsubscribeNews()
      unsubscribeStats()
    }
  }, [lang, activeQuery])

  if (loading) return (
    <div className="dashboard-overlay">
      <div className="liquid-glass-loader">
        <div className="liquid"></div>
      </div>
    </div>
  )

  return (
    <div className="main-dashboard-view">
      <div className="glass-dashboard-main">
        <header className="dashboard-header">
          <h2>{t('live_dashboard')}</h2>
        </header>

        <div className="dashboard-content">
          <section className="dashboard-section">
            <div className="section-header-flex">
              <h3 className="section-title">📊 {t('key_metrics')}</h3>
              <div className="constituency-finder">
                <input 
                  type="text" 
                  placeholder="Enter Constituency or PIN code..." 
                  className="const-search" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button 
                  className="location-btn" 
                  onClick={() => {
                    if (navigator.geolocation) {
                      navigator.geolocation.getCurrentPosition(async (pos) => {
                        const { latitude, longitude } = pos.coords;
                        setSearching(true);
                        try {
                          const { data } = await axios.get(`/api/dashboard/search?lat=${latitude}&lng=${longitude}`);
                          setSearchResult(data);
                        } catch (err) {
                          console.error('Location search failed', err);
                        } finally {
                          setSearching(false);
                        }
                      });
                    } else {
                      alert("Geolocation is not supported by this browser.");
                    }
                  }}
                  title="Detect my location"
                >
                  📍
                </button>
                <button className="search-btn" onClick={handleSearch} disabled={searching}>
                  {searching ? '⏳' : '🔍'}
                </button>
              </div>
            </div>

            {searchResult && (
              <div className="search-result-panel animate-in">
                {searchResult.found ? (
                  <div className="result-card">
                    <button className="close-result" onClick={() => {setSearchResult(null); setStateBriefing(null);}}>✕</button>
                    <h4>📍 {searchResult.data.name}, {searchResult.data.state}</h4>
                    <div className="result-stats">
                      <span><strong>Phase:</strong> {searchResult.data.phase}</span>
                      <span><strong>Candidates:</strong> {searchResult.data.candidates}</span>
                      <span><strong>Prev. Turnout:</strong> {searchResult.data.last_turnout}</span>
                    </div>
                  </div>
                ) : (
                  <div className="result-card error">
                    <button className="close-result" onClick={() => setSearchResult(null)}>✕</button>
                    <p>{searchResult.message}</p>
                  </div>
                )}
              </div>
            )}

            {fetchingBrief && (
              <div className="briefing-loader">
                <div className="shimmer"></div>
                <p>Generating neutral election briefing for {searchResult?.data?.name}...</p>
              </div>
            )}

            {stateBriefing && (
              <div className="state-briefing-panel animate-in skeu-panel">
                <header className="briefing-header">
                  <h3>🗳️ {stateBriefing.state} Election Briefing</h3>
                  <span className="neutral-badge">Neutral Information AI</span>
                </header>
                <div className="markdown-content">
                  <ReactMarkdown>{stateBriefing.briefing}</ReactMarkdown>
                </div>
                {stateBriefing.sources && stateBriefing.sources.length > 0 && (
                  <footer className="briefing-sources">
                    <strong>Sources:</strong>
                    <ul>
                      {stateBriefing.sources.map((src, idx) => (
                        <li key={idx}><a href={src.source_uri} target="_blank" rel="noreferrer">{src.source_uri}</a></li>
                      ))}
                    </ul>
                  </footer>
                )}
              </div>
            )}

            <div className="stats-grid">
              <div className="skeu-card">
                <h4>{t('phase')}</h4>
                <p>{data?.stats?.phase}</p>
              </div>
              <div className="skeu-card">
                <h4>{t('turnout')}</h4>
                <p>{data?.stats?.voter_turnout}</p>
              </div>
              <div className="skeu-card">
                <h4>{t('registered')}</h4>
                <p>{data?.stats?.registered_voters}</p>
              </div>
              <div className="skeu-card">
                <h4>{t('seats')}</h4>
                <p>{data?.stats?.total_seats}</p>
              </div>
            </div>
          </section>

          <section className="dashboard-grid-layout">
            <div className="news-panel">
              <h3 className="section-title">🗞️ {t('latest_updates')}</h3>
              <div className="news-scroll">
                {data?.news.map((item, i) => (
                  <a key={i} href={item.link} target="_blank" rel="noopener noreferrer" className="news-item">
                    <span className="news-title">{item.title}</span>
                    <div className="news-meta">
                      <span className="source-badge">{item.source}</span>
                      <span>{new Date(item.pub_date).toLocaleDateString()}</span>
                    </div>
                  </a>
                ))}
              </div>
            </div>

            <div className="insight-panel skeu-panel">
              <img 
                src="/illustration.png" 
                alt="Election Analytics" 
                className="insight-img"
              />
              <div className="insight-content">
                <h4>{t('verified_intelligence')}</h4>
                <p>{t('verified_p')}</p>
                <button className="secondary-btn" style={{width: '100%', marginTop: 'auto'}}>{t('view_sources')}</button>
              </div>
            </div>
          </section>
        </div>

        <footer className="dashboard-footer">
          <div className="live-indicator">
            <span className="dot"></span> {t('live_updates')}
          </div>
        </footer>
      </div>
    </div>
  )
}
