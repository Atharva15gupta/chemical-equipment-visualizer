import React, { useState } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');

  const handleLoginSuccess = (user) => {
    setIsAuthenticated(true);
    setUsername(user);
  };

  return (
    <div className="App">
      {isAuthenticated ? (
        <Dashboard username={username} />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;
