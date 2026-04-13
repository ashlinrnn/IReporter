import { createContext, useContext, useState, useEffect } from "react";
// import localRecords from "../../data/records.json";
import { api } from "../utils/api";

const RecordsContext = createContext({ records: [], loading: true, updateStatus: () => {}, deleteRecord: () => {}, editRecord: () => {} });

export function RecordsProvider({ children }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getRecords()
      .then(res => {
        if (!res.ok) throw new Error("Backend down");
        return res.json();
      })
      .then(data => {
        setRecords(Array.isArray(data) ? data : data.records || []);
        setLoading(false);
      })
      .catch(() => {
        // setRecords(localRecords.records);
        setLoading(false);
      });
  }, []);

  const updateStatus = (id, status) => {
    setRecords(prev => prev.map(r => r.id === id ? { ...r, status } : r));
    api.updateStatus(id, status).catch(console.error);
  };

  const deleteRecord = (id) => {
    setRecords(prev => prev.filter(r => r.id !== id));
    api.deleteRecord(id).catch(console.error);
  };

  const editRecord = (id, updates) => {
    setRecords(prev => prev.map(r => r.id === id ? { ...r, ...updates } : r));
    return api.updateRecord(id, updates);
  };

  return (
    <RecordsContext.Provider value={{ records, loading, updateStatus, deleteRecord, editRecord }}>
      {children}
    </RecordsContext.Provider>
  );
}

export const useRecords = () => useContext(RecordsContext);