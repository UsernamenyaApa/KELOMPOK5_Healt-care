import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { graphqlFetch } from '../utils/graphql';
import './Appointments.css';
import Medicine from './Medicine';
import Modal from '../components/Modal';

const APPOINTMENT_GQL = 'http://localhost:8003/graphql';
const DOCTOR_GQL = 'http://localhost:8002/graphql';
const PATIENT_GQL = 'http://localhost:8001/graphql';

const Appointments = () => {
  const [showMedicine, setShowMedicine] = useState({ visible: false, appointmentId: null });
  const [form, setForm] = useState({ patient_id: '', specialization: '', doctor_id: '', schedule: '' });
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [filteredDoctors, setFilteredDoctors] = useState([]);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const location = useLocation();

  useEffect(() => {
    // Fetch doctors
    const doctorQuery = `query { doctors { id name specialization } }`;
    graphqlFetch(DOCTOR_GQL, doctorQuery).then(data => {
      setDoctors(data.doctors);
      setSpecializations([...new Set(data.doctors.map(doc => doc.specialization))]);
    });
    // Fetch patients
    const patientQuery = `query { patients { id name } }`;
    graphqlFetch(PATIENT_GQL, patientQuery).then(data => setPatients(data.patients));
    // Fetch appointments
    const appointmentsQuery = `query { appointments { id patientId doctorId schedule } }`;
    graphqlFetch(APPOINTMENT_GQL, appointmentsQuery).then(data => setAppointments(data.appointments));
  }, []);

  useEffect(() => {
    if (form.specialization) {
      setFilteredDoctors(doctors.filter(doc => doc.specialization === form.specialization));
    } else {
      setFilteredDoctors(doctors);
    }
  }, [form.specialization, doctors]);

  useEffect(() => {
    if (location.state && location.state.specialization) {
      setForm(f => ({ ...f, specialization: location.state.specialization, doctorId: location.state.doctorId || '' }));
    }
  }, [location.state]);

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
    if (name === 'specialization') {
      setForm(f => ({ ...f, doctorId: '' }));
    }
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setSuccessMsg('');
    setErrorMsg('');
    try {
      const mutation = `mutation($patientId: Int!, $doctorId: Int!, $schedule: String!) {
        createAppointment(patientId: $patientId, doctorId: $doctorId, schedule: $schedule) { id patientId doctorId schedule }
      }`;
      await graphqlFetch(APPOINTMENT_GQL, mutation, {
        patientId: parseInt(form.patientId),
        doctorId: parseInt(form.doctorId),
        schedule: form.schedule
      });
      setSuccessMsg('Appointment berhasil dijadwalkan.');
      // Refresh appointments
      const appointmentsQuery = `query { appointments { id patientId doctorId schedule } }`;
      graphqlFetch(APPOINTMENT_GQL, appointmentsQuery).then(data => setAppointments(data.appointments));
    } catch (err) {
      setErrorMsg('Gagal menjadwalkan appointment.');
    }
  };

  const getDoctor = id => doctors.find(x => x.id === id) || {};
  const getPatientName = id => {
    const p = patients.find(x => x.id === id);
    return p ? p.name : id;
  };

  const handleReschedule = async id => {
    const newSchedule = window.prompt('Masukkan jadwal baru (YYYY-MM-DDTHH:MM):');
    if (newSchedule) {
      try {
        const mutation = `mutation($appointmentId: Int!, $schedule: String!) {
          updateAppointment(appointmentId: $appointmentId, schedule: $schedule) { id patientId doctorId schedule }
        }`;
        await graphqlFetch(APPOINTMENT_GQL, mutation, { appointmentId: id, schedule: newSchedule });
        // Refresh appointments
        const appointmentsQuery = `query { appointments { id patientId doctorId schedule } }`;
        graphqlFetch(APPOINTMENT_GQL, appointmentsQuery).then(data => setAppointments(data.appointments));
      } catch {
        alert('Gagal mengubah jadwal appointment.');
      }
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this appointment?')) {
      try {
        const mutation = `mutation($appointmentId: Int!) {
          deleteAppointment(appointmentId: $appointmentId)
        }`;
        await graphqlFetch(APPOINTMENT_GQL, mutation, { appointmentId: id });
        setAppointments(appointments.filter(a => a.id !== id));
      } catch {
        alert('Failed to delete appointment.');
      }
    }
  };


  return (
    <div className="appointments-section">
      <h2>Jadwalkan Appointment</h2>
      <form onSubmit={handleSubmit} className="appointment-form">
        <select name="patient_id" value={form.patient_id} onChange={handleChange} required>
          <option value="">Pilih Pasien</option>
          {patients.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <select name="specialization" value={form.specialization} onChange={handleChange} required>
          <option value="">Pilih Spesialisasi</option>
          {specializations.map(sp => <option key={sp} value={sp}>{sp}</option>)}
        </select>
        <select name="doctor_id" value={form.doctor_id} onChange={handleChange} required>
          <option value="">Pilih Dokter</option>
          {filteredDoctors.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
        <input
          type="datetime-local"
          name="schedule"
          value={form.schedule}
          onChange={handleChange}
          required
        />
        <button type="submit">Jadwalkan</button>
      </form>
      {successMsg && <div style={{ color: 'green', marginTop: 10 }}>{successMsg}</div>}
      {errorMsg && <div style={{ color: 'red', marginTop: 10 }}>{errorMsg}</div>}

      <div className="appointments-list">
        <h3>Daftar Appointment</h3>
        {appointments.map(appt => {
          const doctor = getDoctor(appt.doctorId);
          return (
            <div className="appointment-card" key={appt.id}>
              <p><b>Pasien:</b> {getPatientName(appt.patientId)}</p>
              <p><b>Dokter:</b> {doctor.name || appt.doctorId} ({doctor.specialization || '-'})</p>
              <p><b>Jadwal:</b> {appt.schedule}</p>
              <button onClick={() => handleReschedule(appt.id)}>Reschedule</button>
              <button onClick={() => handleDelete(appt.id)} style={{marginLeft: 8}}>Delete</button>
              <button style={{marginLeft: 8}} onClick={() => setShowMedicine({ visible: true, appointmentId: appt.id })}>Beri Resep</button>
              {showMedicine.visible && showMedicine.appointmentId === appt.id && (
  <Modal onClose={() => setShowMedicine({ visible: false, appointmentId: null })}>
    <Medicine appointmentId={appt.id} isDoctor={true} onPrescriptionAdded={() => setShowMedicine({ visible: false, appointmentId: null })} />
    <button onClick={() => setShowMedicine({ visible: false, appointmentId: null })} style={{marginTop: 16}}>Tutup</button>
  </Modal>
)}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Appointments;
