import React, { useState } from 'react'
import './App.css'

function App() {
  const [equity, setEquity] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const equityValue = parseFloat(equity);
    if (isNaN(equityValue) || equityValue <= 0 || equityValue > 1) {
      setError('Please enter a valid equity value between 0 and 1');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('/api/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ set_equity: equityValue }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to calculate splits');
      }

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>Equity Split Calculator</h1>
          <p className="subtitle">Calculate optimal vesting period and cliff based on equity ownership</p>
        </header>

        <form onSubmit={handleSubmit} className="form">
          <div className="input-group">
            <label htmlFor="equity">Set Equity Value</label>
            <input
              id="equity"
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={equity}
              onChange={(e) => setEquity(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter equity value (e.g., 0.3)"
              className="input"
              disabled={loading}
            />
            <small>Enter a value between 0 and 1 (e.g., 0.3 for 30%)</small>
          </div>

          <button 
            type="submit" 
            className="button"
            disabled={loading || !equity}
          >
            {loading ? 'Calculating...' : 'Calculate Splits'}
          </button>
        </form>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && (
          <div className="results">
            <h2>Results</h2>
            <div className="results-grid">
              <div className="result-card">
                <div className="result-label">Vesting Period</div>
                <div className="result-value">{results.vesting_years} years</div>
                <div className="result-detail">({results.vesting_days} days)</div>
              </div>
              <div className="result-card">
                <div className="result-label">Cliff Period</div>
                <div className="result-value">{results.cliff_years} years</div>
                <div className="result-detail">({results.cliff_days} days)</div>
              </div>
            </div>
            <div className="details">
              <p><strong>Equity:</strong> {(results.set_equity * 100).toFixed(1)}%</p>
              <p><strong>Average Score:</strong> {results.avg_score.toFixed(4)}</p>
              <p><strong>Average Ratio:</strong> {results.avg_ratio.toFixed(4)}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App
