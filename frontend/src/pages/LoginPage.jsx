import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import FormInput from "../components/FormInput";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

const demoUsers = [
  {
    role: "Retail Customer",
    userId: "CIF 11028491",
    credentials: "john@bank.com / Customer@123",
  },
  {
    role: "Bank Administrator",
    userId: "OPS 900104",
    credentials: "admin@bank.com / Admin@123",
  },
];

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
      setError(
        err.response?.data?.message || "Authentication could not be completed.",
      );
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b border-slate-800 bg-slate-950 text-white">
        <div className="mx-auto flex max-w-[1200px] items-center justify-between px-6 py-4">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-300">
              NovaBank
            </div>
            <div className="mt-1 text-[20px] font-semibold">Online Banking</div>
          </div>
          <div className="hidden text-[12px] text-slate-300 md:block">
            Retail and operations access portal
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1200px] gap-6 px-6 py-8 lg:grid-cols-[440px_minmax(0,1fr)]">
        <section className="app-panel self-start">
          <div className="border-b border-slate-200 px-6 py-5">
            <div className="section-label">Sign In</div>
            <h1 className="mt-2 text-[28px] font-semibold text-slate-950">
              {" "}
              Banking workspace
            </h1>
            <p className="mt-2 text-[14px] leading-6 text-slate-600">
              Use your registered email and password to view accounts,
              transactions, beneficiaries, and payment activity.
            </p>
          </div>

          <form className="px-6 py-6" onSubmit={handleSubmit}>
            <div className="space-y-5">
              <FormInput
                label="Email Address"
                type="email"
                autoComplete="username"
                value={form.email}
                onChange={(event) =>
                  setForm({ ...form, email: event.target.value })
                }
              />
              <FormInput
                label="Password"
                type="password"
                autoComplete="current-password"
                value={form.password}
                onChange={(event) =>
                  setForm({ ...form, password: event.target.value })
                }
              />
            </div>

            {error ? (
              <div className="mt-5 border border-rose-200 bg-rose-50 px-3 py-2 text-[13px] text-rose-700">
                {error}
              </div>
            ) : null}

            <div className="mt-6 flex flex-wrap gap-3">
              <button className="button-primary min-w-[148px]">Sign In</button>
              <Link to="/register" className="button-secondary min-w-[148px]">
                Open Account
              </Link>
            </div>
          </form>
        </section>
        <section className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-6 py-4">
              <div className="panel-title">Access Information</div>
            </div>

            <div className="px-6 py-6">
              <div className="grid items-center gap-8 md:grid-cols-2">
                {/* Left - Image */}
                <div className="flex justify-center">
                  <img
                    src="public\images\image.png"
                    alt="Customer Support"
                    className="h-54 w-full max-w-sm rounded-xl object-cover shadow-md"
                  />
                </div>

                {/* Right - Support Hours */}
                <div>
                  <div className="section-label">Support hours</div>
                  <p className="mt-2 text-[14px] leading-6 text-slate-700">
                    Retail banking support available Monday to Saturday,
                    <br />
                    <span className="font-semibold">8:00 AM – 8:00 PM IST</span>
                    .
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="app-panel overflow-hidden">
            <div className="border-b border-slate-200 px-6 py-4">
              <div className="panel-title">Demo Access for Review</div>
            </div>
            <table className="min-w-full text-left text-[13px]">
              <thead className="bg-slate-100 text-slate-700">
                <tr>
                  <th className="border-b border-slate-200 px-6 py-3 font-semibold">
                    User Type
                  </th>
                  <th className="border-b border-slate-200 px-6 py-3 font-semibold">
                    Reference
                  </th>
                  <th className="border-b border-slate-200 px-6 py-3 font-semibold">
                    Credentials
                  </th>
                </tr>
              </thead>
              <tbody>
                {demoUsers.map((user) => (
                  <tr key={user.role} className="even:bg-slate-50/60">
                    <td className="border-b border-slate-200 px-6 py-3 font-medium text-slate-900">
                      {user.role}
                    </td>
                    <td className="border-b border-slate-200 px-6 py-3 text-slate-700">
                      {user.userId}
                    </td>
                    <td className="border-b border-slate-200 px-6 py-3 text-slate-700">
                      {user.credentials}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
