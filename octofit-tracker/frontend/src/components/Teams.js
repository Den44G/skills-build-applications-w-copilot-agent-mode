import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        // Get codespace name from environment or use localhost for testing
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME || 'localhost'}-8000.app.github.dev/api/teams/`;
        console.log('Fetching Teams from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Teams API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results ? data.results : data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  return (
    <div className="container">
      <div className="row mb-4">
        <div className="col-md-12">
          <h2>🏆 Teams</h2>
        </div>
      </div>

      {loading && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-info d-flex align-items-center" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              Loading teams...
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error loading teams</h4>
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <div className="row">
          {teams.length === 0 ? (
            <div className="col-md-12">
              <div className="empty-state">
                <h3>No Teams Found</h3>
                <p>Create a team to get started with team competitions.</p>
                <button className="btn btn-primary btn-lg">Create Team</button>
              </div>
            </div>
          ) : (
            <>
              {teams.map((team) => (
                <div key={team.id} className="col-md-6 col-lg-4 mb-4">
                  <div className="card h-100">
                    <div className="card-header">
                      <h5 className="card-title mb-0">{team.name}</h5>
                    </div>
                    <div className="card-body">
                      <p className="card-text">{team.description}</p>
                      <p className="small text-muted mb-0">
                        Created: {new Date(team.created_at || team.date_created).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="card-footer bg-light">
                      <button className="btn btn-sm btn-info">View Team</button>
                      <button className="btn btn-sm btn-warning ms-2">Members</button>
                    </div>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default Teams;
