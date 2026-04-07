import { createContext, useContext, useState, useEffect } from "react";
import localRecords from "../../data/records.json";

const RecordsContext = createContext();

export function RecordsProvider({ children }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
useEffect(() => {
  fetch("http://localhost:5000/api/records", {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  })
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
    fetch(`http://localhost:5000/api/records/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ status }),
    }).catch(console.error);
  };

  return (
    <RecordsContext.Provider value={{ records, loading, updateStatus }}>
      {children}
    </RecordsContext.Provider>
  );
}

export const useRecords = () => useContext(RecordsContext);