import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        // Get codespace name from environment or use localhost for testing
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME || 'localhost'}-8000.app.github.dev/api/activities/`;
        console.log('Fetching Activities from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Activities API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results ? data.results : data;
        setActivities(Array.isArray(activitiesData) ? activitiesData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  return (
    <div className="container">
      <div className="row mb-4">
        <div className="col-md-12">
          <h2>📊 Activities</h2>
        </div>
      </div>

      {loading && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-info d-flex align-items-center" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              Loading activities...
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error loading activities</h4>
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <div className="row">
          <div className="col-md-12">
            {activities.length === 0 ? (
              <div className="empty-state">
                <h3>No Activities Found</h3>
                <p>Start logging your activities to see them here.</p>
              </div>
            ) : (
              <div className="table-container">
                <table className="table table-hover table-striped mb-0">
                  <thead>
                    <tr>
                      <th scope="col">ID</th>
                      <th scope="col">User</th>
                      <th scope="col">Activity Type</th>
                      <th scope="col">Duration</th>
                      <th scope="col">Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {activities.map((activity) => (
                      <tr key={activity.id}>
                        <td className="fw-bold">{activity.id}</td>
                        <td>{activity.user}</td>
                        <td>
                          <span className="badge bg-primary">{activity.activity_type}</span>
                        </td>
                        <td>{activity.duration}</td>
                        <td>{new Date(activity.date).toLocaleDateString()}</td>
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

export default Activities;
