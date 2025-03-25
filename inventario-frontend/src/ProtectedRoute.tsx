import {useAuth} from "react-oidc-context";
import {Navigate, Outlet} from "react-router-dom";

export function ProtectedRoute() {
    const { isAuthenticated } = useAuth();
    return isAuthenticated ? <Outlet /> : <Navigate to="/home" replace />;
}