import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useRecords } from "../context/RecordsContext";
import imagesData from "../../data/images.json";
import { ChevronLeft, ChevronRight, Search, Filter } from "lucide-react";
import kenyanFlag from '../../assets/catswithglasses-kenya-653064.png';

const PER_PAGE = 9; // good for 3x3 grid

export default function Activity() {
  const navigate = useNavigate();
  const { records, loading } = useRecords();
  const [page, setPage] = useState(1);
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  // Transform records to incidents (same as before)
  const allIncidents = records.map((record) => {
    const image = imagesData.images.find(img => img.record_id === record.id);
    return {
      id: record.id,
      title: record.title,
      status: record.status,
      type: record.type,
      timestamp: new Date(record.created_at).toLocaleString(),
      location: record.latitude && record.longitude ? `${record.latitude}, ${record.longitude}` : "No location provided",
      thumbnail: image?.image_url || kenyanFlag,
    };
  });

  // Apply filters
  const filteredIncidents = allIncidents.filter(incident => {
    // Search by title (case-insensitive)
    const matchesSearch = incident.title.toLowerCase().includes(searchTerm.toLowerCase());
    // Type filter
    const matchesType = typeFilter === "all" || incident.type === typeFilter;
    // Status filter
    const matchesStatus = statusFilter === "all" || incident.status === statusFilter;
    return matchesSearch && matchesType && matchesStatus;
  });

  const totalPages = Math.ceil(filteredIncidents.length / PER_PAGE);
  const paginated = filteredIncidents.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  // Reset page when filters change
  const handleFilterChange = () => {
    setPage(1);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-slate-500 dark:text-slate-400">
        Loading incidents...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-black italic text-slate-900 dark:text-white">ACTIVITY FEED</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-widest">
          {filteredIncidents.length} total reports
        </p>
      </div>


      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500" size={18} />
          <input
            type="text"
            placeholder="Search by title..."
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); handleFilterChange(); }}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder:text-slate-500 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          />
        </div>
        <div className="flex gap-3">
          <select
            value={typeFilter}
            onChange={(e) => { setTypeFilter(e.target.value); handleFilterChange(); }}
            className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white text-sm font-medium outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option value="red flag">Red Flag</option>
            <option value="intervention">Intervention</option>
          </select>
          <select
            value={statusFilter}
            onChange={(e) => { setStatusFilter(e.target.value); handleFilterChange(); }}
            className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white text-sm font-medium outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="under investigation">Under Investigation</option>
            <option value="rejected">Rejected</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>
      </div>


      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {paginated.map((incident) => (
          <div
            key={incident.id}
            onClick={() => navigate(`/home/incident/${incident.id}`)}
            className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl overflow-hidden cursor-pointer hover:border-blue-500 transition-all flex flex-col"
          >
      
            <div className="relative w-full pt-[56.25%] bg-slate-100 dark:bg-slate-900">
              <img
                src={incident.thumbnail}
                alt={incident.title}
                className="absolute inset-0 w-full h-full object-cover"
              />
            </div>
            <div className="p-4 space-y-1 flex flex-col flex-1">
              <div className="flex justify-between items-start gap-2">
                <h3 className="font-bold text-slate-900 dark:text-white text-sm sm:text-base line-clamp-2">
                  {incident.title}
                </h3>
                <span className={`px-2 py-1 rounded-full text-[10px] font-black uppercase whitespace-nowrap ${
                  incident.status === "pending" || incident.status === "red flag"
                    ? "bg-red-500/10 text-red-500 dark:text-red-400"
                    : incident.status === "under investigation"
                    ? "bg-orange-500/10 text-orange-500 dark:text-orange-400"
                    : incident.status === "rejected"
                    ? "bg-red-500/10 text-red-500 dark:text-red-400"
                    : "bg-emerald-500/10 text-emerald-500 dark:text-emerald-400"
                }`}>
                  {incident.status}
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">{incident.timestamp}</p>
              <p className="text-xs text-slate-400 dark:text-slate-500 truncate">
                📍 {incident.location}
              </p>
            </div>
          </div>
        ))}
      </div>


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