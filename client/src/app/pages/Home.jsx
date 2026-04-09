import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useRecords } from "../context/RecordsContext";
import Map from "../components/Map";
import { PlusCircle, X } from "lucide-react";

export default function Home() {
  const navigate = useNavigate();
  const { records } = useRecords(); 
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const [pinnedLocation, setPinnedLocation] = useState(null);
  const [pinMode, setPinMode] = useState(false);

  const filtered = records.filter((i) =>
    i.title?.toLowerCase().includes(search.toLowerCase())
  );

  const handleLocationPin = (coords) => {
    if (!pinMode) return;
    setPinnedLocation(coords);
  };

  const handleReportHere = () => {
    navigate("/home/report", { state: { location: pinnedLocation } });
  };

  return (
    <div className="h-full w-full relative">
      

      <button
        onClick={() => { setPinMode(!pinMode); setPinnedLocation(null); }}
        className={`absolute top-4 right-4 z-[1000] flex items-center gap-2 px-4 py-2 rounded-xl font-bold text-sm transition-all shadow-lg ${
          pinMode
            ? "bg-blue-600 text-white shadow-blue-500/30"
            : "bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-blue-500"
        }`}
      >
        <PlusCircle size={16} />
        {pinMode ? "Click map to pin" : "Pin Incident"}
      </button>

      <Map
        incidents={filtered}
        onSelect={setSelected}
        onLocationSelect={handleLocationPin}
        selectedLocation={pinnedLocation}
      />

      {pinnedLocation && (
        <div className="absolute bottom-4 right-4 z-[1000] bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white p-4 rounded-2xl shadow-2xl w-64 space-y-3">
          <div className="flex justify-between items-center">
            <p className="font-black text-sm uppercase tracking-widest">Location Pinned</p>
            <button onClick={() => setPinnedLocation(null)}>
              <X size={16} className="text-slate-400 hover:text-slate-900 dark:hover:text-white" />
            </button>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            {pinnedLocation[0].toFixed(5)}, {pinnedLocation[1].toFixed(5)}
          </p>
          <button
            onClick={handleReportHere}
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-xl text-sm flex items-center justify-center gap-2 transition-all"
          >
            <PlusCircle size={16} /> Report Here
          </button>
        </div>
      )}

      {selected && !pinnedLocation && (
        <div className="absolute bottom-4 left-4 z-[1000] bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white p-4 rounded-2xl shadow-2xl w-64 space-y-2">
          <div className="flex justify-between items-center">
            <h3 className="font-black">{selected.title}</h3>
            <button onClick={() => setSelected(null)}>
              <X size={16} className="text-slate-400 hover:text-slate-900 dark:hover:text-white" />
            </button>
          </div>
          <span className={`px-2 py-1 rounded-full text-[10px] font-black uppercase ${
            selected.status === "red-flag"
              ? "bg-red-500/10 text-red-500"
              : selected.status === "investigating"
              ? "bg-orange-500/10 text-orange-500"
              : "bg-emerald-500/10 text-emerald-500"
          }`}>
            {selected.status}
          </span>
          <button
            onClick={() => navigate(`/home/incident/${selected.id}`)}
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-xl text-sm transition-all"
          >
            View Details
          </button>
        </div>
      )}
    </div>
  );
}