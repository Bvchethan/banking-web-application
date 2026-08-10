import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import StatCard from "../components/StatCard";
import api from "../services/api";
import { formatCurrency, formatNumber } from "../utils/formatters";

function TrendRow({ month, credit, debit }) {
  const creditValue = Number(credit || 0);
  const debitValue = Number(debit || 0);
  const maxValue = Math.max(creditValue, debitValue, 1);

  return (
    <div className="border-b border-slate-200 px-4 py-4 last:border-b-0">
      <div className="mb-3 flex items-center justify-between">
        <div className="text-[13px] font-semibold text-slate-900">{month}</div>
        <div className="text-[12px] text-slate-500">Monthly cash flow</div>
      </div>
      <div className="space-y-3">
        <div>
          <div className="mb-1 flex items-center justify-between text-[12px] text-slate-700">
            <span>Credits</span>
            <span>{formatCurrency(creditValue)}</span>
          </div>
          <div className="h-2 bg-slate-200">
            <div className="h-2 bg-emerald-600" style={{ width: `${(creditValue / maxValue) * 100}%` }} />
          </div>
        </div>
        <div>
          <div className="mb-1 flex items-center justify-between text-[12px] text-slate-700">
            <span>Debits</span>
            <span>{formatCurrency(debitValue)}</span>
          </div>
          <div className="h-2 bg-slate-200">
            <div className="h-2 bg-sky-800" style={{ width: `${(debitValue / maxValue) * 100}%` }} />
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
    <AppShell
      title="Financial Insights"
      subtitle="Track overall spending quality, savings ratio, and monthly inflow-outflow trends for the customer account."
    >
      <div className="grid gap-4 xl:grid-cols-4">
        <StatCard label="Health Score" value={formatNumber(insights?.financialHealthScore)} detail="Overall monthly financial health rating" accent="sky" />
        <StatCard label="Total Credits" value={formatCurrency(insights?.totalCredits)} detail="Aggregate inward account movement" accent="emerald" />
        <StatCard label="Total Debits" value={formatCurrency(insights?.totalDebits)} detail="Aggregate outward account movement" accent="amber" />
        <StatCard label="Savings Rate" value={`${formatNumber(insights?.savingsRate)}%`} detail="Share of income retained after expenses" accent="rose" />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
        <section className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Monthly Cash Flow Trend</div>
            </div>
            <div>
              {insights?.monthlyTrends?.length ? (
                insights.monthlyTrends.map((trend) => <TrendRow key={trend.month} {...trend} />)
              ) : (
                <div className="px-4 py-6 text-[13px] text-slate-500">Monthly trend data is not available.</div>
              )}
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Smart Suggestions</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              {insights?.smartSuggestions?.length ? (
                <ul className="space-y-2">
                  {insights.smartSuggestions.map((suggestion) => (
                    <li key={suggestion}>- {suggestion}</li>
                  ))}
                </ul>
              ) : (
                <div>No advisory suggestions are currently available.</div>
              )}
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Reading the Score</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              Higher scores indicate healthier savings discipline and more balanced monthly spending behavior. Lower scores suggest sustained debit pressure relative to credits.
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
