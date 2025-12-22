import type { Metadata } from "next"
import { LoginForm } from "@/components/auth/login-form"
import { SiteHeader } from "@/components/site-header"
import Link from "next/link"

export const metadata: Metadata = {
  title: "Login",
  description: "Login to your erutalia.com account",
}

export default function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <SiteHeader />
      <main className="flex-1 flex items-center justify-center p-4 italian-bg">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold tracking-tight mb-2">Welcome Back</h1>
            <p className="text-muted-foreground">Sign in to your account</p>
          </div>
          <LoginForm />
          <p className="text-center mt-6 text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link href="/register" className="text-primary hover:underline font-medium">
              Register here
            </Link>
          </p>
        </div>
      </main>
    </div>
  )
}
