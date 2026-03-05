import type { Metadata }     from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import AppProviders          from "./providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "Home Page | Private RAG AI | erutalia.com",
    description: "",
    authors: [{ name: "erutalia.com" }],
    openGraph: {
        title: "erutalia.com",
        description: "",
        type: "website",
        images: [
            {
                url: "https://erutalia.com/opengraph-image-p98pqg.png",
            },
        ],
    },
    twitter: {
        card: "summary_large_image",
        site: "@Lovable",
        images: ["https://erutalia.com/opengraph-image-p98pqg.png"],
    },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
