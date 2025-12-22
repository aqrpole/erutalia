"use client"

import { X } from "lucide-react"
import { useState } from "react"
import { siteConfig } from "@/config/site"

export function ConstructionBanner() {
  const [visible, setVisible] = useState(true)

  if (!visible) return null

  return (
    <div
      className="fixed top-0 left-0 right-0 z-50 px-4 py-3 text-center text-foreground shadow-md"
      style={{ backgroundColor: siteConfig.features.underConstructionBannerColor }}
    >
      <div className="container mx-auto flex items-center justify-center gap-4">
        <span className="font-medium">🚧 Website Under Construction 🚧</span>
        <button
          onClick={() => setVisible(false)}
          className="ml-auto p-1 hover:opacity-70 transition-opacity"
          aria-label="Close banner"
        >
          <X className="h-5 w-5" />
        </button>
      </div>
    </div>
  )
}
