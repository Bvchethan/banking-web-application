import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import StatCard from "../components/StatCard";
import api from "../services/api";
import { formatCurrency, formatDateTime, maskAccountNumber, titleCase } from "../utils/formatters";

export default function CustomerDashboardPage() {
  const [account, setAccount] = useState(null);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const load = async () => {
      const [accountRes, transactionsRes] = await Promise.all([api.get("/customer/account"), api.get("/customer/transactions")]);
      setAccount(accountRes.data);
      setTransactions(transactionsRes.data || []);
    };

    load();
  }, []);

  const recentTransactions = transactions.slice(0, 6);
  const debitTransactions = transactions.filter((item) => item.type === "DEBIT");
  const creditTransactions = transactions.filter((item) => item.type === "CREDIT");
  const lastTransaction = transactions[0];

  return (
    <AppShell
      title="Account Overview"
      subtitle="Review available balance, recent account movement, and important servicing details from a single operational view."
    >
      <div className="grid gap-4 xl:grid-cols-4">
        <StatCard label="Available Balance" value={formatCurrency(account?.balance)} detail="Savings Account - Primary Ledger" accent="sky" />
        <StatCard label="Account Number" value={maskAccountNumber(account?.accountNumber)} detail="Branch: Retail Digital Banking" accent="emerald" />
        <StatCard label="Total Debits" value={formatCurrency(debitTransactions.reduce((sum, item) => sum + Number(item.amount || 0), 0))} detail={`${debitTransactions.length} posted debit entries`} accent="amber" />
        <StatCard label="Total Credits" value={formatCurrency(creditTransactions.reduce((sum, item) => sum + Number(item.amount || 0), 0))} detail={`${creditTransactions.length} posted credit entries`} accent="rose" />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
        <section className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Recent Transactions</div>
            </div>
            <div className="p-4">
              <DataTable
                columns={[
                  { key: "createdAt", label: "Date & Time", render: (value) => formatDateTime(value) },
                  { key: "referenceNumber", label: "Reference" },
                  { key: "type", label: "Entry Type", render: (value) => titleCase(value) },
                  {
                    key: "counterparty",
                    label: "Counterparty",
                    render: (_, row) => row.beneficiaryName || row.receiverName || row.senderName || "Retail Banking Transfer"
                  },
                  {
                    key: "debit",
                    label: "Debit",
                    render: (_, row) => (row.type === "DEBIT" ? formatCurrency(row.amount) : "--")
                  },
                  {
                    key: "credit",
                    label: "Credit",
                    render: (_, row) => (row.type === "CREDIT" ? formatCurrency(row.amount) : "--")
                  },
                  {
                    key: "status",
                    label: "Status",
                    render: () => <span className="status-chip border-emerald-200 bg-emerald-50 text-emerald-700">Posted</span>
                  }
                ]}
                rows={recentTransactions}
                emptyText="No transactions have been recorded for this account yet."
              />
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Service Snapshot</div>
            </div>
            <div className="grid gap-4 px-4 py-4 md:grid-cols-2 xl:grid-cols-4">
              <div>
                <div className="section-label">Product</div>
                <div className="mt-2 text-[14px] font-medium text-slate-900">NovaBank Savings Account</div>
              </div>
              <div>
                <div className="section-label">Currency</div>
                <div className="mt-2 text-[14px] font-medium text-slate-900">{account?.currency || "INR"}</div>
              </div>
              <div>
                <div className="section-label">Account Status</div>
                <div className="mt-2 text-[14px] font-medium text-slate-900">{account?.active === false ? "Dormant" : "Active"}</div>
              </div>
              <div>
                <div className="section-label">Last Posted Entry</div>
                <div className="mt-2 text-[14px] font-medium text-slate-900">{formatDateTime(lastTransaction?.createdAt)}</div>
              </div>
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Account Notices</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <div className="mb-3 border border-sky-200 bg-sky-50 px-3 py-3 text-sky-900">
                UPI, beneficiary transfer, and fraud checks remain active for this session.
              </div>
              <ul className="space-y-2">
                <li>- Review beneficiary details before initiating large transfers.</li>
                <li>- Use the fraud review page to inspect recent risk evaluations.</li>
                <li>- Update profile contact details if phone or address changes.</li>
              </ul>
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Next Recommended Actions</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <div className="mb-2 font-medium text-slate-900">Based on current activity:</div>
              <ul className="space-y-2">
                <li>- Validate beneficiary list before your next payment run.</li>
                <li>- Review transaction narration for audit clarity.</li>
                <li>- Check monthly spending insights to monitor savings rate.</li>
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
