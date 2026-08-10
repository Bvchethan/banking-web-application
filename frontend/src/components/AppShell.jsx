import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const customerLinks = [
  { to: "/dashboard", label: "Account Overview" },
  { to: "/transfer", label: "Payments & Transfers" },
  { to: "/beneficiaries", label: "Beneficiaries" },
  { to: "/transactions", label: "Transaction History" },
  { to: "/fraud-analytics", label: "Fraud Review" },
  { to: "/financial-insights", label: "Financial Insights" },
  { to: "/profile", label: "Profile & Contact" }
];

const adminLinks = [{ to: "/admin", label: "Operations Dashboard" }, ...customerLinks];

export default function AppShell({ title, subtitle, children, actions = null }) {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();
  const isAdmin = auth?.roles?.includes("ROLE_ADMIN");
  const links = isAdmin ? adminLinks : customerLinks;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b border-slate-800 bg-slate-950 text-white">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-6 py-4">
          <div className="flex items-center gap-6">
            <Link to={isAdmin ? "/admin" : "/dashboard"} className="block">
              <div className="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-300">NovaBank</div>
              <div className="mt-1 text-[20px] font-semibold leading-none">Digital Banking</div>
            </Link>
            <div className="hidden border-l border-slate-700 pl-6 text-[12px] text-slate-300 lg:block">
              Secure retail banking workspace
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden text-right sm:block">
              <div className="text-[13px] font-semibold">{auth?.fullName || "Authenticated User"}</div>
              <div className="mt-1 text-[11px] uppercase tracking-[0.06em] text-slate-400">
                {isAdmin ? "Administrator Session" : "Customer Session"}
              </div>
            </div>
            <button type="button" onClick={handleLogout} className="button-secondary !border-slate-600 !bg-slate-950 !px-3 !py-2 !text-white hover:!bg-slate-900">
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1440px] gap-6 px-6 py-6 lg:grid-cols-[248px_minmax(0,1fr)]">
        <aside className="app-panel self-start">
          <div className="border-b border-slate-200 px-4 py-4">
            <div className="section-label">Primary Navigation</div>
            <div className="mt-2 text-[15px] font-semibold text-slate-900">{isAdmin ? "Operations Menu" : "Customer Services"}</div>
          </div>

          <nav className="px-2 py-2">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `mb-1 block border-l-4 px-3 py-2 text-[13px] font-medium ${
                    isActive
                      ? "border-sky-800 bg-sky-50 text-sky-900"
                      : "border-transparent text-slate-700 hover:bg-slate-50 hover:text-slate-900"
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>

          <div className="border-t border-slate-200 px-4 py-4 text-[12px] text-slate-600">
            <div className="font-semibold text-slate-800">Online Banking Support</div>
            <div className="mt-2">Retail care: 1800-266-1001</div>
            <div className="mt-1">Fraud reporting: 1800-266-9191</div>
          </div>
        </aside>

        <main className="min-w-0">
          <section className="app-panel">
            <div className="border-b border-slate-200 px-6 py-5">
              <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
                <div>
                  <div className="section-label">Digital Banking</div>
                  <h1 className="mt-2 text-[28px] font-semibold leading-tight text-slate-950">{title}</h1>
                  {subtitle ? <p className="mt-2 max-w-4xl text-[14px] leading-6 text-slate-600">{subtitle}</p> : null}
                </div>
                <div className="flex flex-wrap items-center gap-3 text-[12px] text-slate-500">
                  <span className="status-chip border-emerald-200 bg-emerald-50 text-emerald-700">Secure Session Active</span>
                  {actions}
                </div>
              </div>
            </div>

            <div className="px-6 py-6">{children}</div>
          </section>
        </main>
      </div>
    </div>
  );
}
