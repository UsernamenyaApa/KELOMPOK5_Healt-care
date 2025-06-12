import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import PatientPortal from './pages/PatientPortal';
import Doctors from './pages/Doctors';
import Appointments from './pages/Appointments';
import ChatAI from './pages/ChatAI';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="header">
          <div className="logo">HealthCare Hub</div>
          <nav>
            <Link to="/services">Services</Link>
            <Link to="/patient-portal">Patient Portal</Link>
            <Link to="/doctors">Doctors</Link>
            <Link to="/appointments">
              <button className="book-btn">Book Appointment</button>
            </Link>
            <Link to="/chat-ai">
              <button className="book-btn" style={{marginLeft: 8}}>AI Konsultasi</button>
            </Link>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/services" element={<Home />} />
            <Route path="/patient-portal" element={<PatientPortal />} />
            <Route path="/doctors" element={<Doctors />} />
            <Route path="/appointments" element={<Appointments />} />
            <Route path="/chat-ai" element={<ChatAI />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
