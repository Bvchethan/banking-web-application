import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import FormInput from "../components/FormInput";
import api from "../services/api";
import { formatCurrency, maskAccountNumber } from "../utils/formatters";

export default function TransferMoneyPage() {
  const [beneficiaries, setBeneficiaries] = useState([]);
  const [account, setAccount] = useState(null);
  const [form, setForm] = useState({ beneficiaryId: "", amount: "", description: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      const [beneficiaryRes, accountRes] = await Promise.all([api.get("/customer/beneficiaries"), api.get("/customer/account")]);
      setBeneficiaries(beneficiaryRes.data || []);
      setAccount(accountRes.data);
    };

    load();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setError("");
      setMessage("");
      const payload = {
        ...form,
        beneficiaryId: Number(form.beneficiaryId),
        amount: Number(form.amount)
      };
      const { data } = await api.post("/customer/transfer", payload);
      setMessage(`Transfer submitted successfully. Reference number: ${data.referenceNumber}`);
      setForm({ beneficiaryId: "", amount: "", description: "" });
    } catch (err) {
      setError(err.response?.data?.message || "Transfer request could not be processed.");
    }
  };

  const selectedBeneficiary = beneficiaries.find((item) => String(item.id) === String(form.beneficiaryId));

  return (
    <AppShell
      title="Payments & Transfers"
      subtitle="Initiate controlled customer transfers using pre-validated beneficiaries and monitored transaction checks."
    >
      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_340px]">
        <section className="app-panel">
          <div className="border-b border-slate-200 px-4 py-3">
            <div className="panel-title">New Transfer Instruction</div>
          </div>

          <form className="px-4 py-4" onSubmit={handleSubmit}>
            <div className="grid gap-5 md:grid-cols-2">
              <FormInput
                label="Debit Account"
                value={`${maskAccountNumber(account?.accountNumber)}  |  ${formatCurrency(account?.balance)}`}
                disabled
              />
              <FormInput
                label="Select Beneficiary"
                as="select"
                value={form.beneficiaryId}
                onChange={(event) => setForm({ ...form, beneficiaryId: event.target.value })}
                options={[
                  { value: "", label: "Choose a beneficiary" },
                  ...beneficiaries.map((beneficiary) => ({
                    value: beneficiary.id,
                    label: `${beneficiary.nickname} - ${beneficiary.beneficiaryAccountNumber}`
                  }))
                ]}
              />
              <FormInput
                label="Transfer Amount"
                type="number"
                min="1"
                step="0.01"
                value={form.amount}
                onChange={(event) => setForm({ ...form, amount: event.target.value })}
              />
              <FormInput
                label="Transfer Purpose"
                value={form.description}
                onChange={(event) => setForm({ ...form, description: event.target.value })}
                hint="Example: Rent payment, family support, vendor settlement"
              />
            </div>

            {message ? <div className="mt-5 border border-emerald-200 bg-emerald-50 px-3 py-2 text-[13px] text-emerald-700">{message}</div> : null}
            {error ? <div className="mt-5 border border-rose-200 bg-rose-50 px-3 py-2 text-[13px] text-rose-700">{error}</div> : null}

            <div className="mt-6 flex flex-wrap gap-3">
              <button className="button-primary min-w-[160px]">Submit Transfer</button>
              <button
                type="button"
                className="button-secondary min-w-[160px]"
                onClick={() => {
                  setForm({ beneficiaryId: "", amount: "", description: "" });
                  setError("");
                  setMessage("");
                }}
              >
                Reset Form
              </button>
            </div>
          </form>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Transfer Summary</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <div className="mb-2 flex items-center justify-between">
                <span>Available balance</span>
                <span className="font-semibold text-slate-900">{formatCurrency(account?.balance)}</span>
              </div>
              <div className="mb-2 flex items-center justify-between">
                <span>Beneficiary selected</span>
                <span className="font-semibold text-slate-900">{selectedBeneficiary?.nickname || "--"}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Transfer amount</span>
                <span className="font-semibold text-slate-900">{formatCurrency(form.amount || 0)}</span>
              </div>
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Control Checks</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <ul className="space-y-2">
                <li>- Transfers are allowed only to saved beneficiaries.</li>
                <li>- Fraud scoring evaluates amount, velocity, and beneficiary history before completion.</li>
                <li>- Both sender and receiver transaction entries are recorded for audit visibility.</li>
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
