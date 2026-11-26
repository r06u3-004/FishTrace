import type { ReactNode } from "react"

import {
  Activity,
  FileSearch,
  FileText,
  Fingerprint,
  FolderSearch,
  Mail,
  Settings2,
  ShieldAlert,
} from "lucide-react"

const sections = [
  { number: "01", label: "Overview", icon: Activity },
  { number: "02", label: "Campaigns", icon: ShieldAlert },
  { number: "03", label: "Investigations", icon: FolderSearch },
  { number: "04", label: "IOC Intelligence", icon: Fingerprint },
  { number: "05", label: "Email", icon: Mail },
  { number: "06", label: "Forensics", icon: FileSearch },
  { number: "07", label: "Reports", icon: FileText },
]

interface AppShellProps {
  children: ReactNode
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="flex min-h-screen">
      <aside className="flex w-[248px] shrink-0 flex-col border-r border-line bg-surface">
        <div className="flex h-[72px] items-center gap-3 border-b border-line px-5">
          <span className="font-technical text-[15px] font-medium tracking-tight text-ink">
            Fish<span className="text-accent">Trace</span>
          </span>
          <span className="font-technical text-[11px] text-muted">v0.1</span>
        </div>
        <nav className="flex-1 py-4" aria-label="Primary navigation">
          <ul className="space-y-0.5">
            {sections.map((section, index) => {
              const Icon = section.icon
              const current = index === 0
              return (
                <li key={section.label}>
                  <div
                    aria-current={current ? "page" : undefined}
                    className={`flex items-center gap-3 border-l-2 px-5 py-2.5 text-[14px] ${
                      current
                        ? "border-accent bg-elevated text-ink"
                        : "border-transparent text-muted hover:bg-elevated hover:text-ink"
                    }`}
                  >
                    <Icon size={17} strokeWidth={1.7} aria-hidden="true" />
                    <span className="w-6 font-technical text-[11px] text-muted">{section.number}</span>
                    <span>{section.label}</span>
                  </div>
                </li>
              )
            })}
          </ul>
        </nav>
        <div className="border-t border-line px-5 py-4">
          <div className="flex items-center gap-3 text-[14px] text-muted">
            <Settings2 size={17} strokeWidth={1.7} aria-hidden="true" />
            <span>Settings</span>
          </div>
          <p className="mt-2 font-technical text-[11px] text-muted">
            © 2026 R06U3. Tous droits réservés.
          </p>
        </div>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-[72px] items-center justify-between border-b border-line px-8">
          <span className="text-[14px] text-muted">Investigation workspace</span>
          <span className="font-technical text-[12px] text-muted">ENGINE v0.1.0</span>
        </header>
        <main className="flex-1 px-8 py-8">{children}</main>
      </div>
    </div>
  )
}
