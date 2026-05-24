import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import RiskBadge from "../components/RiskBadge";
import api from "../services/api";

export default function FraudAnalyticsPage() {
  const [fraudLogs, setFraudLogs] = useState([]);

  useEffect(() => {
    api.get("/customer/fraud-analytics").then(({ data }) => setFraudLogs(data));
  }, []);

  return (
    <AppShell title="Fraud Analytics" subtitle="AI-powered risk scoring highlights suspicious behavior and transfer patterns.">
      <DataTable
        columns={[
          { key: "referenceNumber", label: "Reference" },
          { key: "riskLevel", label: "Risk Status", render: (value) => <RiskBadge risk={value} /> },
          { key: "riskScore", label: "Risk Score" },
          { key: "evaluatedAmount", label: "Amount", render: (value) => `INR ${value}` },
          { key: "reasons", label: "Detection Reason" },
          { key: "analyzedAt", label: "Analyzed At", render: (value) => new Date(value).toLocaleString() }
        ]}
        rows={fraudLogs}
      />
    </AppShell>
  );
}
