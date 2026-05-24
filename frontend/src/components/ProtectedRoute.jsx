import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ allowedRoles }) {
  const { auth } = useAuth();
  const location = useLocation();

  if (!auth) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (!auth.roles?.some((role) => allowedRoles.includes(role))) {
    return <Navigate to={auth.roles?.includes("ROLE_ADMIN") ? "/admin" : "/dashboard"} replace />;
  }

  return <Outlet />;
}
