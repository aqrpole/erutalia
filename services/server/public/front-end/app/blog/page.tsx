import type { Metadata } from "next"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { siteConfig } from "@/config/site"

export const metadata: Metadata = {
  title: "Blog",
  description: "Latest articles and insights from erutalia.com",
}

const blogPosts = siteConfig.blog.featured

export default function BlogPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <SiteHeader />
      <main className="flex-1 py-12">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-8">Blog</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {blogPosts.map((post) => (
              <Link key={post.id} href={`/blog/${post.slug}`}>
                <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
                  <div className="h-48 bg-gradient-to-br from-primary/20 to-accent/20 rounded-t-lg" />
                  <CardHeader>
                    <CardTitle>{post.title.en}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">Click to read more...</p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </main>
      <SiteFooter />
    </div>
  )
}
