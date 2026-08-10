import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import FormInput from "../components/FormInput";
import api from "../services/api";

export default function ProfilePage() {
  const [form, setForm] = useState({ fullName: "", phone: "", address: "", email: "" });
  const [message, setMessage] = useState("");

  useEffect(() => {
    api.get("/customer/profile").then(({ data }) => setForm(data));
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const { data } = await api.put("/customer/profile", {
      fullName: form.fullName,
      phone: form.phone,
      address: form.address
    });
    setForm(data);
    setMessage("Customer contact details updated successfully.");
  };

  return (
    <AppShell
      title="Profile & Contact"
      subtitle="Review the registered customer identity details used for account communication and servicing."
    >
      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
        <section className="app-panel">
          <div className="border-b border-slate-200 px-4 py-3">
            <div className="panel-title">Customer Profile</div>
          </div>
          <form className="grid gap-5 px-4 py-4 md:grid-cols-2" onSubmit={handleSubmit}>
            <FormInput label="Customer Name" value={form.fullName} onChange={(event) => setForm({ ...form, fullName: event.target.value })} />
            <FormInput label="Email Address" value={form.email} disabled />
            <FormInput label="Mobile Number" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
            <FormInput
              label="Registered Address"
              as="textarea"
              value={form.address}
              onChange={(event) => setForm({ ...form, address: event.target.value })}
            />

            {message ? <div className="md:col-span-2 border border-emerald-200 bg-emerald-50 px-3 py-2 text-[13px] text-emerald-700">{message}</div> : null}

            <div className="md:col-span-2">
              <button className="button-primary min-w-[160px]">Update Profile</button>
            </div>
          </form>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-4 py-3">
              <div className="panel-title">Customer Record Notes</div>
            </div>
            <div className="px-4 py-4 text-[13px] leading-6 text-slate-700">
              <ul className="space-y-2">
                <li>- Email address remains the primary online banking login identifier.</li>
                <li>- Contact changes should match the latest KYC and communication records.</li>
                <li>- Update phone number promptly to maintain OTP and alert delivery.</li>
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}
