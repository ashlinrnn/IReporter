import { useState } from 'react';
import Map from '../components/Map';
import { Camera, Video, Send, AlertCircle, CheckCircle } from 'lucide-react';
import { useLocation } from "react-router-dom";
import { api } from "../utils/api";
import { useRecords } from "../context/RecordsContext";

const validate = (formData, location) => {
  const errors = {};
  if (!formData.title.trim()) errors.title = "Title is required";
  else if (formData.title.trim().length < 5) errors.title = "Title must be at least 5 characters";
  if (!formData.description.trim()) errors.description = "Description is required";
  else if (formData.description.trim().length < 20) errors.description = "Description must be at least 20 characters";
  if (!location) errors.location = "Please pin the incident location on the map";
  return errors;
};

export default function ReportSubmission() {
  const routerState = useLocation();
  const [formData, setFormData] = useState({ title: '', description: '', type: 'red flag' });
  const [location, setLocation] = useState(routerState.state?.location || null);
  const [images, setImages] = useState([]);
  const [video, setVideo] = useState(null);
  const [timestamp] = useState(new Date());
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState("");

  const { addRecord } = useRecords();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError("");
    const errs = validate(formData, location);
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;
    setLoading(true);

    try {
      const res = await api.createRecord({
        title: formData.title,
        description: formData.description,
        type: formData.type,
        latitude: location[0],
        longitude: location[1],
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || "Failed to submit report");
      }

      const record = await res.json();
      const newRecord=record.data
      addRecord(newRecord)
      const record_id = record.data.id;

      for (const img of images) {
        await api.uploadImage(record_id, img);
      }

      if (video) await api.uploadVideo(record_id, video);

      setSubmitted(true);
    } catch (err) {
      setSubmitError(err.message || "Submission failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const inputClass = (field) =>
    `w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-900 border ${
      errors[field] ? "border-red-500 focus:ring-red-500" : "border-slate-200 dark:border-slate-700 focus:ring-blue-500"
    } text-slate-900 dark:text-white outline-none focus:ring-2 placeholder:text-slate-500 transition-all`;

  if (submitted) return (
    <div className="max-w-md mx-auto mt-20 text-center space-y-4">
      <div className="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mx-auto">
        <CheckCircle className="w-8 h-8 text-emerald-500" />
      </div>
      <h2 className="text-2xl font-black text-slate-900 dark:text-white">Report Submitted!</h2>
      <p className="text-slate-500 dark:text-slate-400">Your report has been sent and will be reviewed by authorities. You'll receive an email update.</p>
      <button
        onClick={() => {
          setSubmitted(false);
          setFormData({ title: '', description: '', type: 'red flag' });
          setLocation(null);
          setImages([]);
          setVideo(null);
        }}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-xl transition-all"
      >
        Submit Another
      </button>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-black italic text-slate-900 dark:text-white">FILE A REPORT</h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm uppercase tracking-widest">Provide evidence for action</p>
      </header>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4 bg-white dark:bg-slate-800 p-6 rounded-3xl shadow-xl border border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-2 px-4 py-3 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-500 dark:text-slate-400 text-xs">
            <span>🕒</span>
            <span>Report time: <span className="text-slate-900 dark:text-white font-bold">
              {timestamp.toLocaleString('en-KE', { dateStyle: 'medium', timeStyle: 'short' })}
            </span></span>
          </div>

          <select
            className="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white font-bold outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            onChange={e => setFormData({...formData, type: e.target.value})}
          >
            <option value="red flag">🚩 Red-Flag (Corruption)</option>
            <option value="intervention">🛠️ Intervention (Infrastructure)</option>
          </select>

          <div>
            <input placeholder="Short Title" value={formData.title}
              className={inputClass("title")}
              onChange={e => { setFormData({...formData, title: e.target.value}); setErrors({...errors, title: ""}); }}
            />
            {errors.title && <p className="text-red-400 text-xs mt-1 pl-1 flex items-center gap-1"><AlertCircle size={12}/>{errors.title}</p>}
          </div>

          <div>
            <textarea placeholder="Detailed Description... (min 20 characters)" value={formData.description}
              className={`${inputClass("description")} h-40`}
              onChange={e => { setFormData({...formData, description: e.target.value}); setErrors({...errors, description: ""}); }}
            />
            {errors.description && <p className="text-red-400 text-xs mt-1 pl-1 flex items-center gap-1"><AlertCircle size={12}/>{errors.description}</p>}
          </div>

          <div className="flex gap-4">
            <label className="flex-1 flex items-center justify-center gap-2 p-4 bg-slate-100 dark:bg-slate-900 rounded-xl cursor-pointer hover:bg-blue-500/10 transition-all border-2 border-dashed border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400">
              <Camera size={20}/>
              <span className="text-xs font-bold">{images.length > 0 ? `${images.length} image(s)` : 'IMAGES'}</span>
              <input type="file" multiple hidden accept="image/*" onChange={e => setImages([...e.target.files])} />
            </label>
            <label className="flex-1 flex items-center justify-center gap-2 p-4 bg-slate-100 dark:bg-slate-900 rounded-xl cursor-pointer hover:bg-blue-500/10 transition-all border-2 border-dashed border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400">
              <Video size={20}/>
              <span className="text-xs font-bold">{video ? '✓ VIDEO' : 'VIDEO'}</span>
              <input type="file" hidden accept="video/*" onChange={e => setVideo(e.target.files[0])} />
            </label>
          </div>

          {submitError && (
            <div className="flex items-center gap-2 px-4 py-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">
              <AlertCircle size={14}/> {submitError}
            </div>
          )}
        </div>

        <div className="space-y-4">
          <div className={`h-[400px] rounded-3xl overflow-hidden shadow-2xl border-4 ${errors.location ? 'border-red-500' : 'border-slate-200 dark:border-slate-700'}`}>
            <Map onLocationSelect={(coords) => { setLocation(coords); setErrors({...errors, location: ""}); }} selectedLocation={location} />
          </div>
          {errors.location && <p className="text-red-400 text-xs pl-1 flex items-center gap-1"><AlertCircle size={12}/>{errors.location}</p>}
          {location && (
            <p className="text-xs text-slate-500 dark:text-slate-400 text-center">
              📍 {location[0].toFixed(5)}, {location[1].toFixed(5)}
            </p>
          )}
          <button onClick={handleSubmit} disabled={loading}
            className="w-full py-5 bg-blue-600 text-white font-black rounded-2xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-blue-500/20 flex items-center justify-center gap-3 transition-all">
            <Send size={20}/>
            {loading ? "Submitting..." : "SUBMIT TO AUTHORITIES"}
          </button>
        </div>
      </div>
    </div>
  );
}