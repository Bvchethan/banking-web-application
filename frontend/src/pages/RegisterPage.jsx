import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import FormInput from "../components/FormInput";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

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
      setError(err.response?.data?.message || "Registration could not be completed.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b border-slate-800 bg-slate-950 text-white">
        <div className="mx-auto flex max-w-[1200px] items-center justify-between px-6 py-4">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-300">NovaBank</div>
            <div className="mt-1 text-[20px] font-semibold">Retail Customer Onboarding</div>
          </div>
          <Link to="/login" className="button-secondary !border-slate-600 !bg-slate-950 !px-3 !py-2 !text-white hover:!bg-slate-900">
            Back to Sign In
          </Link>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1200px] gap-6 px-6 py-8 lg:grid-cols-[minmax(0,1fr)_320px]">
        <section className="app-panel">
          <div className="border-b border-slate-200 px-6 py-5">
            <div className="section-label">Customer Registration</div>
            <h1 className="mt-2 text-[28px] font-semibold text-slate-950">Open a digital banking profile</h1>
            <p className="mt-2 text-[14px] leading-6 text-slate-600">
              Capture the customer identity and contact details required to provision an online banking account.
            </p>
          </div>

          <form className="px-6 py-6" onSubmit={handleSubmit}>
            <div className="grid gap-5 md:grid-cols-2">
              <FormInput label="Full Name" value={form.fullName} onChange={(event) => setForm({ ...form, fullName: event.target.value })} />
              <FormInput label="Email Address" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
              <FormInput label="Mobile Number" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
              <FormInput
                label="Password"
                type="password"
                hint="Use a strong password with upper case, lower case, number, and special character."
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
              />
              <FormInput
                label="Registered Address"
                as="textarea"
                className="md:col-span-2"
                value={form.address}
                onChange={(event) => setForm({ ...form, address: event.target.value })}
              />
            </div>

            {error ? (
              <div className="mt-5 border border-rose-200 bg-rose-50 px-3 py-2 text-[13px] text-rose-700">{error}</div>
            ) : null}

            <div className="mt-6 flex flex-wrap gap-3">
              <button className="button-primary min-w-[148px]">Create Profile</button>
              <Link to="/login" className="button-secondary min-w-[148px]">
                Cancel
              </Link>
            </div>
          </form>
        </section>

        <aside className="space-y-6">
          <div className="app-panel">
            <div className="border-b border-slate-200 px-5 py-4">
              <div className="panel-title">Registration Checklist</div>
            </div>
            <div className="px-5 py-5 text-[13px] leading-6 text-slate-700">
              <div className="mb-3 font-medium text-slate-900">Before submitting:</div>
              <ul className="space-y-2">
                <li>- Enter a valid email address for sign-in notifications.</li>
                <li>- Use the active mobile number linked to the customer profile.</li>
                <li>- Keep the registered address aligned with KYC records.</li>
                <li>- Review password strength before continuing.</li>
              </ul>
            </div>
          </div>

          <div className="app-panel">
            <div className="border-b border-slate-200 px-5 py-4">
              <div className="panel-title">Provisioning Outcome</div>
            </div>
            <div className="px-5 py-5 text-[13px] leading-6 text-slate-700">
              Successful registration creates a customer login, assigns the retail user role, and provisions a linked account record for dashboard access.
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
