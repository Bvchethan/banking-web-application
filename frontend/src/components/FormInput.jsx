export default function FormInput({
  label,
  error,
  hint,
  className = "",
  as = "input",
  options = [],
  ...props
}) {
  const controlClassName = "form-control";

  return (
    <label className={`block ${className}`}>
      <span className="mb-2 block text-[12px] font-semibold uppercase tracking-[0.05em] text-slate-600">{label}</span>

      {as === "textarea" ? (
        <textarea {...props} className={`${controlClassName} min-h-[96px] resize-y`} />
      ) : as === "select" ? (
        <select {...props} className={controlClassName}>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : (
        <input {...props} className={controlClassName} />
      )}

      {hint ? <span className="mt-2 block text-[12px] text-slate-500">{hint}</span> : null}
      {error ? <span className="mt-2 block text-[12px] text-rose-700">{error}</span> : null}
    </label>
  );
}
