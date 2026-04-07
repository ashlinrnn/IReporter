import { createContext, useContext, useState } from "react";
import recordsData from "../../data/records.json";

const IncidentContext = createContext();

export default function IncidentProvider({ children }) {
  const [incidents, setIncidents] = useState(recordsData.records);

  const updateStatus = (id, status) => {
    setIncidents((prev) =>
      prev.map((i) =>
        i.id === id ? { ...i, status } : i
      )
    );
  };

  const addIncident = (incident) => {
    setIncidents((prev) => [...prev, incident]);
  };

  return (
    <IncidentContext.Provider value={{
      incidents,
      updateStatus,
      addIncident
    }}>
      {children}
    </IncidentContext.Provider>
  );
}

export const useIncidents = () => useContext(IncidentContext);