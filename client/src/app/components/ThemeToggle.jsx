import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [dark, setDark] = useState(true);

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

  return (
    <button
      onClick={() => setDark(prev => !prev)}
      className="fixed top-4 right-4 z-50 bg-white dark:bg-slate-800 text-slate-900 dark:text-white px-3 py-1 rounded"
    >
      {dark ? "🌙 Dark" : "☀️ Light"}
    </button>
  );
}