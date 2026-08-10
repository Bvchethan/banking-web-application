import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import RiskBadge from "../components/RiskBadge";
import StatCard from "../components/StatCard";
import api from "../services/api";
import { formatCurrency, formatDateTime, formatNumber } from "../utils/formatters";

export default function FraudAnalyticsPage() {
  const [fraudLogs, setFraudLogs] = useState([]);

  useEffect(() => {
    api.get("/customer/fraud-analytics").then(({ data }) => setFraudLogs(data || []));
  }, []);

  const highRiskCount = fraudLogs.filter((item) => item.riskLevel === "HIGH").length;
  const mediumRiskCount = fraudLogs.filter((item) => item.riskLevel === "MEDIUM").length;
  const averageScore = fraudLogs.length
    ? Math.round(fraudLogs.reduce((sum, item) => sum + Number(item.riskScore || 0), 0) / fraudLogs.length)
    : 0;

  return (
    <AppShell
      title="Fraud Review"
      subtitle="Inspect customer transfer risk evaluations based on amount, transfer velocity, and beneficiary behavior."
    >
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Total Reviews" value={formatNumber(fraudLogs.length)} detail="Transactions evaluated for risk" accent="sky" />
        <StatCard label="High Risk Cases" value={formatNumber(highRiskCount)} detail="Requires immediate attention" accent="rose" />
        <StatCard label="Average Risk Score" value={formatNumber(averageScore)} detail="Across completed evaluations" accent="amber" />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
        <section className="app-panel">
          <div className="border-b border-slate-200 px-4 py-3">
            <div className="panel-title">Fraud Evaluation Log</div>
          </div>
          <div className="p-4">
            <DataTable
              columns={[
                { key: "referenceNumber", label: "Reference" },
                { key: "riskLevel", label: "Risk Status", render: (value) => <RiskBadge risk={value} /> },
                { key: "riskScore", label: "Score" },
                { key: "evaluatedAmount", label: "Amount", render: (value) => formatCurrency(value) },
                { key: "reasons", label: "Detection Reason" },
                { key: "analyzedAt", label: "Reviewed At", render: (value) => formatDateTime(value) }
              ]}
              rows={fraudLogs}
              emptyText="No fraud evaluations have been recorded for this customer."
            />
          </div>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Detection Rules</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <ul className="space-y-2">
                <li>- High transfer amount relative to recent customer activity.</li>
                <li>- Multiple rapid transfers in a short time window.</li>
                <li>- Transfer initiated to a newly added beneficiary.</li>
              </ul>
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Current Mix</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <div className="mb-2 flex items-center justify-between">
                <span>Low risk</span>
                <span className="font-semibold text-slate-900">{formatNumber(fraudLogs.length - highRiskCount - mediumRiskCount)}</span>
              </div>
              <div className="mb-2 flex items-center justify-between">
                <span>Medium risk</span>
                <span className="font-semibold text-slate-900">{formatNumber(mediumRiskCount)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>High risk</span>
                <span className="font-semibold text-slate-900">{formatNumber(highRiskCount)}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
