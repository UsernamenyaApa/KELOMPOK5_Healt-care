import React, { useEffect, useState } from 'react';
import './PatientPortal.css';
import { graphqlFetch } from '../utils/graphql';
import Medicine from './Medicine';
import Modal from '../components/Modal';

const PATIENT_GQL = 'http://localhost:8001/graphql';

const PatientPortal = () => {
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState({ name: '', age: '', gender: '' });
  const [selected, setSelected] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [showMedicineId, setShowMedicineId] = useState(null);

  useEffect(() => {
    const patientQuery = `query { patients { id name age gender } }`;
    graphqlFetch(PATIENT_GQL, patientQuery).then(data => setPatients(data.patients));
  }, []);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    const mutation = `mutation($name: String!, $age: Int!, $gender: String!) {
      createPatient(name: $name, age: $age, gender: $gender) { id name age gender }
    }`;
    const data = await graphqlFetch(PATIENT_GQL, mutation, {
      name: form.name,
      age: parseInt(form.age),
      gender: form.gender
    });
    setPatients([...patients, data.createPatient]);
    setForm({ name: '', age: '', gender: '' });
  };

  const handleSelect = p => {
    setSelected(p);
    const apptQuery = `query($patientId: Int!) { patientAppointments(patientId: $patientId) { id doctorId schedule } }`;
    graphqlFetch(PATIENT_GQL, apptQuery, { patientId: p.id }).then(data => setAppointments(data.patientAppointments));
  };

  return (
    <div className="patient-portal-section">
      <h2>Patient Portal</h2>
      <div className="portal-content">
        <form onSubmit={handleSubmit} className="patient-form">
          <h3>Personal Information</h3>
          <input name="name" placeholder="Full Name" value={form.name} onChange={handleChange} required />
          <input name="age" type="number" placeholder="Age" value={form.age} onChange={handleChange} required />
          <select name="gender" value={form.gender} onChange={handleChange} required>
            <option value="">Select Gender</option>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
          </select>
          <button type="submit">Update Profile</button>
        </form>
        <div className="medical-records">
          <h3>Medical Records</h3>
          {selected ? (
            <div>
              <p><b>Name:</b> {selected.name}</p>
              <p><b>Age:</b> {selected.age}</p>
              <p><b>Gender:</b> {selected.gender}</p>
              {selected && (
                <div className="appointment-list">
                  <h4>Appointments</h4>
                  {appointments.length === 0 ? <p>No appointments found.</p> : appointments.map(a => (
                    <div key={a.id}>
                      <p><b>Doctor ID:</b> {a.doctorId}</p>
                      <p><b>Schedule:</b> {a.schedule}</p>
                      <button onClick={() => setShowMedicineId(a.id)}>Lihat Resep</button>
                      {showMedicineId === a.id && (
                        <Modal onClose={() => setShowMedicineId(null)}>
                          <Medicine appointmentId={a.id} isDoctor={false} />
                          <button onClick={() => setShowMedicineId(null)} style={{marginTop: 16}}>Tutup</button>
                        </Modal>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : <p>Select a patient to view records</p>}
          <div className="patient-list">
            <h4>Patients</h4>
            {patients.map(p => (
              <button key={p.id} onClick={() => handleSelect(p)}>{p.name}</button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientPortal;
