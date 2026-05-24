import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import StatCard from "../components/StatCard";
import DataTable from "../components/DataTable";
import RiskBadge from "../components/RiskBadge";
import api from "../services/api";

export default function AdminDashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [customers, setCustomers] = useState([]);
  const [fraudLogs, setFraudLogs] = useState([]);
  const [search, setSearch] = useState("");

  const load = async (query = "") => {
    const [dashRes, customerRes, fraudRes] = await Promise.all([
      api.get("/admin/dashboard"),
      api.get(`/admin/customers${query ? `?search=${query}` : ""}`),
      api.get("/admin/fraud-logs")
    ]);
    setDashboard(dashRes.data);
    setCustomers(customerRes.data);
    setFraudLogs(fraudRes.data.slice(0, 5));
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <AppShell title="Admin Dashboard" subtitle="Enterprise visibility into customers, transfers, and platform fraud signals.">
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Customers" value={dashboard?.totalCustomers || 0} accent="teal" />
        <StatCard label="Transactions" value={dashboard?.totalTransactions || 0} accent="blue" />
        <StatCard label="High Risk Alerts" value={dashboard?.highRiskTransactions || 0} accent="rose" />
        <StatCard label="Transaction Volume" value={`INR ${dashboard?.totalVolume || 0}`} accent="orange" />
      </div>

      <div className="mt-8">
        <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <h3 className="text-xl font-semibold text-white">Customers</h3>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && load(search)}
            placeholder="Search by name or email"
            className="rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none"
          />
        </div>
        <DataTable
          columns={[
            { key: "fullName", label: "Customer" },
            { key: "email", label: "Email" },
            { key: "phone", label: "Phone" },
            { key: "address", label: "Address" }
          ]}
          rows={customers}
        />
      </div>

      <div className="mt-8">
        <h3 className="mb-4 text-xl font-semibold text-white">Latest Fraud Signals</h3>
        <DataTable
          columns={[
            { key: "referenceNumber", label: "Reference" },
            { key: "riskLevel", label: "Risk", render: (value) => <RiskBadge risk={value} /> },
            { key: "riskScore", label: "Score" },
            { key: "reasons", label: "Reasons" }
          ]}
          rows={fraudLogs}
        />
      </div>
    </AppShell>
  );
}
