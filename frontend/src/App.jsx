import { Navigate, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import CustomerDashboardPage from "./pages/CustomerDashboardPage";
import AdminDashboardPage from "./pages/AdminDashboardPage";
import TransferMoneyPage from "./pages/TransferMoneyPage";
import BeneficiaryManagementPage from "./pages/BeneficiaryManagementPage";
import TransactionHistoryPage from "./pages/TransactionHistoryPage";
import ProfilePage from "./pages/ProfilePage";
import FraudAnalyticsPage from "./pages/FraudAnalyticsPage";
import FinancialInsightsPage from "./pages/FinancialInsightsPage";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute allowedRoles={["ROLE_CUSTOMER", "ROLE_ADMIN"]} />}>
        <Route path="/dashboard" element={<CustomerDashboardPage />} />
        <Route path="/transfer" element={<TransferMoneyPage />} />
        <Route path="/beneficiaries" element={<BeneficiaryManagementPage />} />
        <Route path="/transactions" element={<TransactionHistoryPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/fraud-analytics" element={<FraudAnalyticsPage />} />
        <Route path="/financial-insights" element={<FinancialInsightsPage />} />
      </Route>

      <Route element={<ProtectedRoute allowedRoles={["ROLE_ADMIN"]} />}>
        <Route path="/admin" element={<AdminDashboardPage />} />
      </Route>
    </Routes>
  );
}
