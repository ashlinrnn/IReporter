import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useRecords } from "../context/RecordsContext";
import imagesData from "../../data/images.json";
import { ChevronLeft, ChevronRight } from "lucide-react";

const PER_PAGE = 5;

export default function Activity() {
  const navigate = useNavigate();
  const { records, loading } = useRecords();
  const [page, setPage] = useState(1);

  const incidents = records.map((record) => {
    const image = imagesData.images.find(img => img.record_id === record.id);
    return {
      id: record.id,
      title: record.title,
      status: record.status,
      type: record.type,
      timestamp: new Date(record.created_at).toLocaleString(),
      location: `${record.latitude}, ${record.longitude}`,
      thumbnail: image?.image_url || "https://via.placeholder.com/400",
    };
  });

  const totalPages = Math.ceil(incidents.length / PER_PAGE);
  const paginated = incidents.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  if (loading) return (
    <div className="flex items-center justify-center h-full text-slate-500 dark:text-slate-400">
      Loading incidents...
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-black italic text-slate-900 dark:text-white">ACTIVITY FEED</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-widest">
          {incidents.length} total reports
        </p>
      </div>

      <div className="space-y-4">
        {paginated.map((incident) => (
          <div
            key={incident.id}
            onClick={() => navigate(`/home/incident/${incident.id}`)}
            className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl overflow-hidden cursor-pointer hover:border-blue-500 transition-all"
          >
            <img src={incident.thumbnail} alt={incident.title} className="w-full h-44 object-cover" />
            <div className="p-4 space-y-1">
              <div className="flex justify-between items-start">
                <h3 className="font-bold text-slate-900 dark:text-white">{incident.title}</h3>
                <span className={`px-2 py-1 rounded-full text-[10px] font-black uppercase flex-shrink-0 ${
                  incident.status === "red-flag"
                    ? "bg-red-500/10 text-red-500 dark:text-red-400"
                    : incident.status === "investigating"
                    ? "bg-orange-500/10 text-orange-500 dark:text-orange-400"
                    : "bg-emerald-500/10 text-emerald-500 dark:text-emerald-400"
                }`}>
                  {incident.status}
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">{incident.timestamp}</p>
              <p className="text-xs text-slate-400 dark:text-slate-500">📍 {incident.location}</p>
            </div>
          </div>
        ))}
      </div>

      {/* PAGINATION */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-700">
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Page {page} of {totalPages}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 disabled:opacity-30 hover:border-blue-500 transition-all"
            >
              <ChevronLeft size={16} />
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(n => (
              <button
                key={n}
                onClick={() => setPage(n)}
                className={`w-8 h-8 rounded-xl text-xs font-black transition-all ${
                  page === n
                    ? "bg-blue-600 text-white"
                    : "bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:border-blue-500"
                }`}
              >
                {n}
              </button>
            ))}
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 disabled:opacity-30 hover:border-blue-500 transition-all"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}