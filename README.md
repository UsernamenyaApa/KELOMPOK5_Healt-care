# Dokumentasi API Healthcare v1.0

Selamat datang di dokumentasi resmi untuk API Healthcare. API ini menyediakan akses terpusat ke berbagai layanan dari sistem kami dan berfungsi sebagai pintu gerbang utama untuk semua integrasi.

## Informasi Umum

- **Base URL**: Setiap layanan memiliki URL dasar yang berbeda
- **Format Data**: Semua permintaan dan respons menggunakan format `JSON`
- **Autentikasi**: Saat ini tidak ada autentikasi yang diterapkan

---

## Endpoint Referensi

### 👨‍⚕️ Doctor Service

**Base URL**: `http://localhost:8002`

#### GraphQL API

> `POST http://localhost:8002/graphql`

Menyediakan akses ke data dokter melalui GraphQL.

**Query yang tersedia**:

- `doctors`: Mendapatkan semua dokter
- `doctor(doctor_id: Int!)`: Mendapatkan detail dokter berdasarkan ID
- `doctor_appointments(doctor_id: Int!)`: Mendapatkan semua janji temu untuk dokter tertentu

**Mutation yang tersedia**:

- `create_doctor(name: String!, specialization: String!)`: Membuat dokter baru

**Contoh Query**:
```graphql
query {
  doctors {
    id
    name
    specialization
  }
}

Contoh Respons Sukses (200 OK):
{
  "data": {
    "doctors": [
      {
        "id": 1,
        "name": "Dr. Andi",
        "specialization": "Cardiology"
      },
      {
        "id": 2,
        "name": "Dr. Budi",
        "specialization": "Dermatology"
      }
    ]
  }
}

### 👤 Patient Service
Base URL: http://localhost:8001

GraphQL API
POST http://localhost:8001/graphql


Menyediakan akses ke data pasien melalui GraphQL.

Query yang tersedia:

patients: Mendapatkan semua pasien
patient(patient_id: Int!): Mendapatkan detail pasien berdasarkan ID
patient_appointments(patient_id: Int!): Mendapatkan semua janji temu untuk pasien tertentu
Mutation yang tersedia:

create_patient(name: String!, age: Int!, gender: String!): Membuat pasien baru
Contoh Query:
