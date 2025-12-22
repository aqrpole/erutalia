import type { Metadata } from "next"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { siteConfig } from "@/config/site"
import { notFound } from "next/navigation"
import { Share2, Linkedin, Twitter, Instagram } from "lucide-react"
import { Button } from "@/components/ui/button"

type Props = {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const post = siteConfig.blog.featured.find((p) => p.slug === slug)

  if (!post) {
    return {
      title: "Post Not Found",
    }
  }

  return {
    title: post.title.en,
    description: `Read about ${post.title.en} on erutalia.com blog`,
  }
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params
  const post = siteConfig.blog.featured.find((p) => p.slug === slug)

  if (!post) {
    notFound()
  }

  return (
    <div className="min-h-screen flex flex-col">
      <SiteHeader />
      <main className="flex-1 py-12">
        <article className="container mx-auto px-4 max-w-3xl">
          <div className="mb-8">
            <div className="h-64 bg-gradient-to-br from-primary/20 to-accent/20 rounded-lg mb-8" />
            <h1 className="text-4xl font-bold mb-4">{post.title.en}</h1>
            <p className="text-muted-foreground italic mb-6">{post.title.it}</p>
          </div>

          <div className="prose prose-lg max-w-none">
            {/* TODO: Add actual blog content here */}
            <p>This is a template blog post. Replace this content with your actual blog post content.</p>
            <h2>Introduction</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
              dolore magna aliqua.
            </p>
            <h2>Main Content</h2>
            <p>
              Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
              consequat.
            </p>
            <h2>Conclusion</h2>
            <p>
              Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            </p>
          </div>

          <div className="mt-12 pt-8 border-t">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Share2 className="h-5 w-5" />
              Share this article
            </h3>
            <div className="flex gap-2">
              {siteConfig.socialLinks.linkedin && (
                <Button variant="outline" size="icon" asChild>
                  <a href={siteConfig.socialLinks.linkedin} target="_blank" rel="noopener noreferrer">
                    <Linkedin className="h-4 w-4" />
                  </a>
                </Button>
              )}
              {siteConfig.socialLinks.twitter && (
                <Button variant="outline" size="icon" asChild>
                  <a href={siteConfig.socialLinks.twitter} target="_blank" rel="noopener noreferrer">
                    <Twitter className="h-4 w-4" />
                  </a>
                </Button>
              )}
              {siteConfig.socialLinks.instagram && (
                <Button variant="outline" size="icon" asChild>
                  <a href={siteConfig.socialLinks.instagram} target="_blank" rel="noopener noreferrer">
                    <Instagram className="h-4 w-4" />
                  </a>
                </Button>
              )}
            </div>
          </div>
        </article>
      </main>
      <SiteFooter />
    </div>
  )
}
