import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tenants, setTenants] = useState<{[key: string]: {api_key: string, modules: string[]}} | null>(null);
  const [selectedTenant, setSelectedTenant] = useState<string>('');
  const [apiKey, setApiKey] = useState('');
  const [query, setQuery] = useState('');
  const [antwort, setAntwort] = useState('');
  const [status, setStatus] = useState('');
  const [newTenant, setNewTenant] = useState({ name: '', api_key: '', modules: '' });
  const [addStatus, setAddStatus] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/tenants')
      .then(res => setTenants(res.data))
      .catch(() => setTenants(null));
  }, []);

  useEffect(() => {
    if (tenants && selectedTenant && tenants[selectedTenant]) {
      setApiKey(tenants[selectedTenant].api_key);
    }
  }, [selectedTenant, tenants]);

  const absenden = async () => {
    setStatus('');
    setAntwort('');
    try {
      const res = await axios.post('http://localhost:8000/query', { query }, {
        headers: { 'X-API-Key': apiKey }
      });
      setAntwort(JSON.stringify(res.data.antworten, null, 2));
    } catch (err: any) {
      setAntwort('');
      setStatus('Fehler: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleAddTenant = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddStatus('');
    try {
      const modulesArr = newTenant.modules.split(',').map(m => m.trim()).filter(Boolean);
      await axios.post('http://localhost:8000/tenants', {
        name: newTenant.name,
        api_key: newTenant.api_key,
        modules: modulesArr
      });
      setAddStatus('Tenant erfolgreich angelegt!');
      setNewTenant({ name: '', api_key: '', modules: '' });
      // Refresh tenants
      const res = await axios.get('http://localhost:8000/tenants');
      setTenants(res.data);
    } catch (err: any) {
      setAddStatus('Fehler: ' + (err.response?.data?.error || err.message));
    }
  };

  const handleDeleteTenant = async (tenantName: string) => {
    if (!window.confirm(`Tenant "${tenantName}" wirklich löschen?`)) return;
    setAddStatus('');
    try {
      await axios.delete(`http://localhost:8000/tenants/${tenantName}`);
      setAddStatus('Tenant gelöscht!');
      // Refresh tenants
      const res = await axios.get('http://localhost:8000/tenants');
      setTenants(res.data);
      if (selectedTenant === tenantName) {
        setSelectedTenant('');
        setApiKey('');
      }
    } catch (err: any) {
      setAddStatus('Fehler: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>MCP Web Client</h2>
      {tenants ? (
        <>
          <label>Tenant auswählen:&nbsp;
            <select value={selectedTenant} onChange={e => setSelectedTenant(e.target.value)}>
              <option value="">-- bitte wählen --</option>
              {Object.keys(tenants).map(k => (
                <option key={k} value={k}>{k}</option>
              ))}
            </select>
          </label>
          <br /><br />
        </>
      ) : <div>Tenants werden geladen...</div>}
      <input
        type="text"
        placeholder="API-Key"
        value={apiKey}
        onChange={e => setApiKey(e.target.value)}
        style={{ width: 300 }}
      /><br /><br />
      <textarea
        placeholder="Frage"
        rows={4}
        cols={50}
        value={query}
        onChange={e => setQuery(e.target.value)}
      /><br /><br />
      <button onClick={absenden} disabled={!apiKey || !query}>Senden</button>
      {status && <div style={{color:'red'}}>{status}</div>}
      <pre>{antwort}</pre>
      <hr style={{margin:'32px 0'}} />
      <h3>Neuen Tenant anlegen</h3>
      <form onSubmit={handleAddTenant} style={{marginBottom:16}}>
        <input
          type="text"
          placeholder="Tenant-Name"
          value={newTenant.name}
          onChange={e => setNewTenant({ ...newTenant, name: e.target.value })}
          required
        />&nbsp;
        <input
          type="text"
          placeholder="API-Key"
          value={newTenant.api_key}
          onChange={e => setNewTenant({ ...newTenant, api_key: e.target.value })}
          required
        />&nbsp;
        <input
          type="text"
          placeholder="Module (Komma-getrennt)"
          value={newTenant.modules}
          onChange={e => setNewTenant({ ...newTenant, modules: e.target.value })}
          required
        />&nbsp;
        <button type="submit">Anlegen</button>
      </form>
      {addStatus && <div style={{color: addStatus.startsWith('Fehler') ? 'red' : 'green'}}>{addStatus}</div>}
      {tenants && (
        <table style={{marginTop:16, borderCollapse:'collapse'}}>
          <thead>
            <tr><th>Tenant</th><th>API-Key</th><th>Module</th><th></th></tr>
          </thead>
          <tbody>
            {Object.entries(tenants).map(([k, v]) => (
              <tr key={k} style={{borderBottom:'1px solid #ccc'}}>
                <td>{k}</td>
                <td>{v.api_key}</td>
                <td>{v.modules.join(', ')}</td>
                <td>
                  <button onClick={() => handleDeleteTenant(k)} style={{color:'red'}}>Löschen</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;

