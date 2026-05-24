import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const customerLinks = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/transfer", label: "Transfer" },
  { to: "/beneficiaries", label: "Beneficiaries" },
  { to: "/transactions", label: "Transactions" },
  { to: "/fraud-analytics", label: "Fraud Analytics" },
  { to: "/financial-insights", label: "Financial Insights" },
  { to: "/profile", label: "Profile" }
];

const adminLinks = [
  { to: "/admin", label: "Admin Dashboard" },
  ...customerLinks
];

export default function AppShell({ title, subtitle, children }) {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();
  const links = auth?.roles?.includes("ROLE_ADMIN") ? adminLinks : customerLinks;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen grid-surface">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 lg:flex-row lg:gap-6">
        <aside className="glass mb-6 rounded-3xl p-6 shadow-glow lg:mb-0 lg:w-80">
          <Link to="/dashboard" className="mb-8 block">
            <p className="text-sm uppercase tracking-[0.35em] text-teal-300">NovaBank</p>
            <h1 className="mt-2 text-3xl font-semibold text-white">Digital Banking</h1>
          </Link>

          <div className="mb-8 rounded-2xl bg-teal-400/10 p-4">
            <p className="text-sm text-slate-300">Signed in as</p>
            <p className="mt-1 text-lg font-semibold text-white">{auth?.fullName}</p>
            <p className="text-sm text-slate-400">{auth?.email}</p>
          </div>

          <nav className="space-y-2">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `block rounded-2xl px-4 py-3 text-sm transition ${
                    isActive ? "bg-white text-slate-900" : "text-slate-300 hover:bg-white/10 hover:text-white"
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>

          <button
            type="button"
            onClick={handleLogout}
            className="mt-8 w-full rounded-2xl border border-white/10 px-4 py-3 text-sm text-white transition hover:bg-white/10"
          >
            Logout
          </button>
        </aside>

        <main className="flex-1">
          <section className="glass rounded-3xl p-6 shadow-glow">
            <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-orange-300">Secure Banking</p>
                <h2 className="mt-2 text-3xl font-semibold text-white">{title}</h2>
                <p className="mt-2 max-w-3xl text-slate-400">{subtitle}</p>
              </div>
            </div>
            {children}
          </section>
        </main>
      </div>
    </div>
  );
}
