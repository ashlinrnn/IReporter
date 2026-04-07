import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Mail, Lock, AlertCircle } from "lucide-react";

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); 
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [loading, setLoading] = useState(false);

  const inputClass = (field) =>
    `w-full px-4 py-3.5 rounded-xl bg-white dark:bg-slate-800 border ${
      errors[field] ? "border-red-500 focus:ring-red-500" : "border-slate-200 dark:border-slate-700 focus:ring-blue-500"
    } text-slate-900 dark:text-white placeholder:text-slate-500 focus:ring-2 outline-none transition-all`;

  const handleRequestCode = async (e) => {
    e.preventDefault();
    setServerError("");
    if (!email) { setErrors({ email: "Email is required" }); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { setErrors({ email: "Enter a valid email" }); return; }
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (res.ok) {
        setStep(2);
      } else {
        setServerError(data.message || "Email not found.");
      }
    } catch {
      // demo mode
      setStep(2);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setServerError("");
    if (!code.trim()) { setErrors({ code: "Please enter the code" }); return; }
    if (code.trim().length < 4) { setErrors({ code: "Invalid code" }); return; }
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/verify-reset-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code }),
      });
      const data = await res.json();
      if (res.ok) {
        setStep(3);
      } else {
        setServerError(data.message || "Invalid or expired code.");
      }
    } catch {
      
      setStep(3);
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setServerError("");
    const errs = {};
    if (!password) errs.password = "Password is required";
    else if (password.length < 6) errs.password = "Password must be at least 6 characters";
    if (!confirm) errs.confirm = "Please confirm your password";
    else if (password !== confirm) errs.confirm = "Passwords do not match";
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code, password }),
      });
      const data = await res.json();
      if (res.ok) {
        setStep(4);
      } else {
        setServerError(data.message || "Failed to reset password.");
      }
    } catch {
      // demo mode
      setStep(4);
    } finally {
      setLoading(false);
    }
  };

  const stepLabels = ["Email", "Verify", "Reset"];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#020c1b] text-white p-4">
      <div className="w-full max-w-md space-y-8">

        {/* HEADER */}
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-600 rounded-2xl font-black text-2xl mb-4">iR</div>
          <h1 className="text-4xl font-black tracking-tight">IReporter</h1>
          <p className="text-slate-400 mt-2">Reset your password</p>
        </div>

        {/* STEP INDICATOR */}
        {step < 4 && (
          <div className="flex items-center gap-2">
            {stepLabels.map((label, i) => (
              <div key={label} className="flex-1 flex flex-col items-center gap-1">
                <div className={`w-full h-1 rounded-full transition-all ${
                  step > i + 1 ? "bg-blue-600" : step === i + 1 ? "bg-blue-500" : "bg-slate-700"
                }`} />
                <span className={`text-[10px] uppercase tracking-widest font-black ${
                  step === i + 1 ? "text-blue-400" : "text-slate-600"
                }`}>{label}</span>
              </div>
            ))}
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-4">

          {/* STEP 1 — ENTER EMAIL */}
          {step === 1 && (
            <>
              <div className="text-center space-y-2 pb-2">
                <div className="w-14 h-14 bg-blue-600/10 rounded-2xl flex items-center justify-center mx-auto">
                  <Mail size={28} className="text-blue-500" />
                </div>
                <p className="text-slate-400 text-sm">Enter your email and we'll send you a reset code</p>
              </div>

              {serverError && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm px-4 py-3 rounded-xl flex items-center gap-2">
                  <AlertCircle size={14} /> {serverError}
                </div>
              )}

              <div>
                <input
                  type="email"
                  placeholder="Email address"
                  value={email}
                  className={inputClass("email")}
                  onChange={e => { setEmail(e.target.value); setErrors({}); }}
                />
                {errors.email && <p className="text-red-400 text-xs mt-1 pl-1 flex items-center gap-1"><AlertCircle size={12}/>{errors.email}</p>}
              </div>

              <button
                onClick={handleRequestCode}
                disabled={loading}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl font-black text-white transition-all"
              >
                {loading ? "Sending code..." : "Send Reset Code"}
              </button>

              <p className="text-center text-slate-500 text-sm">
                Remember your password?{" "}
                <Link to="/login" className="text-blue-400 hover:text-blue-300 transition-colors">Sign In</Link>
              </p>
            </>
          )}

          {/* STEP 2 — ENTER CODE */}
          {step === 2 && (
            <>
              <div className="text-center space-y-2 pb-2">
                <div className="w-14 h-14 bg-emerald-500/10 rounded-2xl flex items-center justify-center mx-auto">
                  <Mail size={28} className="text-emerald-500" />
                </div>
                <p className="text-slate-300 text-sm">Code sent to</p>
                <p className="text-white font-black">{email}</p>
                <p className="text-slate-500 text-xs">Check your inbox and enter the 6-digit code</p>
              </div>

              {serverError && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm px-4 py-3 rounded-xl flex items-center gap-2">
                  <AlertCircle size={14} /> {serverError}
                </div>
              )}

              <div>
                <input
                  type="text"
                  placeholder="000000"
                  value={code}
                  maxLength={8}
                  className={`w-full px-4 py-3.5 rounded-xl bg-white dark:bg-slate-800 border ${
                    errors.code ? "border-red-500" : "border-slate-700"
                  } text-slate-900 dark:text-white placeholder:text-slate-600 focus:ring-2 focus:ring-blue-500 outline-none text-center text-2xl tracking-[0.5em] font-black transition-all`}
                  onChange={e => { setCode(e.target.value); setErrors({}); }}
                />
                {errors.code && <p className="text-red-400 text-xs mt-1 text-center flex items-center justify-center gap-1"><AlertCircle size={12}/>{errors.code}</p>}
              </div>

              <button
                onClick={handleVerifyCode}
                disabled={loading}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl font-black text-white transition-all"
              >
                {loading ? "Verifying..." : "Verify Code"}
              </button>

              <button
                onClick={() => { setStep(1); setCode(""); setErrors({}); setServerError(""); }}
                className="w-full py-2 text-slate-500 hover:text-slate-300 text-sm transition-colors"
              >
                ← Try a different email
              </button>
            </>
          )}

          {/* STEP 3 — NEW PASSWORD */}
          {step === 3 && (
            <>
              <div className="text-center space-y-2 pb-2">
                <div className="w-14 h-14 bg-blue-600/10 rounded-2xl flex items-center justify-center mx-auto">
                  <Lock size={28} className="text-blue-500" />
                </div>
                <p className="text-slate-400 text-sm">Create a new password for your account</p>
              </div>

              {serverError && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm px-4 py-3 rounded-xl flex items-center gap-2">
                  <AlertCircle size={14} /> {serverError}
                </div>
              )}

              <div className="space-y-3">
                <div>
                  <input
                    type="password"
                    placeholder="New password"
                    value={password}
                    className={inputClass("password")}
                    onChange={e => { setPassword(e.target.value); setErrors({...errors, password: ""}); }}
                  />
                  {errors.password && <p className="text-red-400 text-xs mt-1 pl-1 flex items-center gap-1"><AlertCircle size={12}/>{errors.password}</p>}
                </div>
                <div>
                  <input
                    type="password"
                    placeholder="Confirm new password"
                    value={confirm}
                    className={inputClass("confirm")}
                    onChange={e => { setConfirm(e.target.value); setErrors({...errors, confirm: ""}); }}
                  />
                  {errors.confirm && <p className="text-red-400 text-xs mt-1 pl-1 flex items-center gap-1"><AlertCircle size={12}/>{errors.confirm}</p>}
                </div>
              </div>

              <button
                onClick={handleResetPassword}
                disabled={loading}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl font-black text-white transition-all"
              >
                {loading ? "Resetting..." : "Reset Password"}
              </button>
            </>
          )}

          {/* STEP 4 — SUCCESS */}
          {step === 4 && (
            <div className="text-center space-y-4 py-4">
              <div className="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-black text-white">Password Reset!</h2>
              <p className="text-slate-400 text-sm">Your password has been updated successfully.</p>
              <button
                onClick={() => navigate("/login")}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 rounded-xl font-black text-white transition-all"
              >
                Sign In
              </button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}