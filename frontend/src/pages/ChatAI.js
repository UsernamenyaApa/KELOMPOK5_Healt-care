import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8004/chat';

const ChatAI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, input];
    setMessages(newMessages);
    setInput('');
    setLoading(true);
    try {
      const res = await axios.post(API_URL, { messages: newMessages });
      setMessages([...newMessages, res.data.reply]);
    } catch {
      setMessages([...newMessages, '[Error: gagal menghubungi layanan konsultasi]']);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', border: '1px solid #ccc', borderRadius: 8, padding: 16 }}>
      <h2>AI Konsultasi & Rekomendasi Dokter</h2>
      <div style={{ minHeight: 180, background: '#f9f9f9', padding: 8, borderRadius: 4, marginBottom: 12 }}>
        {messages.length === 0 && <div style={{ color: '#aaa' }}>Mulai chat dengan mengetik gejala Anda...</div>}
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: idx % 2 === 0 ? 'right' : 'left', margin: '6px 0' }}>
            <span style={{ background: idx % 2 === 0 ? '#d1e7dd' : '#e2e3e5', padding: '6px 12px', borderRadius: 16, display: 'inline-block' }}>{msg}</span>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Tulis gejala Anda..."
          style={{ flex: 1, padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading || !input.trim()}>Kirim</button>
      </div>
    </div>
  );
};

export default ChatAI;
