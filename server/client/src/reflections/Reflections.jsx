import React, { useState, useEffect, useContext } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import AuthContext from '../contexts/AuthContext'

const API_BASE = 'http://localhost:5003'

function Reflections() {
  const [reflections, setReflections] = useState([])
  const [users, setUsers] = useState([])
  const [sessions, setSessions] = useState([])
  const [editingReflection, setEditingReflection] = useState(null)
  const { user } = useContext(AuthContext)
  const currentUserId=parseInt(localStorage.getItem("user_id"))

  useEffect(() => {
    fetchReflections()
    fetchUsers()
    fetchSessions()
  }, [])

  const getHeaders = () => {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    }
  }

  const fetchReflections = async () => {
    try {
      const response = await fetch(`/reflections`, {
        headers: getHeaders()
      })
      const data = await response.json()
      setReflections(data)
    } catch (error) {
      console.error('Error fetching reflections:', error)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await fetch(`/users`, {
        headers: getHeaders()
      })
      const data = await response.json()
      setUsers(data)
    } catch (error) {
      console.error('Error fetching users:', error)
    }
  }

  const fetchSessions = async () => {
    try {
      const response = await fetch(`/sessions`, {
        headers: getHeaders()
      })
      const data = await response.json()
      setSessions(data)
    } catch (error) {
      console.error('Error fetching sessions:', error)
    }
  }

  const createReflection = async (values, { resetForm }) => {
    try {
      const response = await fetch(`/reflections`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(values)
      })
      if (response.ok) {
        fetchReflections()
        resetForm()
      }
    } catch (error) {
      console.error('Error creating reflection:', error)
    }
  }

  const updateReflection = async (values, { resetForm }) => {
    try {
      const response = await fetch(`/reflections/${editingReflection.id}`, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify(values)
      })
      if (response.ok) {
        fetchReflections()
        setEditingReflection(null)
        resetForm()
      }
    } catch (error) {
      console.error('Error updating reflection:', error)
    }
  }

  const deleteReflection = async (id) => {
    try {
      const response = await fetch(`/reflections/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      if (response.ok) {
        fetchReflections()
      }
    } catch (error) {
      console.error('Error deleting reflection:', error)
    }
  }

  const validationSchema = Yup.object({
    content: Yup.string().required('Content is required').min(10, 'Content must be at least 10 characters'),
    user_id: Yup.number().integer('Must be a valid user ID').required('User is required'),
    session_id: Yup.number().integer('Must be a valid session ID').required('Session is required')
  })

  return (
    <div>
      <h1>Reflections</h1>

      <h2>{editingReflection ? 'Edit Reflection' : 'Add New Reflection'}</h2>
      <Formik
        initialValues={editingReflection ? {
          content: editingReflection.content,
          user_id: editingReflection.user_id,
          session_id: editingReflection.session_id
        } : { content: '', user_id: '', session_id: '' }}
        validationSchema={validationSchema}
        onSubmit={editingReflection ? updateReflection : createReflection}
        enableReinitialize
      >
        <Form>
          <div>
            <label>Content:</label>
            <Field as="textarea" name="content" rows="4" />
            <ErrorMessage name="content" component="div" className="error" />
          </div>
          <div>
            <label>User:</label>
            <Field as="select" name="user_id">
              <option value="">Select User</option>
              {users.map(user => (
                <option key={user.id} value={user.id}>{user.name} ({user.email})</option>
              ))}
            </Field>
            <ErrorMessage name="user_id" component="div" className="error" />
          </div>
          <div>
            <label>Session:</label>
            <Field as="select" name="session_id">
              <option value="">Select Session</option>
              {sessions.map(session => (
                <option key={session.id} value={session.id}>{session.title} - {session.theme}</option>
              ))}
            </Field>
            <ErrorMessage name="session_id" component="div" className="error" />
          </div>
          <button type="submit">{editingReflection ? 'Update' : 'Create'}</button>
          {editingReflection && <button type="button" onClick={() => setEditingReflection(null)}>Cancel</button>}
        </Form>
      </Formik>

      <h2>All Reflections</h2>
      <ul>
        {reflections.map(reflection => {
  const user = users.find(u => u.id === reflection.user_id)
  const session = sessions.find(s => s.id === reflection.session_id)
  return (
    <li key={reflection.id}>
      <strong>{user ? user.name : 'Unknown User'} </strong>  
      on <em>{session ? session.title : 'Unknown Session'}</em>: {reflection.content}


  {reflection.user_id === currentUserId && (
    <>
      <button onClick={() => setEditingReflection(reflection)}>Edit</button>
      <button onClick={() => deleteReflection(reflection.id)}>Delete</button>
    </>
  )}
</li>
  )
})}
      </ul>
    </div>
  )
}

export default Reflections