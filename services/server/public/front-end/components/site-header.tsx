"use client"

import Link from "next/link"
import { useState } from "react"
import { Menu, X } from "lucide-react"
import { siteConfig } from "@/config/site"
import { translations } from "@/lib/i18n"
import { Button } from "@/components/ui/button"

export function SiteHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [lang, setLang] = useState<"en" | "it">("en")
  const t = translations[lang]

  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/50 bg-background/80 backdrop-blur-md">
      <div className="container mx-auto flex h-20 items-center justify-between px-4">
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-xl md:text-2xl font-normal tracking-tight">{siteConfig.name}</span>
        </Link>

        <nav className="hidden md:flex items-center gap-8">
          <Link
            href="/#about"
            className="text-sm font-light tracking-wide hover:text-foreground transition-colors text-muted-foreground"
          >
            {t.nav.about}
          </Link>
          <Link
            href="/#services"
            className="text-sm font-light tracking-wide hover:text-foreground transition-colors text-muted-foreground"
          >
            {t.nav.services}
          </Link>
          <Link
            href="/blog"
            className="text-sm font-light tracking-wide hover:text-foreground transition-colors text-muted-foreground"
          >
            {t.nav.blog}
          </Link>
          <Link
            href="/#contact"
            className="text-sm font-light tracking-wide hover:text-foreground transition-colors text-muted-foreground"
          >
            {t.nav.contact}
          </Link>
          <Link href="/login">
            <Button variant="outline" size="sm" className="rounded-sm font-normal bg-transparent">
              {t.nav.login}
            </Button>
          </Link>
          <select
            value={lang}
            onChange={(e) => setLang(e.target.value as "en" | "it")}
            className="text-sm border border-border/50 rounded-sm px-3 py-1.5 bg-background font-light"
          >
            <option value="en">EN</option>
            <option value="it">IT</option>
          </select>
        </nav>

        <button className="md:hidden p-2" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} aria-label="Toggle menu">
          {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden border-t border-border/50 bg-background/95 backdrop-blur-md">
          <nav className="container mx-auto flex flex-col gap-4 p-4">
            <Link
              href="/#about"
              className="text-sm font-light hover:text-foreground transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.about}
            </Link>
            <Link
              href="/#services"
              className="text-sm font-light hover:text-foreground transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.services}
            </Link>
            <Link
              href="/blog"
              className="text-sm font-light hover:text-foreground transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.blog}
            </Link>
            <Link
              href="/#contact"
              className="text-sm font-light hover:text-foreground transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.contact}
            </Link>
            <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="outline" size="sm" className="w-full rounded-sm bg-transparent">
                {t.nav.login}
              </Button>
            </Link>
            <select
              value={lang}
              onChange={(e) => setLang(e.target.value as "en" | "it")}
              className="text-sm border border-border/50 rounded-sm px-3 py-1.5 bg-background"
            >
              <option value="en">EN</option>
              <option value="it">IT</option>
            </select>
          </nav>
        </div>
      )}
    </header>
  )
}
