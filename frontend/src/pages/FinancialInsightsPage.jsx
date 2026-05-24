import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import StatCard from "../components/StatCard";
import api from "../services/api";

function TrendBar({ month, credit, debit }) {
  const maxValue = Math.max(Number(credit), Number(debit), 1);
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm text-slate-300">{month}</span>
        <span className="text-xs text-slate-400">Monthly flow</span>
      </div>
      <div className="space-y-3">
        <div>
          <div className="mb-1 flex justify-between text-xs text-slate-300">
            <span>Credit</span>
            <span>INR {credit}</span>
          </div>
          <div className="h-3 rounded-full bg-white/10">
            <div className="h-3 rounded-full bg-emerald-400" style={{ width: `${(Number(credit) / maxValue) * 100}%` }} />
          </div>
        </div>
        <div>
          <div className="mb-1 flex justify-between text-xs text-slate-300">
            <span>Debit</span>
            <span>INR {debit}</span>
          </div>
          <div className="h-3 rounded-full bg-white/10">
            <div className="h-3 rounded-full bg-orange-400" style={{ width: `${(Number(debit) / maxValue) * 100}%` }} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function FinancialInsightsPage() {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    api.get("/customer/financial-insights").then(({ data }) => setInsights(data));
  }, []);

  return (
    <AppShell title="Financial Insights" subtitle="Track financial health score, savings patterns, and monthly spending signals.">
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Health Score" value={insights?.financialHealthScore || 0} accent="teal" />
        <StatCard label="Total Credits" value={`INR ${insights?.totalCredits || 0}`} accent="blue" />
        <StatCard label="Total Debits" value={`INR ${insights?.totalDebits || 0}`} accent="orange" />
        <StatCard label="Savings Rate" value={`${insights?.savingsRate || 0}%`} accent="rose" />
      </div>

      <div className="mt-8 grid gap-4 lg:grid-cols-2">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h3 className="text-xl font-semibold text-white">Smart Suggestions</h3>
          <div className="mt-4 space-y-3">
            {insights?.smartSuggestions?.map((suggestion) => (
              <div key={suggestion} className="rounded-2xl bg-slate-950/50 p-4 text-slate-300">
                {suggestion}
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          {insights?.monthlyTrends?.map((trend) => (
            <TrendBar key={trend.month} {...trend} />
          ))}
        </div>
      </div>
    </AppShell>
  );
}
