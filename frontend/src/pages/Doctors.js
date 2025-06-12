import React, { useEffect, useState } from 'react';
import './Doctors.css';
import { useNavigate } from 'react-router-dom';
import { graphqlFetch } from '../utils/graphql';
import Medicine from './Medicine';
import Modal from '../components/Modal';

const DOCTOR_GQL = 'http://localhost:8002/graphql';

const Doctors = () => {
  const [doctors, setDoctors] = useState([]);
  const [selected, setSelected] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [showMedicineId, setShowMedicineId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const doctorQuery = `query { doctors { id name specialization } }`;
    graphqlFetch(DOCTOR_GQL, doctorQuery).then(data => setDoctors(data.doctors));
  }, []);

  const handleBook = (doctor) => {
    navigate('/appointments', { state: { specialization: doctor.specialization, doctor_id: doctor.id } });
  };

  const handleSelect = (doc) => {
    setSelected(doc);
    const apptQuery = `query($doctorId: Int!) { doctorAppointments(doctorId: $doctorId) { id patient_id schedule } }`;
    graphqlFetch(DOCTOR_GQL, apptQuery, { doctorId: doc.id }).then(data => setAppointments(data.doctorAppointments));
  };


  return (
    <div className="doctors-section">
      <h2>Daftar Dokter</h2>
      <div className="doctors-list">
        {doctors.map(doc => (
          <div className="doctor-card" key={doc.id}>
            <p><b>{doc.name}</b></p>
            <p>{doc.specialization}</p>
            <button onClick={() => handleBook(doc)}>Buat Appointment</button>
            <button onClick={() => handleSelect(doc)} style={{ marginLeft: 8 }}>Lihat Appointment</button>
            {selected && selected.id === doc.id && (
  <div className="appointment-list">
    <h4>Appointment</h4>
    {appointments.length === 0 ? <p>Tidak ada appointment.</p> : appointments.map(a => (
  <div key={a.id} className="appointment-card">
    <p><b>Pasien ID:</b> {a.patient_id}</p>
    <p><b>Jadwal:</b> {a.schedule}</p>
    <button onClick={() => setShowMedicineId(a.id)}>Beri Resep</button>
    {showMedicineId === a.id && (
      <Modal onClose={() => setShowMedicineId(null)}>
        <Medicine appointmentId={a.id} isDoctor={true} />
        <button onClick={() => setShowMedicineId(null)} style={{marginTop: 16}}>Tutup</button>
      </Modal>
    )}
  </div>
))}
  </div>
)}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Doctors;
