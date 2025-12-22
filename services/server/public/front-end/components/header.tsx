import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/40 backdrop-blur-md">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-md bg-primary" />
              <span className="text-xl font-semibold">Nexus AI</span>
            </div>
            <nav className="hidden md:flex items-center gap-6">
              <a href="#platform" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Platform Overview
              </a>
              <a href="#pricing" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </a>
              <a href="#docs" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Documentation
              </a>
              <a href="#forum" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Developer Forum
              </a>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="hidden sm:flex">
              <Search className="h-4 w-4" />
            </Button>
            <Button variant="ghost" className="hidden sm:inline-flex">
              Log in
            </Button>
            <Button>Get Started</Button>
          </div>
        </div>
      </div>
    </header>
  )
}
