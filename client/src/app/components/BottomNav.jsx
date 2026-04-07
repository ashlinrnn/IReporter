import { NavLink } from "react-router-dom";

export default function BottomNav() {
  const link = ({ isActive }) =>
    isActive ? "text-blue-400" : "text-gray-400";

  return (
    <div className="flex justify-around p-3 bg-white dark:bg-slate-800">
      <NavLink to="/home" className={link}>Map</NavLink>
      <NavLink to="/home/activity" className={link}>Activity</NavLink>
      <NavLink to="/home/admin" className={link}>Admin</NavLink>
      <NavLink to="/home/settings" className={link}>
        Settings
      </NavLink>
    </div>
  );
}