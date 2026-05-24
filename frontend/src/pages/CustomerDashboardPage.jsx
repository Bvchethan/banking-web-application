import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import StatCard from "../components/StatCard";
import DataTable from "../components/DataTable";
import api from "../services/api";

export default function CustomerDashboardPage() {
  const [account, setAccount] = useState(null);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const load = async () => {
      const [accountRes, transactionsRes] = await Promise.all([
        api.get("/customer/account"),
        api.get("/customer/transactions")
      ]);
      setAccount(accountRes.data);
      setTransactions(transactionsRes.data.slice(0, 5));
    };
    load();
  }, []);

  return (
    <AppShell title="Customer Dashboard" subtitle="Monitor balances, recent activity, and account health in one place.">
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Available Balance" value={`INR ${account?.balance || "0.00"}`} accent="teal" />
        <StatCard label="Account Number" value={account?.accountNumber || "Loading"} accent="blue" />
        <StatCard label="Currency" value={account?.currency || "INR"} accent="orange" />
      </div>

      <div className="mt-8">
        <h3 className="mb-4 text-xl font-semibold text-white">Recent Transactions</h3>
        <DataTable
          columns={[
            { key: "referenceNumber", label: "Reference" },
            { key: "type", label: "Type" },
            { key: "amount", label: "Amount", render: (value) => `INR ${value}` },
            { key: "description", label: "Description" }
          ]}
          rows={transactions}
        />
      </div>
    </AppShell>
  );
}
