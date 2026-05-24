import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import FormInput from "../components/FormInput";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      const { data } = await api.post("/auth/login", form);
      login(data);
      navigate(data.roles.includes("ROLE_ADMIN") ? "/admin" : "/dashboard");
    } catch (err) {
      setError(err.response?.data?.message || "Login failed");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="glass w-full max-w-5xl overflow-hidden rounded-[2rem] shadow-glow">
        <div className="grid md:grid-cols-2">
          <section className="grid-surface p-10">
            <p className="text-sm uppercase tracking-[0.35em] text-teal-300">NovaBank</p>
            <h1 className="mt-4 text-5xl font-semibold text-white">Banking built for trust, speed, and insight.</h1>
            <p className="mt-6 text-slate-300">
              Secure transfers, fraud intelligence, and financial wellness in one modern banking workspace.
            </p>
            <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-6">
              <p className="text-sm text-slate-300">Demo accounts</p>
              <p className="mt-3 text-white">Admin: admin@bank.com / Admin@123</p>
              <p className="mt-2 text-white">Customer: john@bank.com / Customer@123</p>
            </div>
          </section>

          <section className="p-10">
            <h2 className="text-3xl font-semibold text-white">Welcome back</h2>
            <p className="mt-2 text-slate-400">Sign in to access your banking dashboard.</p>

            <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
              <FormInput
                label="Email"
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
              <FormInput
                label="Password"
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />

              {error ? <p className="text-sm text-rose-300">{error}</p> : null}

              <button className="w-full rounded-2xl bg-teal-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-teal-300">
                Sign In
              </button>
            </form>

            <p className="mt-6 text-sm text-slate-400">
              New customer?{" "}
              <Link to="/register" className="text-teal-300 hover:text-teal-200">
                Create an account
              </Link>
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
