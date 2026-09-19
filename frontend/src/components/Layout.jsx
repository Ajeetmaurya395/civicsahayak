import { Outlet, Link, useLocation } from 'react-router-dom'
import { MessageSquare, Search, User, Bookmark, Home, Shield } from 'lucide-react'

const navItems = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/chat', label: 'Find Schemes', icon: MessageSquare },
  { path: '/results', label: 'Results', icon: Search },
  { path: '/profile', label: 'Profile', icon: User },
  { path: '/saved', label: 'Saved', icon: Bookmark },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-surface-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-surface-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2.5 no-underline">
              <div className="w-9 h-9 bg-primary-700 rounded-xl flex items-center justify-center shadow-sm">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div>
                <span className="text-lg font-bold text-surface-900 tracking-tight">
                  CivicOS
                </span>
                <span className="hidden sm:inline text-xs text-surface-500 ml-2 font-medium">
                  Government Scheme Discovery
                </span>
              </div>
            </Link>

            <nav className="hidden md:flex items-center gap-1">
              {navItems.map(({ path, label, icon: Icon }) => {
                const isActive = location.pathname === path
                return (
                  <Link
                    key={path}
                    to={path}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium no-underline transition-all duration-200 ${
                      isActive
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-surface-600 hover:bg-surface-100 hover:text-surface-900'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {label}
                  </Link>
                )
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Mobile bottom nav */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-surface-200 z-50">
        <div className="flex items-center justify-around py-2">
          {navItems.map(({ path, label, icon: Icon }) => {
            const isActive = location.pathname === path
            return (
              <Link
                key={path}
                to={path}
                className={`flex flex-col items-center gap-1 px-3 py-1.5 rounded-lg no-underline transition-colors ${
                  isActive
                    ? 'text-primary-700'
                    : 'text-surface-400 hover:text-surface-600'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="text-[10px] font-medium">{label}</span>
              </Link>
            )
          })}
        </div>
      </nav>

      {/* Footer spacer for mobile nav */}
      <div className="md:hidden h-16" />
    </div>
  )
}
