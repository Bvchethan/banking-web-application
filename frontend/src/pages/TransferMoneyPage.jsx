import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import FormInput from "../components/FormInput";
import api from "../services/api";

export default function TransferMoneyPage() {
  const [beneficiaries, setBeneficiaries] = useState([]);
  const [form, setForm] = useState({ beneficiaryId: "", amount: "", description: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/customer/beneficiaries").then(({ data }) => setBeneficiaries(data));
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      setMessage("");
      const payload = { ...form, beneficiaryId: Number(form.beneficiaryId), amount: Number(form.amount) };
      const { data } = await api.post("/customer/transfer", payload);
      setMessage(`Transfer completed successfully. Reference: ${data.referenceNumber}`);
      setForm({ beneficiaryId: "", amount: "", description: "" });
    } catch (err) {
      setError(err.response?.data?.message || "Transfer failed");
    }
  };

  return (
    <AppShell title="Transfer Money" subtitle="Send funds securely with beneficiary validation and fraud analysis.">
      <form onSubmit={handleSubmit} className="grid gap-5 md:grid-cols-2">
        <label className="block">
          <span className="mb-2 block text-sm text-slate-300">Select Beneficiary</span>
          <select
            value={form.beneficiaryId}
            onChange={(e) => setForm({ ...form, beneficiaryId: e.target.value })}
            className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none"
          >
            <option value="">Choose beneficiary</option>
            {beneficiaries.map((beneficiary) => (
              <option key={beneficiary.id} value={beneficiary.id}>
                {beneficiary.nickname} - {beneficiary.beneficiaryAccountNumber}
              </option>
            ))}
          </select>
        </label>
        <FormInput label="Amount" type="number" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} />
        <FormInput
          label="Transfer Description"
          className="md:col-span-2"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />

        {message ? <p className="md:col-span-2 text-sm text-emerald-300">{message}</p> : null}
        {error ? <p className="md:col-span-2 text-sm text-rose-300">{error}</p> : null}

        <button className="rounded-2xl bg-teal-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-teal-300">
          Transfer Funds
        </button>
      </form>
    </AppShell>
  );
}
