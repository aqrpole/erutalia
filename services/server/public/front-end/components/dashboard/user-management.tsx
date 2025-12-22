"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Trash2, UserPlus, Loader2 } from "lucide-react"
// import { apiConfig } from '@/config/api'

type User = {
  id: string
  name: string
  email: string
  createdAt: string
}

export function UserManagement() {
  const [users, setUsers] = useState<User[]>([
    { id: "1", name: "John Doe", email: "john@example.com", createdAt: "2024-01-15" },
    { id: "2", name: "Jane Smith", email: "jane@example.com", createdAt: "2024-01-20" },
  ])
  const [showAddForm, setShowAddForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [newUser, setNewUser] = useState({ name: "", email: "", password: "" })

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // TODO: Uncomment when API is ready
      // const response = await fetch(`${apiConfig.baseUrl}${apiConfig.endpoints.createUser}`, {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${localStorage.getItem('token')}`
      //   },
      //   body: JSON.stringify(newUser)
      // })
      // const data = await response.json()
      // setUsers(prev => [...prev, data])

      // Simulated
      await new Promise((resolve) => setTimeout(resolve, 1000))
      const user: User = {
        id: Date.now().toString(),
        name: newUser.name,
        email: newUser.email,
        createdAt: new Date().toISOString().split("T")[0],
      }
      setUsers((prev) => [...prev, user])
      setNewUser({ name: "", email: "", password: "" })
      setShowAddForm(false)
    } catch (error) {
      console.error("Add user error:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteUser = async (userId: string) => {
    if (!confirm("Are you sure you want to delete this user?")) return

    try {
      // TODO: Uncomment when API is ready
      // await fetch(`${apiConfig.baseUrl}${apiConfig.endpoints.deleteUser(userId)}`, {
      //   method: 'DELETE',
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('token')}`
      //   }
      // })

      setUsers((prev) => prev.filter((u) => u.id !== userId))
    } catch (error) {
      console.error("Delete user error:", error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold">Users</h2>
        <Button onClick={() => setShowAddForm(!showAddForm)}>
          <UserPlus className="h-4 w-4 mr-2" />
          Add User
        </Button>
      </div>

      {showAddForm && (
        <Card>
          <CardHeader>
            <CardTitle>Add New User</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddUser} className="space-y-4">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  value={newUser.name}
                  onChange={(e) => setNewUser((prev) => ({ ...prev, name: e.target.value }))}
                  required
                  disabled={loading}
                />
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={newUser.email}
                  onChange={(e) => setNewUser((prev) => ({ ...prev, email: e.target.value }))}
                  required
                  disabled={loading}
                />
              </div>
              <div>
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={newUser.password}
                  onChange={(e) => setNewUser((prev) => ({ ...prev, password: e.target.value }))}
                  required
                  disabled={loading}
                />
              </div>
              <div className="flex gap-2">
                <Button type="submit" disabled={loading}>
                  {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : null}
                  Add User
                </Button>
                <Button type="button" variant="outline" onClick={() => setShowAddForm(false)}>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4">
        {users.map((user) => (
          <Card key={user.id}>
            <CardContent className="flex justify-between items-center p-6">
              <div>
                <h3 className="font-semibold">{user.name}</h3>
                <p className="text-sm text-muted-foreground">{user.email}</p>
                <p className="text-xs text-muted-foreground mt-1">Joined: {user.createdAt}</p>
              </div>
              <Button variant="destructive" size="icon" onClick={() => handleDeleteUser(user.id)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
