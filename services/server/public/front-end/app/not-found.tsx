"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Home, ArrowLeft } from "lucide-react"

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 italian-bg">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-primary mb-4">404</h1>
          <h2 className="text-3xl font-semibold mb-2">Page Not Found</h2>
          <p className="text-xl text-muted-foreground mb-1">Pagina non trovata</p>
          <p className="text-muted-foreground mt-4">The page you're looking for doesn't exist or has been moved.</p>
        </div>

        <div className="flex gap-4 justify-center">
          <Button asChild>
            <Link href="/">
              <Home className="mr-2 h-4 w-4" />
              Go Home
            </Link>
          </Button>
          <Button variant="outline" onClick={() => window.history.back()}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Go Back
          </Button>
        </div>

        {/* Decorative architectural element */}
        <div className="mt-16 flex justify-center">
          <div className="w-32 h-1 bg-primary/30 renaissance-pattern" />
        </div>
      </div>
    </div>
  )
}
