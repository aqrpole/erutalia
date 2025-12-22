import type { Metadata } from "next"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"

export const metadata: Metadata = {
  title: "Terms and Conditions",
}

export default function TermsPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <SiteHeader />
      <main className="flex-1 py-12">
        <div className="container mx-auto px-4 max-w-3xl">
          <h1 className="text-4xl font-bold mb-8">Terms and Conditions</h1>
          <div className="prose prose-lg max-w-none">
            <p>Last updated: {new Date().toLocaleDateString()}</p>
            <h2>Agreement to Terms</h2>
            <p>By accessing or using erutalia.com, you agree to be bound by these Terms and Conditions.</p>
            {/* TODO: Add your actual terms and conditions content */}
            <h2>Use License</h2>
            <p>Permission is granted to temporarily use the services...</p>
            <h2>Limitations</h2>
            <p>In no event shall erutalia.com be liable for any damages...</p>
            <h2>Contact</h2>
            <p>For any questions regarding these terms, please contact us.</p>
          </div>
        </div>
      </main>
      <SiteFooter />
    </div>
  )
}
