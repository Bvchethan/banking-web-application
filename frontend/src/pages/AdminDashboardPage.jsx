import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import RiskBadge from "../components/RiskBadge";
import StatCard from "../components/StatCard";
import api from "../services/api";
import { formatCurrency, formatDateTime, formatNumber } from "../utils/formatters";

export default function AdminDashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [customers, setCustomers] = useState([]);
  const [fraudLogs, setFraudLogs] = useState([]);
  const [search, setSearch] = useState("");

  const load = async (query = "") => {
    const [dashboardRes, customerRes, fraudRes] = await Promise.all([
      api.get("/admin/dashboard"),
      api.get(`/admin/customers${query ? `?search=${query}` : ""}`),
      api.get("/admin/fraud-logs")
    ]);

    setDashboard(dashboardRes.data);
    setCustomers(customerRes.data || []);
    setFraudLogs(fraudRes.data || []);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <AppShell
      title="Operations Dashboard"
      subtitle="Monitor customer activity, transaction throughput, and fraud review queues from an administrative control view."
      actions={
        <button type="button" onClick={() => load(search)} className="button-secondary !px-3 !py-2">
          Refresh Data
        </button>
      }
    >
      <div className="grid gap-4 xl:grid-cols-4">
        <StatCard label="Customers" value={formatNumber(dashboard?.totalCustomers)} detail="Registered retail customers" accent="sky" />
        <StatCard label="Transactions" value={formatNumber(dashboard?.totalTransactions)} detail="Posted across all customer accounts" accent="emerald" />
        <StatCard label="High Risk Alerts" value={formatNumber(dashboard?.highRiskTransactions)} detail="Requires review by operations team" accent="rose" />
        <StatCard label="Transaction Volume" value={formatCurrency(dashboard?.totalVolume)} detail="Aggregate movement across monitored period" accent="amber" />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
        <section className="space-y-6">
          <div className="app-panel">
            <div className="flex flex-col gap-4 border-b border-slate-200 px-4 py-4 md:flex-row md:items-end md:justify-between">
              <div>
                <div className="panel-title">Customer Directory</div>
                <div className="mt-1 text-[13px] text-slate-600">Search customer records by name or email address.</div>
              </div>
              <div className="flex gap-3">
                <input
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  onKeyDown={(event) => event.key === "Enter" && load(search)}
                  placeholder="Search customer name or email"
                  className="form-control min-w-[280px]"
                />
                <button type="button" onClick={() => load(search)} className="button-primary">
                  Search
                </button>
              </div>
            </div>
            <div className="p-4">
              <DataTable
                columns={[
                  { key: "fullName", label: "Customer Name" },
                  { key: "email", label: "Email Address" },
                  { key: "phone", label: "Mobile Number" },
                  { key: "address", label: "Registered Address" }
                ]}
                rows={customers}
                emptyText="No customers matched the current search criteria."
              />
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Fraud Monitoring Queue</div>
            </div>
            <div className="p-4">
              <DataTable
                columns={[
                  { key: "referenceNumber", label: "Reference" },
                  { key: "riskLevel", label: "Risk Level", render: (value) => <RiskBadge risk={value} /> },
                  { key: "riskScore", label: "Score" },
                  { key: "evaluatedAmount", label: "Amount", render: (value) => formatCurrency(value) },
                  { key: "reasons", label: "Review Remarks" },
                  { key: "analyzedAt", label: "Reviewed At", render: (value) => formatDateTime(value) }
                ]}
                rows={fraudLogs.slice(0, 8)}
                emptyText="No fraud review items are currently available."
              />
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Operations Notes</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <ul className="space-y-2">
                <li>- Customer listings exclude password and internal authentication fields.</li>
                <li>- High-risk transactions should be reconciled with account and beneficiary history.</li>
                <li>- Use the search control to validate account ownership details during review.</li>
              </ul>
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Current Control Totals</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <div className="mb-2 flex items-center justify-between">
                <span>Customers onboarded</span>
                <span className="font-semibold text-slate-900">{formatNumber(dashboard?.totalCustomers)}</span>
              </div>
              <div className="mb-2 flex items-center justify-between">
                <span>Transactions booked</span>
                <span className="font-semibold text-slate-900">{formatNumber(dashboard?.totalTransactions)}</span>
              </div>
              <div className="mb-2 flex items-center justify-between">
                <span>High-risk alerts</span>
                <span className="font-semibold text-slate-900">{formatNumber(dashboard?.highRiskTransactions)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Volume observed</span>
                <span className="font-semibold text-slate-900">{formatCurrency(dashboard?.totalVolume)}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
