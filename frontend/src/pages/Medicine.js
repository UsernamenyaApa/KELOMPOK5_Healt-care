import React, { useEffect, useState } from 'react';
import { graphqlFetch, SHIPMENT_GQL } from '../utils/graphql';

const MEDICINE_GQL = 'http://localhost:8004/graphql';

const Medicine = ({ appointmentId, isDoctor, onPrescriptionAdded, isViewOnly = false, patientId }) => {
  const [medicines, setMedicines] = useState([]);
  const [draftPrescription, setDraftPrescription] = useState([]); // [{medicine_id, quantity}]
  const [displayPrescription, setDisplayPrescription] = useState([]); // hasil getReceipt
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [shipment, setShipment] = useState(null);
  const [shipmentLoading, setShipmentLoading] = useState(false);

  // Ambil daftar obat
  useEffect(() => {
    const query = `query { medicines { id name price description } }`;
    graphqlFetch(MEDICINE_GQL, query).then(data => setMedicines(data.medicines));
  }, []);

  // Ambil resep yang sudah diberikan untuk appointment ini
  useEffect(() => {
    if (appointmentId) {
      const receiptQuery = `query($appointmentId: Int!) { getReceipt(appointmentId: $appointmentId) { medicines { name quantity pricePerUnit total } totalAmount } }`;
      graphqlFetch(MEDICINE_GQL, receiptQuery, { appointmentId: appointmentId }).then(data => {
        setDisplayPrescription((data.getReceipt && data.getReceipt.medicines) || []);
      });
    }
  }, [appointmentId, successMsg]);

  // Cek status pengiriman untuk appointment ini
  useEffect(() => {
    if (appointmentId && !isDoctor) {
      setShipmentLoading(true);
      const shipmentQuery = `query($orderId: ID!) { shipmentsByOrder(order_id: $orderId) { id tracking_number carrier status shipping_address estimated_delivery updates { status location description created_at } } }`;
      
      // Asumsikan appointment_id sama dengan order_id untuk demo
      graphqlFetch(SHIPMENT_GQL, shipmentQuery, { orderId: appointmentId.toString() })
        .then(data => {
          if (data && data.shipmentsByOrder && data.shipmentsByOrder.length > 0) {
            setShipment(data.shipmentsByOrder[0]);
          }
          setShipmentLoading(false);
        })
        .catch(err => {
          console.error('Error fetching shipment:', err);
          setShipmentLoading(false);
        });
    }
  }, [appointmentId, isDoctor]);

  const handleAddToPrescription = (medicine_id) => {
    setDraftPrescription(prev => {
      if (prev.find(p => p.medicine_id === medicine_id)) return prev;
      return [...prev, { medicine_id, quantity: 1 }];
    });
  };

  const handleQuantityChange = (medicine_id, qty) => {
    setDraftPrescription(prev => prev.map(p => p.medicine_id === medicine_id ? { ...p, quantity: qty } : p));
  };

  const handleRemove = (medicine_id) => {
    setDraftPrescription(prev => prev.filter(p => p.medicine_id !== medicine_id));
  };

  const handleSubmitPrescription = async () => {
    setSuccessMsg('');
    setErrorMsg('');
    try {
      const mutation = `mutation($appointmentId: Int!, $medicines: [Int!]!, $quantities: [Int!]!) { addMedicinesToAppointment(appointmentId: $appointmentId, medicines: $medicines, quantities: $quantities) }`;
      await graphqlFetch(MEDICINE_GQL, mutation, {
        appointmentId: appointmentId,
        medicines: draftPrescription.map(p => p.medicine_id),
        quantities: draftPrescription.map(p => parseInt(p.quantity))
      });
      setSuccessMsg('Resep berhasil ditambahkan ke appointment.');
      setDraftPrescription([]);
      // Display prescription akan otomatis refresh via useEffect [successMsg]
      if (onPrescriptionAdded) onPrescriptionAdded();
    } catch (err) {
      setErrorMsg('Gagal menambahkan resep.');
    }
  };

  const handleCreateShipment = async () => {
    if (!patientId || !appointmentId) {
      setErrorMsg('Data pasien atau appointment tidak lengkap');
      return;
    }

    setShipmentLoading(true);
    try {
      const mutation = `
        mutation($orderId: ID!, $userId: ID!) { 
          createShipment(order_id: $orderId, user_id: $userId) { 
            id tracking_number status estimated_delivery 
          } 
        }`;
      
      const result = await graphqlFetch(SHIPMENT_GQL, mutation, {
        orderId: appointmentId.toString(),
        userId: patientId.toString()
      });
      
      if (result && result.createShipment) {
        setShipment(result.createShipment);
        setSuccessMsg('Pengiriman obat berhasil dibuat!');
      }
    } catch (err) {
      console.error('Error creating shipment:', err);
      setErrorMsg(`Gagal membuat pengiriman: ${err.message}`);
    } finally {
      setShipmentLoading(false);
    }
  };

  return (
    <div style={{ margin: '24px 0' }}>
      {!isViewOnly && (
        <>
          <h3>Daftar Obat</h3>
          <ul>
            {medicines.map(m => (
              <li key={m.id} style={{ marginBottom: 8 }}>
                <b>{m.name}</b> (Rp{m.price}) - {m.description}
                {isDoctor && (
                  <>
                    <button style={{ marginLeft: 8 }} onClick={() => handleAddToPrescription(m.id)} disabled={!!draftPrescription.find(p => p.medicine_id === m.id)}>
                      Tambah ke Resep
                    </button>
                    <input
                      type="number"
                      min={1}
                      value={draftPrescription.find(p => p.medicine_id === m.id)?.quantity || 1}
                      onChange={e => handleQuantityChange(m.id, e.target.value)}
                      style={{ width: 50, marginLeft: 8 }}
                    />
                    <button style={{ marginLeft: 8 }} onClick={() => handleRemove(m.id)}>
                      Hapus
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>
          {isDoctor && draftPrescription.length > 0 && (
            <button style={{ marginTop: 12 }} onClick={handleSubmitPrescription}>Simpan Resep ke Appointment</button>
          )}
          {successMsg && <div style={{ color: 'green', marginTop: 8 }}>{successMsg}</div>}
          {errorMsg && <div style={{ color: 'red', marginTop: 8 }}>{errorMsg}</div>}
        </>
      )}
      {displayPrescription.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h4>Resep yang sudah diberikan:</h4>
          {displayPrescription.map((p, idx) => (
            <div key={idx}>
              {p.name} - {p.quantity} {p.pricePerUnit ? `(Rp${p.pricePerUnit} x ${p.quantity} = Rp${p.total})` : ''}
            </div>
          ))}
          
          {!isDoctor && !shipment && displayPrescription.length > 0 && (
            <div style={{ marginTop: 16 }}>
              <button 
                onClick={handleCreateShipment} 
                disabled={shipmentLoading}
                style={{ backgroundColor: '#4CAF50', color: 'white', padding: '10px 15px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                {shipmentLoading ? 'Memproses...' : 'Pesan Pengiriman Obat'}
              </button>
            </div>
          )}
          
          {shipment && (
            <div style={{ marginTop: 16, padding: 16, border: '1px solid #ddd', borderRadius: 8 }}>
              <h4>Status Pengiriman Obat</h4>
              <p><b>Nomor Tracking:</b> {shipment.tracking_number}</p>
              <p><b>Status:</b> {shipment.status}</p>
              {shipment.carrier && <p><b>Kurir:</b> {shipment.carrier}</p>}
              {shipment.estimated_delivery && (
                <p><b>Estimasi Tiba:</b> {new Date(shipment.estimated_delivery).toLocaleDateString('id-ID')}</p>
              )}
              {shipment.updates && shipment.updates.length > 0 && (
                <div>
                  <h5>Riwayat Status:</h5>
                  <ul style={{ paddingLeft: 20 }}>
                    {shipment.updates.map((update, idx) => (
                      <li key={idx}>
                        <b>{new Date(update.created_at).toLocaleString('id-ID')}</b> - {update.status}
                        {update.location && ` di ${update.location}`}
                        {update.description && <div>{update.description}</div>}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Medicine;
