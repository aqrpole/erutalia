import type { Metadata } from "next"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"

export const metadata: Metadata = {
  title: "Privacy Policy",
}

export default function PrivacyPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <SiteHeader />
      <main className="flex-1 py-12">
        <div className="container mx-auto px-4 max-w-3xl">
          <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
          <div className="prose prose-lg max-w-none">
            <p>Last updated: {new Date().toLocaleDateString()}</p>
            <h2>Introduction</h2>
            <p>This Privacy Policy describes how erutalia.com collects, uses, and shares your personal information.</p>
            {/* TODO: Add your actual privacy policy content */}
            <h2>Information We Collect</h2>
            <p>We collect information you provide directly to us...</p>
            <h2>How We Use Your Information</h2>
            <p>We use the information we collect to...</p>
            <h2>Contact Us</h2>
            <p>If you have any questions about this Privacy Policy, please contact us.</p>
          </div>
        </div>
      </main>
      <SiteFooter />
    </div>
  )
}
