import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import Auth from '../components/Auth'

function Home() {
  const { user } = useContext(AuthContext);

  return (
    <div style={{ textAlign: 'center' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Welcome to Bible Club</h1>

      <p style={{ textAlign: 'center', fontSize: '1.2rem', marginBottom: '3rem' }}>
        Manage users, sessions, and reflections for your Bible study group.
      </p>

      {!user && (
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <Link to="/login" style={{ margin: '0 1rem' }}>
            <button style={{ padding: '0.75rem 1.5rem', fontSize: '1rem' }}>Login</button>
          </Link>
          <Link to="/signup" style={{ margin: '0 1rem' }}>
            <button style={{ padding: '0.75rem 1.5rem', fontSize: '1rem' }}>Signup</button>
          </Link>
        </div>
      )}

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem', justifyContent: 'center' }}>

        <div className="feature-card">
          <h2>ABOUT</h2>
          <p>Bible Club is a community where we come together to learn, share, and grow through God's Word. It is designed to be interactive and accessible for everyone—whether you are joining for the first time or already part of our sessions.</p>
        </div>

        <div className="feature-card">
          <h2>How It Works</h2>
          <ul>
            <li>Register</li>
               <p>If you are new, you can create a free account to become part of the Bible Club. Registration gives you access to all sessions, updates, and personalized features.</p>
          
            <li>Join Sessions</li>
               <p>Once registered, you can join live or scheduled Bible study sessions. Each session focuses on a specific passage, theme, or lesson, with opportunities to participate, ask questions, and share thoughts.</p>
          
            <li>Reflect and share</li>
               <p>After every session, you’ll have the chance to write your reflections. This is your space to share what you learned, how it touched your life, or even ask follow-up questions. Your feedback helps us grow as a community and also deepens your own learning journey.</p>
          </ul>
        </div>

        <div className="feature-card">
          <h2>Why Join?</h2>
          <ul>
            <li>Be part of a supportive, faith-filled community.</li>
            <li>Gain deeper understanding of the Bible in an engaging way.</li>
            <li>Track your personal reflections and spiritual growth.</li>
            <li>Share and learn from the experiences of others.</li>
          </ul>
            
        </div>

      </div>
    </div>
  )
}

export default Home