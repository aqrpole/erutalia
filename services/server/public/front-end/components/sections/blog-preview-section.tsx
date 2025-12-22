import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { siteConfig } from "@/config/site"
import { ArrowRight } from "lucide-react"

export function BlogPreviewSection() {
  return (
    <section className="py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center mb-12">
          <h2 className="text-4xl font-bold tracking-tight">Latest Insights</h2>
          <Link href="/blog">
            <Button variant="outline">
              View All <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {siteConfig.blog.featured.map((post) => (
            <Link key={post.id} href={`/blog/${post.slug}`}>
              <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
                <div className="h-48 bg-gradient-to-br from-primary/20 to-accent/20 rounded-t-lg" />
                <CardHeader>
                  <CardTitle className="text-xl">{post.title.en}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>Click to read more about this topic...</CardDescription>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
