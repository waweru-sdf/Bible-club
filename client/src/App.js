import { Routes, Route, Link } from 'react-router-dom'
import { useContext } from 'react'
import './App.css'
import Home from './components/Home'
import Users from './components/Users'
import Sessions from './sessions/Sessions'
import Reflections from './reflections/Reflections'
import Login from './components/Login'
import Signup from './components/Signup'
import AuthContext from './contexts/AuthContext'

function App() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="App">
      {user && (
        <div className="sidebar">
          <Link to="/">Home</Link>
          <Link to="/users">Users</Link>
          <Link to="/sessions">Sessions</Link>
          <Link to="/reflections">Reflections</Link>
          <button onClick={logout} style={{ marginTop: '2rem', width: '100%' }}>Logout</button>
        </div>
      )}
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          {user && (
            <>
              <Route path="/users" element={<Users />} />
              <Route path="/sessions" element={<Sessions />} />
              <Route path="/reflections" element={<Reflections />} />
            </>
          )}
          <Route path="*" element={<Home />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
