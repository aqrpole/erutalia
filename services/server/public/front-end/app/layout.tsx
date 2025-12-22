import type React from "react"
import type { Metadata, Viewport } from "next"
import { EB_Garamond, Geist_Mono } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { siteConfig } from "@/config/site"
import { ConstructionBanner } from "@/components/construction-banner"

const ebGaramond = EB_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
})

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: {
    default: `${siteConfig.name} - ${siteConfig.tagline.en}`,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description.en,
  keywords: [
    "web development",
    "graph analytics",
    "HPC",
    "AI solutions",
    "AgriTech",
    "FinTech",
    "Italy",
    "Padova",
    "machine learning",
    "data science",
  ],
  authors: [{ name: siteConfig.name }],
  creator: siteConfig.name,
  openGraph: {
    type: "website",
    locale: "en_US",
    alternateLocale: ["it_IT"],
    url: "https://erutalia.com",
    title: siteConfig.name,
    description: siteConfig.description.en,
    siteName: siteConfig.name,
  },
  twitter: {
    card: "summary_large_image",
    title: siteConfig.name,
    description: siteConfig.description.en,
  },
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: "/icon.svg",
    apple: "/apple-icon.png",
  },
    generator: 'v0.app'
}

export const viewport: Viewport = {
  themeColor: "#F5F3ED",
  width: "device-width",
  initialScale: 1,
  userScalable: true,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${ebGaramond.variable} ${geistMono.variable} font-sans antialiased`}>
        {siteConfig.features.underConstruction && <ConstructionBanner />}
        {children}
        <Analytics />
      </body>
    </html>
  )
}
