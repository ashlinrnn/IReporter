import { createBrowserRouter } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Activity from "./pages/Activity";
import IncidentDetail from "./pages/IncidentDetail";
import AdminDashboard from "./pages/AdminDashboard";
import Settings from "./pages/Settings";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard />,
  },
  {
    path: "/home",
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: "activity", element: <Activity /> },
      { path: "incident/:id", element: <IncidentDetail /> },
      { path: "admin", element: <AdminDashboard /> },
      { path: "settings", element: <Settings /> }
    ],
  },
]);