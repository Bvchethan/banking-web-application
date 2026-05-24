import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import api from "../services/api";

export default function TransactionHistoryPage() {
  const [transactions, setTransactions] = useState([]);
  const [search, setSearch] = useState("");

  const load = async (query = "") => {
    const { data } = await api.get(`/customer/transactions${query ? `?search=${query}` : ""}`);
    setTransactions(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <AppShell title="Transaction History" subtitle="Review account movement with searchable transaction references and descriptions.">
      <div className="mb-4 flex justify-end">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && load(search)}
          placeholder="Search transactions"
          className="rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none"
        />
      </div>

      <DataTable
        columns={[
          { key: "referenceNumber", label: "Reference" },
          { key: "type", label: "Type" },
          { key: "amount", label: "Amount", render: (value) => `INR ${value}` },
          { key: "beneficiaryName", label: "Beneficiary" },
          { key: "description", label: "Description" },
          { key: "createdAt", label: "Date", render: (value) => new Date(value).toLocaleString() }
        ]}
        rows={transactions}
      />
    </AppShell>
  );
}
