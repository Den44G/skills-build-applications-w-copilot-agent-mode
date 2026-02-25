import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        // Get codespace name from environment or use localhost for testing
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME || 'localhost'}-8000.app.github.dev/api/leaderboards/`;
        console.log('Fetching Leaderboard from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results ? data.results : data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  const getRankBadgeColor = (rank) => {
    if (rank === 1) return 'bg-warning';
    if (rank === 2) return 'bg-secondary';
    if (rank === 3) return 'bg-danger';
    return 'bg-info';
  };

  return (
    <div className="container">
      <div className="row mb-4">
        <div className="col-md-12">
          <h2>🏅 Leaderboard</h2>
          <p className="text-muted">Top performers on OctoFit Tracker</p>
        </div>
      </div>

      {loading && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-info d-flex align-items-center" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              Loading leaderboard...
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error loading leaderboard</h4>
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <div className="row">
          <div className="col-md-12">
            {leaderboard.length === 0 ? (
              <div className="empty-state">
                <h3>No Leaderboard Data</h3>
                <p>Leaderboard will update as users complete activities.</p>
              </div>
            ) : (
              <div className="table-container">
                <table className="table table-hover mb-0">
                  <thead>
                    <tr>
                      <th scope="col" style={{ width: '80px' }}>Rank</th>
                      <th scope="col">User</th>
                      <th scope="col" style={{ width: '120px' }}>Score</th>
                      <th scope="col" style={{ width: '150px' }}>Activities</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.map((entry, index) => (
                      <tr key={entry.id || index}>
                        <td>
                          <span className={`badge ${getRankBadgeColor(index + 1)} fs-5`}>
                            #{index + 1}
                          </span>
                        </td>
                        <td>
                          <div className="d-flex align-items-center">
                            <div 
                              className="rounded-circle me-2" 
                              style={{
                                width: '35px',
                                height: '35px',
                                backgroundColor: `hsl(${(index * 50) % 360}, 70%, 60%)`,
                                color: 'white',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontWeight: 'bold'
                              }}
                            >
                              {(entry.user_name || entry.user || 'U')[0].toUpperCase()}
                            </div>
                            {entry.user_name || entry.user || 'Unknown'}
                          </div>
                        </td>
                        <td>
                          <span className="h5 mb-0" style={{ color: '#007bff' }}>
                            {entry.score || entry.points || 0}
                          </span>
                        </td>
                        <td>
                          <span className="badge bg-success">
                            {entry.activities_count || entry.activity_count || 0} activities
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
