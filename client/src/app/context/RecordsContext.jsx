import { createContext, useContext, useState, useEffect } from "react";
import localRecords from "../../data/records.json";

const RecordsContext = createContext({ records: [], loading: true, updateStatus: () => {}, deleteRecord: () => {}, editRecord: () => {} });

const API = import.meta.env.VITE_API || "http://localhost:5000/api/v1";
const authHeader = () => ({ Authorization: `Bearer ${localStorage.getItem("token")}` });

export function RecordsProvider({ children }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/records`, { headers: authHeader() })
      .then(res => {
        if (!res.ok) throw new Error("Backend down");
        return res.json();
      })
      .then(data => {
        setRecords(Array.isArray(data) ? data : data.records || []);
        setLoading(false);
      })
      .catch(() => {
        setRecords(localRecords.records);
        setLoading(false);
      });
  }, []);

  const updateStatus = (id, status) => {
    setRecords(prev => prev.map(r => r.id === id ? { ...r, status } : r));
    fetch(`${API}/admin/records/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ status }),
    }).catch(console.error);
  };

  const deleteRecord = (id) => {
    setRecords(prev => prev.filter(r => r.id !== id));
    fetch(`${API}/records/me/${id}`, {
      method: "DELETE",
      headers: authHeader(),
    }).catch(console.error);
  };

  const editRecord = (id, updates) => {
    setRecords(prev => prev.map(r => r.id === id ? { ...r, ...updates } : r));
    return fetch(`${API}/records/me/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(updates),
    });
  };

  return (
    <RecordsContext.Provider value={{ records, loading, updateStatus, deleteRecord, editRecord }}>
      {children}
    </RecordsContext.Provider>
  );
}

export const useRecords = () => useContext(RecordsContext);