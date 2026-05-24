import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import FormInput from "../components/FormInput";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    phone: "",
    password: "",
    address: ""
  });
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      const { data } = await api.post("/auth/register", form);
      login(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="glass w-full max-w-3xl rounded-[2rem] p-10 shadow-glow">
        <p className="text-sm uppercase tracking-[0.35em] text-orange-300">Open Your Account</p>
        <h1 className="mt-4 text-4xl font-semibold text-white">Start your digital banking journey.</h1>

        <form className="mt-8 grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
          <FormInput label="Full Name" value={form.fullName} onChange={(e) => setForm({ ...form, fullName: e.target.value })} />
          <FormInput label="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <FormInput label="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <FormInput label="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          <FormInput
            label="Address"
            className="md:col-span-2"
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
          />

          {error ? <p className="md:col-span-2 text-sm text-rose-300">{error}</p> : null}

          <button className="rounded-2xl bg-orange-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-orange-300">
            Register
          </button>
          <Link
            to="/login"
            className="rounded-2xl border border-white/10 px-4 py-3 text-center font-semibold text-white transition hover:bg-white/10"
          >
            Back to Login
          </Link>
        </form>
      </div>
    </div>
  );
}
