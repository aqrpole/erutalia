import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export function CTA() {
  return (
    <section className="py-20 sm:py-28">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight mb-6 text-balance">
            Start building with AI today
          </h2>
          <p className="text-lg text-muted-foreground mb-10 leading-relaxed text-balance">
            Join thousands of developers creating the next generation of intelligent applications. Get started in
            minutes with our comprehensive documentation and support.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button size="lg" className="text-base px-8">
              Get API access
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="text-base px-8 bg-transparent">
              Read documentation
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
