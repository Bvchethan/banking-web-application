export default function StatCard({ label, value, detail, accent = "sky" }) {
  const accentMap = {
    sky: "border-sky-200 bg-sky-50 text-sky-900",
    emerald: "border-emerald-200 bg-emerald-50 text-emerald-900",
    amber: "border-amber-200 bg-amber-50 text-amber-900",
    rose: "border-rose-200 bg-rose-50 text-rose-900"
  };

  return (
    <div className="app-panel">
      <div className={`border-l-4 px-4 py-4 ${accentMap[accent] || accentMap.sky}`}>
        <div className="text-[12px] font-semibold uppercase tracking-[0.05em] text-slate-600">{label}</div>
        <div className="mt-2 text-[24px] font-semibold leading-none text-slate-950">{value}</div>
        {detail ? <div className="mt-2 text-[12px] leading-5 text-slate-600">{detail}</div> : null}
      </div>
    </div>
  );
}
