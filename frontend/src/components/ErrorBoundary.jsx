import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary-container">
          <div className="error-card">
            <h2>Oops! Something went wrong.</h2>
            <p>VoteSaathi encountered an unexpected error.</p>
            <button onClick={() => window.location.reload()} className="primary-btn">
              Reload Application
            </button>
          </div>
          <style>{`
            .error-boundary-container {
              display: flex;
              align-items: center;
              justify-content: center;
              height: 100vh;
              background: #f8fafc;
              font-family: system-ui, -apple-system, sans-serif;
            }
            .error-card {
              background: white;
              padding: 2rem;
              border-radius: 1rem;
              box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
              text-align: center;
              max-width: 400px;
            }
            .error-card h2 { color: #1e293b; margin-bottom: 1rem; }
            .error-card p { color: #64748b; margin-bottom: 2rem; }
          `}</style>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
