import { useState } from "react";
import { useRecords } from "../context/RecordsContext";
import { Shield, ChevronLeft, ChevronRight } from "lucide-react";

const PER_PAGE = 10;

export default function AdminDashboard() {
  const { records, updateStatus } = useRecords();
  const [page, setPage] = useState(1);

  const stats = {
    redFlags: records.filter(r => r.status === "red-flag").length,
    pending: records.filter(r => r.status === "under investigation").length,
    resolved: records.filter(r => r.status === "resolved").length,
  };

  const totalPages = Math.ceil(records.length / PER_PAGE);
  const paginated = records.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black italic text-slate-900 dark:text-white">ADMIN CONTROL</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm uppercase tracking-widest">Investigation Management</p>
        </div>
        <div className="bg-blue-600/10 text-blue-600 dark:text-blue-400 p-3 rounded-xl flex items-center gap-2 font-bold text-sm">
          <Shield size={18}/> AUTHORIZED ACCESS
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white dark:bg-slate-800 rounded-3xl shadow-xl border-b-4 border-red-500">
          <h4 className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase mb-2">Red-Flags</h4>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.redFlags).padStart(2, '0')}</p>
        </div>
        <div className="p-6 bg-white dark:bg-slate-800 rounded-3xl shadow-xl border-b-4 border-orange-500">
          <h4 className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase mb-2">Pending</h4>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.pending).padStart(2, '0')}</p>
        </div>
        <div className="p-6 bg-white dark:bg-slate-800 rounded-3xl shadow-xl border-b-4 border-emerald-500">
          <h4 className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase mb-2">Resolved</h4>
          <p className="text-4xl font-black italic text-slate-900 dark:text-white">{String(stats.resolved).padStart(2, '0')}</p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl overflow-hidden border border-slate-200 dark:border-slate-700">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 dark:bg-slate-900 text-[10px] font-black uppercase tracking-widest text-slate-500 dark:text-slate-400">
              <th className="p-6">Incident Details</th>
              <th className="p-6">Type</th>
              <th className="p-6 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
            {paginated.map((record) => (
              <tr key={record.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
                <td className="p-6">
                  <p className="font-bold text-slate-900 dark:text-white">{record.title}</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {new Date(record.created_at).toLocaleString()}
                  </p>
                </td>
                <td className="p-6">
                  <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${
                    record.type === "red-flag"
                      ? "bg-red-500/10 text-red-500 dark:text-red-400"
                      : "bg-blue-500/10 text-blue-500 dark:text-blue-400"
                  }`}>
                    {record.type}
                  </span>
                </td>
                <td className="p-6 text-right">
                  <select
                    value={record.status}
                    onChange={e => updateStatus(record.id, e.target.value)}
                    className="bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white p-2 rounded-lg text-xs font-bold outline-none cursor-pointer"
                  >
                    <option value='pending'>Pending</option>
                    <option value="under investigation">Under Investigation</option>
                    <option value="resolved">Resolved</option>
                    <option value="rejected">Rejected</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* PAGINATION */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between px-6 py-4 border-t border-slate-100 dark:border-slate-700">
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Showing {(page - 1) * PER_PAGE + 1}–{Math.min(page * PER_PAGE, records.length)} of {records.length}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="p-2 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 disabled:opacity-30 hover:border-blue-500 transition-all"
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
                      : "bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:border-blue-500"
                  }`}
                >
                  {n}
                </button>
              ))}
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="p-2 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 disabled:opacity-30 hover:border-blue-500 transition-all"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}