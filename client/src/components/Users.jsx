import React, { useState, useEffect } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'

const API_BASE = 'http://localhost:5003'

function Users() {
  const [users, setUsers] = useState([])
  const [editingUser, setEditingUser] = useState(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const getHeaders = () => {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_BASE}/users`, {
        headers: getHeaders()
      })
      const data = await response.json()
      setUsers(data)
    } catch (error) {
      console.error('Error fetching users:', error)
    }
  }

  const createUser = async (values, { resetForm }) => {
    try {
      const response = await fetch(`${API_BASE}/users`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(values)
      })
      if (response.ok) {
        fetchUsers()
        resetForm()
      }
    } catch (error) {
      console.error('Error creating user:', error)
    }
  }

  const updateUser = async (values, { resetForm }) => {
    try {
      const response = await fetch(`${API_BASE}/users/${editingUser.id}`, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify(values)
      })
      if (response.ok) {
        fetchUsers()
        setEditingUser(null)
        resetForm()
      }
    } catch (error) {
      console.error('Error updating user:', error)
    }
  }

  const deleteUser = async (id) => {
    try {
      const response = await fetch(`${API_BASE}/users/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      if (response.ok) {
        fetchUsers()
      }
    } catch (error) {
      console.error('Error deleting user:', error)
    }
  }

  const validationSchema = Yup.object({
    name: Yup.string().required('Name is required').min(2, 'Name must be at least 2 characters'),
    email: Yup.string().email('Invalid email format').required('Email is required'),
    password: Yup.string().required('Password is required').min(6, 'Password must be at least 6 characters')
  })

  const editValidationSchema = Yup.object({
    name: Yup.string().required('Name is required').min(2, 'Name must be at least 2 characters'),
    email: Yup.string().email('Invalid email format').required('Email is required'),
    password: Yup.string().min(6, 'Password must be at least 6 characters')
  })

  return (
    <div>
      <h1>Users</h1>

      <h2>{editingUser ? 'Edit User' : 'Add New User'}</h2>
      <Formik
        initialValues={editingUser ? { name: editingUser.name, email: editingUser.email, password: '' } : { name: '', email: '', password: '' }}
        validationSchema={editingUser ? editValidationSchema : validationSchema}
        onSubmit={editingUser ? updateUser : createUser}
        enableReinitialize
      >
        <Form>
          <div>
            <label>Name:</label>
            <Field type="text" name="name" />
            <ErrorMessage name="name" component="div" className="error" />
          </div>
          <div>
            <label>Email:</label>
            <Field type="email" name="email" />
            <ErrorMessage name="email" component="div" className="error" />
          </div>
          <div>
            <label>Password:</label>
            <Field type="password" name="password" />
            <ErrorMessage name="password" component="div" className="error" />
          </div>
          <button type="submit">{editingUser ? 'Update' : 'Create'}</button>
          {editingUser && <button type="button" onClick={() => setEditingUser(null)}>Cancel</button>}
        </Form>
      </Formik>

      <h2>All Users</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.name} - {user.email}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Users