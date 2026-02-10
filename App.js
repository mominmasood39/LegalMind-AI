import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/login';
import Signup from './components/Signup';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      // Fetch user info
      fetchUserInfo();
    }
  }, [token]);

  const fetchUserInfo = async () => {
    try {
      const response = await fetch('http://localhost:8000/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      } else {
        handleLogout();
      }
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  };

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/login" 
            element={token ? <Navigate to="/chat" /> : <Login onLogin={handleLogin} />} 
          />
          <Route 
            path="/signup" 
            element={token ? <Navigate to="/chat" /> : <Signup onSignup={() => window.location.href = '/login'} />} 
          />
          <Route 
            path="/chat" 
            element={token ? <ChatInterface token={token} user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/" 
            element={<Navigate to={token ? "/chat" : "/login"} />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;