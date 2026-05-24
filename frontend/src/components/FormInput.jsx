export default function FormInput({ label, error, className = "", ...props }) {
  return (
    <label className={`block ${className}`}>
      <span className="mb-2 block text-sm text-slate-300">{label}</span>
      <input
        {...props}
        className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none transition focus:border-teal-400"
      />
      {error ? <span className="mt-2 block text-sm text-rose-300">{error}</span> : null}
    </label>
  );
}
