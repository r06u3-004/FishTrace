import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import { AppShell } from "@/components/AppShell"

describe("AppShell", () => {
  it("renders the primary investigation sections", () => {
    render(
      <AppShell>
        <div>workspace</div>
      </AppShell>,
    )

    expect(screen.getByRole("navigation", { name: "Primary navigation" })).toBeInTheDocument()
    expect(screen.getByText("Investigations")).toBeInTheDocument()
    expect(screen.getByText("IOC Intelligence")).toBeInTheDocument()
    expect(screen.getByText("Reports")).toBeInTheDocument()
    expect(screen.getByText("workspace")).toBeInTheDocument()
  })
})
