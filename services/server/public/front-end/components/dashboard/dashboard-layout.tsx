"use client"

import type React from "react"

import { useState } from "react"
import { LogOut, Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { siteConfig } from "@/config/site"
import { ChatSidebar } from "./chat-sidebar"
import { useRouter } from "next/navigation"

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const router = useRouter()
  const userName = "User" // TODO: Get from session

  const handleLogout = () => {
    // TODO: Implement actual logout
    // localStorage.removeItem('token')
    router.push("/login")
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="border-b bg-background h-16 flex items-center px-4 justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(!sidebarOpen)} className="lg:hidden">
            {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
          <span className="text-xl font-bold">{siteConfig.name}</span>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm text-muted-foreground">{userName}</span>
          <Button variant="outline" size="sm" onClick={handleLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            Logout
          </Button>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <ChatSidebar isOpen={sidebarOpen} />

        {/* Main Content */}
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  )
}
