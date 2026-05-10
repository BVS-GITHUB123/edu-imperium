
import React, { useEffect, useState } from 'react';
import axios from 'axios';

// ─── Backend URL ──────────────────────────────────────────────────────────────
// During development this falls back to localhost.
// In production (Render Static Site) set the environment variable:
//   REACT_APP_API_URL=https://<your-backend-service>.onrender.com
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [msg, setMsg] = useState('');

  useEffect(() => {
    axios
      .get(`${API_URL}/api/health/`)
      .then((r) => setMsg(r.data.status))
      .catch(() => setMsg('Backend not connected'));
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>EDUIMPERIUM LIVE</h1>
      <h2>{msg}</h2>
    </div>
  );
}

export default App;
