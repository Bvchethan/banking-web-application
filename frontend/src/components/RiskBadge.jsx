export default function RiskBadge({ risk }) {
  const styles = {
    LOW: "border-emerald-200 bg-emerald-50 text-emerald-700",
    MEDIUM: "border-amber-200 bg-amber-50 text-amber-700",
    HIGH: "border-rose-200 bg-rose-50 text-rose-700"
  };

  return <span className={`status-chip ${styles[risk] || styles.LOW}`}>{risk || "LOW"}</span>;
}
