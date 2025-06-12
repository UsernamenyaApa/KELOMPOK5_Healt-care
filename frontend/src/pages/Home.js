import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => (
  <div className="home-section">
    <h1>Your Health, Our Priority</h1>
    <p>Akses layanan kesehatan terbaik dengan platform kami. Hubungkan dengan dokter, kelola appointment, dan kendalikan perjalanan kesehatan Anda.</p>
    <div className="home-btns">
      <Link to="/patient-portal"><button>Mulai</button></Link>
      <a href="#services"><button>Pelajari Lebih Lanjut</button></a>
    </div>
    <section id="services" className="services-section">
      <h2>Layanan Kami</h2>
      <div className="services-cards">
        <div className="service-card">
          <h3>Layanan Pasien</h3>
          <p>Kelola data pasien dan riwayat appointment.</p>
          <Link to="/patient-portal"><button>Akses Portal Pasien</button></Link>
        </div>
        <div className="service-card">
          <h3>Layanan Dokter</h3>
          <p>Terhubung dengan tenaga medis profesional.</p>
          <Link to="/doctors"><button>Daftar Dokter</button></Link>
        </div>
        <div className="service-card">
          <h3>Layanan Appointment</h3>
          <p>Jadwalkan dan kelola kunjungan Anda.</p>
          <Link to="/appointments"><button>Buat Appointment</button></Link>
        </div>
      </div>
    </section>
  </div>
);

export default Home;
