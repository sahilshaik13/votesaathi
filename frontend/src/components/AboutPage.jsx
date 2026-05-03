import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import './AboutPage.css';

export default function AboutPage({ onGoToDashboard }) {
  const { t } = useLanguage();

  return (
    <div className="about-page">
      <div className="about-container">
        <header className="about-header animate-fade-in">
          <div className="brand-badge">ELECTION INTELLIGENCE 2024</div>
          <h1>{t('about_title')}</h1>
          <p className="subtitle">{t('about_subtitle')}</p>
        </header>

        <section className="about-section glass-card animate-slide-up">
          <div className="section-content">
            <div className="icon-wrapper">⚠️</div>
            <div>
              <h2>{t('problem_title')}</h2>
              <p>{t('problem_p')}</p>
            </div>
          </div>
        </section>

        <section className="about-grid">
          <div className="about-section glass-card animate-slide-up delay-1">
            <div className="icon-wrapper">✨</div>
            <h2>{t('solution_title')}</h2>
            <p>{t('solution_p')}</p>
          </div>

          <div className="about-section glass-card animate-slide-up delay-2">
            <div className="icon-wrapper">🛠️</div>
            <h2>{t('how_title')}</h2>
            <ul className="tech-list">
              <li>{t('how_rag')}</li>
              <li>{t('how_lang')}</li>
              <li>{t('how_live')}</li>
              <li>{t('how_secure')}</li>
            </ul>
          </div>
        </section>

        <footer className="about-footer animate-fade-in delay-3">
          <button className="cta-button" onClick={onGoToDashboard}>
            {t('explore_dashboard')} <span className="arrow">→</span>
          </button>
        </footer>
      </div>
    </div>
  );
}
