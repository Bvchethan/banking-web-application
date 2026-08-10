import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import api from "../services/api";
import { formatCurrency, formatDateTime, formatNumber, titleCase } from "../utils/formatters";

export default function TransactionHistoryPage() {
  const [transactions, setTransactions] = useState([]);
  const [search, setSearch] = useState("");

  const load = async (query = "") => {
    const { data } = await api.get(`/customer/transactions${query ? `?search=${query}` : ""}`);
    setTransactions(data || []);
  };

  useEffect(() => {
    load();
  }, []);

  const debitCount = transactions.filter((item) => item.type === "DEBIT").length;
  const creditCount = transactions.filter((item) => item.type === "CREDIT").length;

  return (
    <AppShell
      title="Transaction History"
      subtitle="Search posted account activity by reference, beneficiary, or narration for customer servicing and audit review."
      actions={
        <button type="button" onClick={() => load(search)} className="button-secondary !px-3 !py-2">
          Refresh List
        </button>
      }
    >
      <div className="grid gap-4 md:grid-cols-3">
        <div className="app-panel px-4 py-4">
          <div className="section-label">Total Entries</div>
          <div className="mt-2 text-[24px] font-semibold text-slate-950">{formatNumber(transactions.length)}</div>
        </div>
        <div className="app-panel px-4 py-4">
          <div className="section-label">Debit Entries</div>
          <div className="mt-2 text-[24px] font-semibold text-slate-950">{formatNumber(debitCount)}</div>
        </div>
        <div className="app-panel px-4 py-4">
          <div className="section-label">Credit Entries</div>
          <div className="mt-2 text-[24px] font-semibold text-slate-950">{formatNumber(creditCount)}</div>
        </div>
      </div>

      <div className="mt-6 app-panel">
        <div className="flex flex-col gap-4 border-b border-slate-200 px-4 py-4 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="panel-title">Posted Transaction Listing</div>
            <div className="mt-1 text-[13px] text-slate-600">Use search to narrow by reference number or narration.</div>
          </div>
          <div className="flex gap-3">
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              onKeyDown={(event) => event.key === "Enter" && load(search)}
              placeholder="Search reference or description"
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
              { key: "createdAt", label: "Date & Time", render: (value) => formatDateTime(value) },
              { key: "referenceNumber", label: "Reference" },
              { key: "type", label: "Entry Type", render: (value) => titleCase(value) },
              {
                key: "counterparty",
                label: "Counterparty",
                render: (_, row) => row.beneficiaryName || row.receiverName || row.senderName || "Internal Transfer"
              },
              { key: "description", label: "Narration" },
              {
                key: "debit",
                label: "Debit",
                render: (_, row) => (row.type === "DEBIT" ? formatCurrency(row.amount) : "--")
              },
              {
                key: "credit",
                label: "Credit",
                render: (_, row) => (row.type === "CREDIT" ? formatCurrency(row.amount) : "--")
              }
            ]}
            rows={transactions}
            emptyText="No transactions were found for the selected filter."
          />
        </div>
      </div>
    </AppShell>
  );
}
