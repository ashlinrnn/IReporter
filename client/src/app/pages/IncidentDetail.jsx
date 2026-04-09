import { useState } from 'react';
import { useNavigate, useParams } from 'react-router';
import { useRecords } from '../context/RecordsContext';
import users from '../../data/users.json';
import images from '../../data/images.json';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { ArrowLeft, Clock, User, MapPin, Pencil, Trash2, Save, X } from 'lucide-react';

const TIMELINE = [
  { key: 'red-flag', label: 'Red-Flag Reported' },
  { key: 'investigating', label: 'Under Investigation' },
  { key: 'resolved', label: 'Resolved' },
];
const STATUS_ORDER = ['red-flag', 'investigating', 'resolved'];

export default function IncidentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { records, deleteRecord, editRecord } = useRecords();
  const currentUser = JSON.parse(localStorage.getItem("user") || "{}");

  const record = records.find(r => r.id === Number(id));
  const user = users.users.find(u => u.id === record?.user_id);
  const image = images.images.find(i => i.record_id === record?.id);

  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({ title: '', description: '' });
  const [deleting, setDeleting] = useState(false);

  if (!record) return (
    <div className="flex items-center justify-center h-full text-slate-500 dark:text-slate-400">
      Incident not found.
    </div>
  );

  const isPending = record.status === "red-flag";
  const isOwner = currentUser?.id === record?.user_id;
  const canEdit = isPending && isOwner;

  const currentIndex = STATUS_ORDER.indexOf(record.status.toLowerCase().trim());

  const handleEdit = () => {
    setEditData({ title: record.title, description: record.description });
    setEditing(true);
  };

  const handleSave = async () => {
    await editRecord(record.id, editData);
    setEditing(false);
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this report?")) return;
    setDeleting(true);
    deleteRecord(record.id);
    navigate(-1);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all"
          >
            <ArrowLeft size={18} />
          </button>
          <h1 className="text-2xl font-black text-slate-900 dark:text-white">Incident Details</h1>
        </div>

        {/* EDIT / DELETE — only if pending and owner */}
        {canEdit && !editing && (
          <div className="flex gap-2">
            <button
              onClick={handleEdit}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600/10 text-blue-600 dark:text-blue-400 rounded-xl text-sm font-bold hover:bg-blue-600/20 transition-all"
            >
              <Pencil size={14}/> Edit
            </button>
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="flex items-center gap-2 px-4 py-2 bg-red-500/10 text-red-500 dark:text-red-400 rounded-xl text-sm font-bold hover:bg-red-500/20 transition-all"
            >
              <Trash2 size={14}/> Delete
            </button>
          </div>
        )}

        {/* SAVE / CANCEL when editing */}
        {editing && (
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-xl text-sm font-bold hover:bg-emerald-500/20 transition-all"
            >
              <Save size={14}/> Save
            </button>
            <button
              onClick={() => setEditing(false)}
              className="flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-500 rounded-xl text-sm font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition-all"
            >
              <X size={14}/> Cancel
            </button>
          </div>
        )}
      </div>

      {image?.image_url && (
        <div className="relative rounded-3xl overflow-hidden h-64">
          <img src={image.image_url} alt={record.title} className="w-full h-full object-cover" />
          <span className={`absolute top-4 right-4 px-4 py-1.5 rounded-full text-xs font-black uppercase text-white ${
            record.type === 'red-flag' ? 'bg-red-500' : 'bg-blue-500'
          }`}>
            {record.type}
          </span>
          {isPending && isOwner && (
            <span className="absolute top-4 left-4 px-3 py-1.5 rounded-full text-xs font-black uppercase bg-amber-500 text-white">
              Pending — Editable
            </span>
          )}
        </div>
      )}

      <div className="space-y-2">
        {editing ? (
          <input
            value={editData.title}
            onChange={e => setEditData({...editData, title: e.target.value})}
            className="w-full text-2xl font-black bg-white dark:bg-slate-800 border border-blue-500 rounded-xl px-4 py-2 text-slate-900 dark:text-white outline-none"
          />
        ) : (
          <h2 className="text-2xl font-black text-slate-900 dark:text-white">{record.title}</h2>
        )}
        <div className="flex items-center gap-4 text-slate-500 dark:text-slate-400 text-sm">
          <span className="flex items-center gap-1">
            <Clock size={14} />
            {new Date(record.created_at).toLocaleString()}
          </span>
          <span className="flex items-center gap-1">
            <User size={14} />
            {user?.username || 'Unknown'}
          </span>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-6 space-y-2">
        <h3 className="text-sm font-black uppercase tracking-widest text-slate-500 dark:text-slate-400">Description</h3>
        {editing ? (
          <textarea
            value={editData.description}
            onChange={e => setEditData({...editData, description: e.target.value})}
            className="w-full bg-white dark:bg-slate-900 border border-blue-500 rounded-xl px-4 py-3 text-slate-900 dark:text-white outline-none h-32 resize-none"
          />
        ) : (
          <p className="text-slate-900 dark:text-white leading-relaxed">{record.description}</p>
        )}
      </div>

      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-6 space-y-4">
        <div className="flex items-center gap-2 text-blue-500 dark:text-blue-400">
          <MapPin size={18} />
          <h3 className="text-sm font-black uppercase tracking-widest">Location</h3>
        </div>
        <p className="text-slate-900 dark:text-white font-mono text-sm">{record.latitude}, {record.longitude}</p>
        <div className="h-48 rounded-xl overflow-hidden">
          <MapContainer center={[record.latitude, record.longitude]} zoom={14} className="h-full w-full" zoomControl={false}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <Marker position={[record.latitude, record.longitude]} />
          </MapContainer>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-6 space-y-4">
        <h3 className="text-sm font-black uppercase tracking-widest text-slate-500 dark:text-slate-400">Timeline</h3>
        <div className="space-y-0">
          {TIMELINE.map((step, index) => {
            const isCompleted = index <= currentIndex;
            const isLast = index === TIMELINE.length - 1;
            return (
              <div key={step.key} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 border-2 ${
                    isCompleted ? 'bg-emerald-500 border-emerald-500' : 'bg-slate-100 dark:bg-slate-700 border-slate-300 dark:border-slate-600'
                  }`}>
                    {isCompleted && (
                      <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                  {!isLast && <div className={`w-0.5 h-10 ${isCompleted ? 'bg-emerald-500' : 'bg-slate-200 dark:bg-slate-700'}`} />}
                </div>
                <div className="pb-2 pt-1">
                  <p className={`font-bold text-sm ${isCompleted ? 'text-slate-900 dark:text-white' : 'text-slate-400 dark:text-slate-500'}`}>
                    {step.label}
                  </p>
                  <p className="text-xs text-slate-400 dark:text-slate-500">
                    {isCompleted ? new Date(record.created_at).toLocaleString() : 'Pending'}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}