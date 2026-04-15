import { useNavigate } from "react-router-dom";
import { useRecords } from "../context/RecordsContext";
import { PlusCircle, Flag, Search, Clock, Trash2 } from "lucide-react";

export default function Home() {
  const navigate = useNavigate();
  const { records, loading, deleteRecord } = useRecords();
  const currentUser = JSON.parse(localStorage.getItem("user") || "{}");

  const myRecords = records.filter(r => r.user_id === currentUser?.id);

  const stats = {
    total: myRecords.length,
    redFlags: myRecords.filter(r => r.type === "red-flag").length,
    investigating: myRecords.filter(r => r.status === "investigating" || r.status === "under investigation").length,
    resolved: myRecords.filter(r => r.status === "resolved").length,
  };

  const statusColor = (status) => {
    if (status === "pending") return "bg-red-500/10 text-red-500 dark:text-red-400";
    if (status === "investigating" || status === "under investigation") return "bg-orange-500/10 text-orange-500 dark:text-orange-400";
    if (status === "resolved") return "bg-emerald-500/10 text-emerald-500 dark:text-emerald-400";
    if (status === "rejected") return "bg-slate-500/10 text-slate-500";
    return "bg-slate-500/10 text-slate-500";
  };

  const handleDelete = (e, record) => {
    e.stopPropagation(); 
    if (!window.confirm(`Delete "${record.title}"? This cannot be undone.`)) return;
    deleteRecord(record.id);
  };

  if (loading) return (
    <div className="flex items-center justify-center h-full text-slate-500 dark:text-slate-400">
      Loading...
    </div>
  );

  return (
    <div className="space-y-8 max-w-4xl mx-auto">

      {/* GREETING */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white">
            Welcome, {currentUser?.username || "Citizen"} 👋
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1 uppercase tracking-widest">
            Your reporting dashboard
          </p>
        </div>
        <button
          onClick={() => navigate("/home/report")}
          className="flex items-center gap-2 px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl transition-all shadow-lg shadow-blue-500/20"
        >
          <PlusCircle size={18}/> File Report
        </button>
      </div>

      {/* STATS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5">
          <p className="text-xs font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-2">Total Reports</p>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.total).padStart(2, '0')}</p>
        </div>
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 border-b-4 border-b-red-500">
          <p className="text-xs font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-2">Red Flags</p>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.redFlags).padStart(2, '0')}</p>
        </div>
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 border-b-4 border-b-orange-500">
          <p className="text-xs font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-2">Investigating</p>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.investigating).padStart(2, '0')}</p>
        </div>
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 border-b-4 border-b-emerald-500">
          <p className="text-xs font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-2">Resolved</p>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.resolved).padStart(2, '0')}</p>
        </div>
      </div>

      {/* MY REPORTS */}
      <div className="space-y-4">
        <h2 className="text-lg font-black text-slate-900 dark:text-white uppercase tracking-widest">My Reports</h2>

        {myRecords.length === 0 ? (
          <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-12 text-center space-y-4">
            <Flag size={40} className="mx-auto text-slate-300 dark:text-slate-600" />
            <p className="text-slate-500 dark:text-slate-400 font-bold">You haven't filed any reports yet.</p>
            <button
              onClick={() => navigate("/home/report")}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-xl transition-all"
            >
              File Your First Report
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {myRecords.map(record => (
              <div
                key={record.id}
                onClick={() => navigate(`/home/incident/${record.id}`)}
                className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 cursor-pointer hover:border-blue-500 transition-all flex items-center justify-between gap-4"
              >
                <div className="space-y-1 flex-1 min-w-0">
                  <p className="font-black text-slate-900 dark:text-white truncate">{record.title}</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {new Date(record.created_at).toLocaleString('en-KE', { dateStyle: 'medium', timeStyle: 'short' })}
                  </p>
                </div>
                <div className="flex items-center gap-3 flex-shrink-0">
                  <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${
                    record.type === "red-flag"
                      ? "bg-red-500/10 text-red-500 dark:text-red-400"
                      : "bg-blue-500/10 text-blue-500 dark:text-blue-400"
                  }`}>
                    {record.type}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${statusColor(record.status)}`}>
                    {record.status}
                  </span>

                  {/* DELETE — only when pending */}
                  {record.status === "pending" && (
                    <button
                      onClick={(e) => handleDelete(e, record)}
                      className="p-2 rounded-xl bg-red-500/10 text-red-500 dark:text-red-400 hover:bg-red-500/20 transition-all"
                      title="Delete report"
                    >
                      <Trash2 size={14}/>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* QUICK LINKS */}
      <div className="grid grid-cols-2 gap-4">
        <button
          onClick={() => navigate("/home/map")}
          className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 text-left hover:border-blue-500 transition-all space-y-2"
        >
          <Search size={24} className="text-blue-500" />
          <p className="font-black text-slate-900 dark:text-white">Live Map</p>
          <p className="text-xs text-slate-500 dark:text-slate.400">View all incidents on the map</p>
        </button>
        <button
          onClick={() => navigate("/home/activity")}
          className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 text-left hover:border-blue-500 transition-all space-y-2"
        >
          <Clock size={24} className="text-orange-500" />
          <p className="font-black text-slate-900 dark:text-white">Activity Feed</p>
          <p className="text-xs text-slate-500 dark:text-slate-400">Browse all community reports</p>
        </button>
      </div>
    </div>
  );
}