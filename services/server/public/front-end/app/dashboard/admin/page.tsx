import type { Metadata } from "next"
import { DashboardLayout } from "@/components/dashboard/dashboard-layout"
import { UserManagement } from "@/components/dashboard/user-management"

export const metadata: Metadata = {
  title: "User Management",
  description: "Manage users",
}

export default function AdminPage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">User Management</h1>
        <UserManagement />
      </div>
    </DashboardLayout>
  )
}
