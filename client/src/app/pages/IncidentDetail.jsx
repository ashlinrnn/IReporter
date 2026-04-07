import { useNavigate, useParams } from 'react-router';
import { useRecords } from '../context/RecordsContext';
import users from '../../data/users.json';
import images from '../../data/images.json';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { ArrowLeft, Clock, User, MapPin } from 'lucide-react';

const TIMELINE = [
  { key: 'red-flag', label: 'Red-Flag Reported' },
  { key: 'investigating', label: 'Under Investigation' },
  { key: 'resolved', label: 'Resolved' },
];

const STATUS_ORDER = ['red-flag', 'investigating', 'resolved'];

export default function IncidentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { records } = useRecords();

  const record = records.find(r => r.id === Number(id));
  const user = users.users.find(u => u.id === record?.user_id);
  const image = images.images.find(i => i.record_id === record?.id);

  if (!record) return (
    <div className="flex items-center justify-center h-full text-slate-500 dark:text-slate-400">
      Incident not found.
    </div>
  );

  const currentIndex = STATUS_ORDER.indexOf(record.status.toLowerCase().trim());

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">

      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all"
        >
          <ArrowLeft size={18} />
        </button>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white">Incident Details</h1>
      </div>

      {image?.image_url && (
        <div className="relative rounded-3xl overflow-hidden h-64">
          <img src={image.image_url} alt={record.title} className="w-full h-full object-cover" />
          <span className={`absolute top-4 right-4 px-4 py-1.5 rounded-full text-xs font-black uppercase text-white ${
            record.type === 'red-flag' ? 'bg-red-500' : 'bg-blue-500'
          }`}>
            {record.type}
          </span>
        </div>
      )}

      <div className="space-y-2">
        <h2 className="text-2xl font-black text-slate-900 dark:text-white">{record.title}</h2>
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
        <p className="text-slate-900 dark:text-white leading-relaxed">{record.description}</p>
      </div>

      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-6 space-y-4">
        <div className="flex items-center gap-2 text-blue-500 dark:text-blue-400">
          <MapPin size={18} />
          <h3 className="text-sm font-black uppercase tracking-widest">Location</h3>
        </div>
        <p className="text-slate-900 dark:text-white font-mono text-sm">{record.latitude}, {record.longitude}</p>
        <div className="h-48 rounded-xl overflow-hidden">
          <MapContainer
            center={[record.latitude, record.longitude]}
            zoom={14}
            className="h-full w-full"
            zoomControl={false}
          >
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
                    isCompleted
                      ? 'bg-emerald-500 border-emerald-500'
                      : 'bg-slate-100 dark:bg-slate-700 border-slate-300 dark:border-slate-600'
                  }`}>
                    {isCompleted && (
                      <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                  {!isLast && (
                    <div className={`w-0.5 h-10 ${isCompleted ? 'bg-emerald-500' : 'bg-slate-200 dark:bg-slate-700'}`} />
                  )}
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