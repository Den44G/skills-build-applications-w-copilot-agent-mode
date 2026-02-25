import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        // Get codespace name from environment or use localhost for testing
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME || 'localhost'}-8000.app.github.dev/api/workouts/`;
        console.log('Fetching Workouts from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results ? data.results : data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  const getDifficultyBadge = (difficulty) => {
    const level = difficulty?.toLowerCase() || 'unknown';
    if (level.includes('easy')) return 'bg-success';
    if (level.includes('medium') || level.includes('intermediate')) return 'bg-warning';
    if (level.includes('hard') || level.includes('advanced')) return 'bg-danger';
    return 'bg-secondary';
  };

  return (
    <div className="container">
      <div className="row mb-4">
        <div className="col-md-12">
          <h2>💪 Workouts</h2>
          <p className="text-muted">Browse and start a workout</p>
        </div>
      </div>

      {loading && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-info d-flex align-items-center" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              Loading workouts...
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error loading workouts</h4>
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <div className="row">
          {workouts.length === 0 ? (
            <div className="col-md-12">
              <div className="empty-state">
                <h3>No Workouts Available</h3>
                <p>Check back soon for new workout options.</p>
              </div>
            </div>
          ) : (
            <>
              {workouts.map((workout) => (
                <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
                  <div className="card h-100">
                    <div className="card-header">
                      <h5 className="card-title mb-0">{workout.name}</h5>
                    </div>
                    <div className="card-body">
                      <p className="card-text">{workout.description}</p>
                      <div className="mb-3">
                        <p className="mb-2">
                          <strong>Type:</strong>{' '}
                          <span className="badge bg-info">{workout.type || workout.workout_type}</span>
                        </p>
                        <p className="mb-2">
                          <strong>Duration:</strong>{' '}
                          <span className="text-success">{workout.duration} minutes</span>
                        </p>
                        <p className="mb-0">
                          <strong>Difficulty:</strong>{' '}
                          <span className={`badge ${getDifficultyBadge(workout.difficulty)}`}>
                            {workout.difficulty || 'Not specified'}
                          </span>
                        </p>
                      </div>
                    </div>
                    <div className="card-footer bg-light">
                      <button className="btn btn-sm btn-primary">View Details</button>
                      <button className="btn btn-sm btn-success ms-2">Start Workout</button>
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

export default Workouts;
