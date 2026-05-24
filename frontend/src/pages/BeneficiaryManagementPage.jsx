import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import FormInput from "../components/FormInput";
import DataTable from "../components/DataTable";
import api from "../services/api";

const initialForm = {
  nickname: "",
  beneficiaryName: "",
  beneficiaryAccountNumber: "",
  bankName: "",
  ifscCode: ""
};

export default function BeneficiaryManagementPage() {
  const [beneficiaries, setBeneficiaries] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    const { data } = await api.get("/customer/beneficiaries");
    setBeneficiaries(data);
  };

  useEffect(() => {
    load();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (editingId) {
      await api.put(`/customer/beneficiaries/${editingId}`, form);
    } else {
      await api.post("/customer/beneficiaries", form);
    }
    setForm(initialForm);
    setEditingId(null);
    load();
  };

  const handleEdit = (row) => {
    setEditingId(row.id);
    setForm(row);
  };

  const handleDelete = async (id) => {
    await api.delete(`/customer/beneficiaries/${id}`);
    load();
  };

  return (
    <AppShell title="Beneficiary Management" subtitle="Manage trusted payees with clean validation and edit controls.">
      <form className="grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
        <FormInput label="Nickname" value={form.nickname} onChange={(e) => setForm({ ...form, nickname: e.target.value })} />
        <FormInput label="Beneficiary Name" value={form.beneficiaryName} onChange={(e) => setForm({ ...form, beneficiaryName: e.target.value })} />
        <FormInput
          label="Account Number"
          value={form.beneficiaryAccountNumber}
          onChange={(e) => setForm({ ...form, beneficiaryAccountNumber: e.target.value })}
        />
        <FormInput label="Bank Name" value={form.bankName} onChange={(e) => setForm({ ...form, bankName: e.target.value })} />
        <FormInput label="IFSC Code" value={form.ifscCode} onChange={(e) => setForm({ ...form, ifscCode: e.target.value })} />
        <button className="rounded-2xl bg-orange-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-orange-300">
          {editingId ? "Update Beneficiary" : "Add Beneficiary"}
        </button>
      </form>

      <div className="mt-8">
        <DataTable
          columns={[
            { key: "nickname", label: "Nickname" },
            { key: "beneficiaryName", label: "Name" },
            { key: "beneficiaryAccountNumber", label: "Account" },
            { key: "bankName", label: "Bank" },
            { key: "ifscCode", label: "IFSC" },
            {
              key: "actions",
              label: "Actions",
              render: (_, row) => (
                <div className="flex gap-2">
                  <button type="button" className="rounded-full bg-white/10 px-3 py-1" onClick={() => handleEdit(row)}>
                    Edit
                  </button>
                  <button
                    type="button"
                    className="rounded-full bg-rose-400/20 px-3 py-1 text-rose-200"
                    onClick={() => handleDelete(row.id)}
                  >
                    Delete
                  </button>
                </div>
              )
            }
          ]}
          rows={beneficiaries}
        />
      </div>
    </AppShell>
  );
}
