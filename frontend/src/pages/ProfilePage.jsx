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
    setMessage("Profile updated successfully.");
  };

  return (
    <AppShell title="Profile Page" subtitle="Maintain your account identity details with secure update controls.">
      <form className="grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
        <FormInput label="Full Name" value={form.fullName} onChange={(e) => setForm({ ...form, fullName: e.target.value })} />
        <FormInput label="Email" value={form.email} disabled />
        <FormInput label="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        <FormInput label="Address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
        {message ? <p className="md:col-span-2 text-sm text-emerald-300">{message}</p> : null}
        <button className="rounded-2xl bg-teal-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-teal-300">
          Save Profile
        </button>
      </form>
    </AppShell>
  );
}
