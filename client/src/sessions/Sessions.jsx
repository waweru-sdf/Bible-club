import React, { useState, useEffect } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const API_BASE = "http://localhost:5003";

function Sessions() {
  const [allSessions, setAllSessions] = useState([]);
  const [mySessions, setMySessions] = useState([]);
  const [users, setUsers] = useState([]);
  const [editingSession, setEditingSession] = useState(null);

  const currentUserId = localStorage.getItem("user_id");
  const token = localStorage.getItem("token");

  useEffect(() => {
    loadSessions();
    loadUsers();
  }, []);

  const getHeaders = () => {
    return {
      "Content-Type": "application/json",
      "Authorization": token ? `Bearer ${token}` : "",
    };
  };

  const loadSessions = async () => {
    const res = await fetch(`${API_BASE}/sessions`, { headers: getHeaders() });
    const data = await res.json();

    // Add helper fields so UI knows if current user already joined
    const decorated = data.map((s) => ({
      ...s,
      joined:
        String(s.facilitator_id) === String(currentUserId) ||
        s.members?.some((m) => String(m.id) === String(currentUserId)),
    }));

    setAllSessions(decorated);

    if (currentUserId) {
      const mine = decorated.filter((s) => s.joined);
      setMySessions(mine);
    }
  };

  const loadUsers = async () => {
    const res = await fetch(`${API_BASE}/users`, { headers: getHeaders() });
    const data = await res.json();
    setUsers(data);
  };

  const createSession = async (values, { resetForm }) => {
    await fetch(`${API_BASE}/sessions`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(values),
    });
    loadSessions();
    resetForm();
  };

  const updateSession = async (values, { resetForm }) => {
    await fetch(`${API_BASE}/sessions/${editingSession.id}`, {
      method: "PATCH",
      headers: getHeaders(),
      body: JSON.stringify(values),
    });
    loadSessions();
    setEditingSession(null);
    resetForm();
  };

  const deleteSession = async (id) => {
    await fetch(`${API_BASE}/sessions/${id}`, {
      method: "DELETE",
      headers: getHeaders(),
    });
    loadSessions();
  };

  async function joinSession(sessionId) {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/join`, {
      method: "POST",
      headers: getHeaders(),
    });

    if (!res.ok) throw new Error("Failed to join");

    const data = await res.json(); 

   
    setAllSessions((prev) =>
      prev.map((s) =>
        s.id === sessionId
          ? { ...s, joined: true, userSession: data }
          : s
      )
    );


    setMySessions((prev) => {
      const alreadyIn = prev.some((s) => s.id === sessionId);
      if (alreadyIn) return prev;
      const joinedSession = allSessions.find((s) => s.id === sessionId);
      return [...prev, { ...joinedSession, joined: true, userSession: data }];
    });
  }

  const validationSchema = Yup.object({
    title: Yup.string().required("Title is required"),
    theme: Yup.string().required("Theme is required"),
    facilitator_id: Yup.number().required("Facilitator is required"),
  });

  return (
    <div>
      <h1>Sessions</h1>

      <h2>{editingSession ? "Edit Session" : "Add New Session"}</h2>
      <Formik
        initialValues={
          editingSession
            ? {
                title: editingSession.title,
                theme: editingSession.theme,
                facilitator_id: editingSession.facilitator_id || "",
              }
            : { title: "", theme: "", facilitator_id: "" }
        }
        validationSchema={validationSchema}
        onSubmit={editingSession ? updateSession : createSession}
        enableReinitialize
      >
        <Form>
          <div>
            <label>Title:</label>
            <Field type="text" name="title" />
            <ErrorMessage name="title" component="div" />
          </div>
          <div>
            <label>Theme:</label>
            <Field type="text" name="theme" />
            <ErrorMessage name="theme" component="div" />
          </div>
          <div>
            <label>Facilitator:</label>
            <Field as="select" name="facilitator_id">
              <option value="">Select Facilitator</option>
              {users.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.name}
                </option>
              ))}
            </Field>
            <ErrorMessage name="facilitator_id" component="div" />
          </div>
          <button type="submit">
            {editingSession ? "Update" : "Create"}
          </button>
          {editingSession && (
            <button type="button" onClick={() => setEditingSession(null)}>
              Cancel
            </button>
          )}
        </Form>
      </Formik>

      <h2>All Sessions</h2>
      <ul>
        {allSessions.map((s) => (
          <li key={s.id}>
            {s.title} - {s.theme} (Facilitator Id:{" "}
            {s.facilitator_id ? s.facilitator_id : "None"})
            <div>
              {String(s.facilitator_id) === String(currentUserId) && (
                <>
                  <button onClick={() => setEditingSession(s)}>Edit</button>
                  <button onClick={() => deleteSession(s.id)}>Delete</button>
                </>
              )}

              {/* 🔹 Only show Join if not facilitator & not already joined */}
              {String(s.facilitator_id) !== String(currentUserId) && !s.joined && (
                <button onClick={() => joinSession(s.id)}>Join Session</button>
              )}

              {s.joined && String(s.facilitator_id) !== String(currentUserId) && (
                <button disabled>Already Joined</button>
              )}
            </div>
          </li>
        ))}
      </ul>

      <h2>My Sessions</h2>
      <ul>
        {mySessions.length > 0 ? (
          mySessions.map((s) => (
            <li key={s.id}>
              {s.title} - {s.theme}{" "}
              {String(s.facilitator_id) === String(currentUserId)
                ? "(Facilitator)"
                : "(Participant)"}
            </li>
          ))
        ) : (
          <p>You have no sessions.</p>
        )}
      </ul>
    </div>
  );
}

export default Sessions;
