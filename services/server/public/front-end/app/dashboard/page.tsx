import type { Metadata } from "next"
import { DashboardLayout } from "@/components/dashboard/dashboard-layout"
import { ChatInterface } from "@/components/dashboard/chat-interface"

export const metadata: Metadata = {
  title: "Dashboard",
  description: "Your erutalia.com dashboard",
}

export default function DashboardPage() {
  // TODO: Add authentication check
  // const session = await getSession()
  // if (!session) redirect('/login')

  return (
    <DashboardLayout>
      <ChatInterface />
    </DashboardLayout>
  )
}
