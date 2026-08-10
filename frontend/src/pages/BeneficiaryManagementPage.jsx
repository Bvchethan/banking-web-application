import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import DataTable from "../components/DataTable";
import FormInput from "../components/FormInput";
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
    setBeneficiaries(data || []);
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
    setForm({
      nickname: row.nickname || "",
      beneficiaryName: row.beneficiaryName || "",
      beneficiaryAccountNumber: row.beneficiaryAccountNumber || "",
      bankName: row.bankName || "",
      ifscCode: row.ifscCode || ""
    });
  };

  const handleDelete = async (id) => {
    await api.delete(`/customer/beneficiaries/${id}`);
    load();
  };

  return (
    <AppShell
      title="Beneficiary Management"
      subtitle="Maintain approved payee records for future customer transfers with standard validation details."
    >
      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
        <section className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">{editingId ? "Update Beneficiary" : "Add Beneficiary"}</div>
            </div>
            <form className="grid gap-5 px-4 py-4 md:grid-cols-2" onSubmit={handleSubmit}>
              <FormInput label="Nickname" value={form.nickname} onChange={(event) => setForm({ ...form, nickname: event.target.value })} />
              <FormInput
                label="Beneficiary Name"
                value={form.beneficiaryName}
                onChange={(event) => setForm({ ...form, beneficiaryName: event.target.value })}
              />
              <FormInput
                label="Account Number"
                value={form.beneficiaryAccountNumber}
                onChange={(event) => setForm({ ...form, beneficiaryAccountNumber: event.target.value })}
              />
              <FormInput label="Bank Name" value={form.bankName} onChange={(event) => setForm({ ...form, bankName: event.target.value })} />
              <FormInput label="IFSC Code" value={form.ifscCode} onChange={(event) => setForm({ ...form, ifscCode: event.target.value })} />

              <div className="flex flex-wrap gap-3 self-end">
                <button className="button-primary min-w-[160px]">{editingId ? "Save Changes" : "Add Beneficiary"}</button>
                {editingId ? (
                  <button
                    type="button"
                    className="button-secondary min-w-[160px]"
                    onClick={() => {
                      setEditingId(null);
                      setForm(initialForm);
                    }}
                  >
                    Cancel Edit
                  </button>
                ) : null}
              </div>
            </form>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Registered Beneficiaries</div>
            </div>
            <div className="p-4">
              <DataTable
                columns={[
                  { key: "nickname", label: "Nickname" },
                  { key: "beneficiaryName", label: "Beneficiary Name" },
                  { key: "beneficiaryAccountNumber", label: "Account Number" },
                  { key: "bankName", label: "Bank Name" },
                  { key: "ifscCode", label: "IFSC" },
                  {
                    key: "actions",
                    label: "Actions",
                    render: (_, row) => (
                      <div className="flex flex-wrap gap-2">
                        <button type="button" className="button-secondary !px-3 !py-1.5 !text-[12px]" onClick={() => handleEdit(row)}>
                          Edit
                        </button>
                        <button type="button" className="button-danger !px-3 !py-1.5 !text-[12px]" onClick={() => handleDelete(row.id)}>
                          Delete
                        </button>
                      </div>
                    )
                  }
                ]}
                rows={beneficiaries}
                emptyText="No beneficiaries are registered for this customer."
              />
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Validation Guidance</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <ul className="space-y-2">
                <li>- Confirm account number and IFSC before approving a new payee.</li>
                <li>- Use nicknames that help the customer identify the beneficiary clearly.</li>
                <li>- Edit or remove inactive payees to reduce transfer errors.</li>
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
