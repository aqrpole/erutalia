"use client"

import { useState } from "react"
import { Search, Plus, Users, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import Link from "next/link"

export function ChatSidebar({ isOpen }: { isOpen: boolean }) {
  const [searchQuery, setSearchQuery] = useState("")

  // TODO: Fetch from API
  const chats = [
    { id: "1", title: "Graph Analytics Discussion", lastMessage: "2 hours ago" },
    { id: "2", title: "HPC Project Setup", lastMessage: "1 day ago" },
    { id: "3", title: "AI Model Training", lastMessage: "3 days ago" },
  ]

  const filteredChats = chats.filter((chat) => chat.title.toLowerCase().includes(searchQuery.toLowerCase()))

  if (!isOpen) return null

  return (
    <aside className="w-80 border-r bg-muted/30 flex flex-col">
      <div className="p-4 space-y-4">
        <Button className="w-full" size="sm">
          <Plus className="h-4 w-4 mr-2" />
          New Chat
        </Button>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      <ScrollArea className="flex-1 px-2">
        <div className="space-y-2 pb-4">
          {filteredChats.map((chat) => (
            <button key={chat.id} className="w-full text-left p-3 rounded-lg hover:bg-accent transition-colors">
              <div className="flex items-start gap-3">
                <MessageSquare className="h-5 w-5 mt-0.5 text-muted-foreground flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{chat.title}</p>
                  <p className="text-sm text-muted-foreground">{chat.lastMessage}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </ScrollArea>

      <div className="border-t p-4">
        <Link href="/dashboard/admin">
          <Button variant="outline" className="w-full bg-transparent" size="sm">
            <Users className="h-4 w-4 mr-2" />
            User Management
          </Button>
        </Link>
      </div>
    </aside>
  )
}
