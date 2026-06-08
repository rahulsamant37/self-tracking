import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Dashboard', icon: '📊', end: true },
  { to: '/today', label: "Today's Tasks", icon: '✅' },
  { to: '/dsa', label: 'DSA (TLE)', icon: '💻' },
  { to: '/goals', label: 'Goals', icon: '🎯' },
]

export function Layout() {
  return (
    <div className="min-h-screen md:flex">
      <aside className="border-b border-slate-200 bg-white md:w-64 md:border-b-0 md:border-r">
        <div className="flex items-center gap-2 px-6 py-5">
          <span className="text-2xl">🚀</span>
          <div>
            <h1 className="text-base font-bold leading-tight">Goal Progress</h1>
            <p className="text-xs text-slate-500">Tracker</p>
          </div>
        </div>
        <nav className="flex gap-1 overflow-x-auto px-3 pb-3 md:flex-col md:gap-1 md:pb-0">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `flex items-center gap-3 whitespace-nowrap rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`
              }
            >
              <span>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="flex-1 px-4 py-6 md:px-10 md:py-8">
        <div className="mx-auto max-w-5xl">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
