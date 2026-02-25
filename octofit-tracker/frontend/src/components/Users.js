import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // Get codespace name from environment or use localhost for testing
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME || 'localhost'}-8000.app.github.dev/api/users/`;
        console.log('Fetching Users from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Users API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results ? data.results : data;
        setUsers(Array.isArray(usersData) ? usersData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="container">
      <div className="row mb-4">
        <div className="col-md-12">
          <h2>👥 Users & Profiles</h2>
        </div>
      </div>

      {loading && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-info d-flex align-items-center" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              Loading users...
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error loading users</h4>
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <div className="row">
          <div className="col-md-12">
            {users.length === 0 ? (
              <div className="empty-state">
                <h3>No Users Found</h3>
                <p>Users will appear here once they join the platform.</p>
              </div>
            ) : (
              <div className="table-container">
                <table className="table table-hover table-striped mb-0">
                  <thead>
                    <tr>
                      <th scope="col">ID</th>
                      <th scope="col">Username</th>
                      <th scope="col">Email</th>
                      <th scope="col">First Name</th>
                      <th scope="col">Last Name</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td className="fw-bold">{user.id}</td>
                        <td>
                          <span className="badge bg-success">{user.username || user.user}</span>
                        </td>
                        <td>{user.email}</td>
                        <td>{user.first_name || '-'}</td>
                        <td>{user.last_name || '-'}</td>
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

export default Users;
