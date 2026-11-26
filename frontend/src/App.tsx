import { AppShell } from "@/components/AppShell"

export function App() {
  return (
    <AppShell>
      <section className="max-w-[880px] border border-line bg-surface">
        <div className="border-b border-line px-6 py-5">
          <h1 className="text-[22px] font-medium tracking-tight text-ink">FishTrace</h1>
          <p className="mt-1 text-[14px] text-muted">
            Phishing threat intelligence and email forensics workspace.
          </p>
        </div>
        <div className="px-6 py-6">
          <p className="font-technical text-[12px] uppercase tracking-[0.14em] text-accent">
            Milestone 01 — Foundation
          </p>
          <p className="mt-3 max-w-[620px] text-[15px] leading-7 text-muted">
            The analysis engine, database schema and API foundation are in place. Investigation
            workflows become available as the forensic milestones are completed.
          </p>
        </div>
      </section>
    </AppShell>
  )
}
