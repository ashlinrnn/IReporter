import { createContext, useContext, useState, useEffect } from "react";
// import localRecords from "../../data/records.json";
import { api } from "../utils/api";

const RecordsContext = createContext({ records: [], loading: true, updateStatus: () => {}, deleteRecord: () => {}, editRecord: () => {} });

export function RecordsProvider({ children }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setLoading(false);
      return;
    }
    api.getRecords()
      .then(recordsList => {
        console.log("Records data:", recordsList);
        setRecords(Array.isArray(recordsList) ? recordsList : []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch records:", err);
        setRecords([]);
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
  const addRecord = (newRecord) => {
    setRecords(prev => [newRecord, ...prev]);
  };
  const refreshRecords = () => {
  api.getRecords()
    .then(recordsList => {
      setRecords(Array.isArray(recordsList) ? recordsList : []);
      setLoading(false);
    })
    .catch(err => console.error("Failed to refresh records:", err));  
  };

  return (
    <RecordsContext.Provider value={{ records, loading, updateStatus, deleteRecord, editRecord, addRecord,refreshRecords }}>
      {children}
    </RecordsContext.Provider>
  );
}

export const useRecords = () => useContext(RecordsContext);