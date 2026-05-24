export default function StatCard({ label, value, accent = "teal" }) {
  const accentMap = {
    teal: "from-teal-400/20 to-teal-400/5 text-teal-200",
    orange: "from-orange-400/20 to-orange-400/5 text-orange-200",
    blue: "from-sky-400/20 to-sky-400/5 text-sky-200",
    rose: "from-rose-400/20 to-rose-400/5 text-rose-200"
  };

  return (
    <div className={`rounded-3xl border border-white/10 bg-gradient-to-br p-5 ${accentMap[accent]}`}>
      <p className="text-sm text-slate-300">{label}</p>
      <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
    </div>
  );
}
