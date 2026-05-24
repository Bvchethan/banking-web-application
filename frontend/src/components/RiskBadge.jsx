export default function RiskBadge({ risk }) {
  const styles = {
    LOW: "bg-emerald-400/15 text-emerald-200",
    MEDIUM: "bg-amber-400/15 text-amber-200",
    HIGH: "bg-rose-400/15 text-rose-200"
  };

  return <span className={`rounded-full px-3 py-1 text-xs font-semibold ${styles[risk] || styles.LOW}`}>{risk}</span>;
}
