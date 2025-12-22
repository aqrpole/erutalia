import { siteConfig } from "@/config/site"
import { Button } from "@/components/ui/button"
import { Mail } from "lucide-react"

export function ContactSection() {
  return (
    <section id="contact" className="py-32 border-t border-border/50">
      <div className="container mx-auto px-4 text-center max-w-3xl">
        <span className="text-sm uppercase tracking-widest text-muted-foreground font-light">Contact</span>
        <h2 className="text-4xl md:text-5xl font-normal mb-6 tracking-tight mt-2">Let's Work Together</h2>
        <p className="text-lg text-muted-foreground mb-12 font-light leading-relaxed">
          Send us an email for your personal quotation of work. We'll get back to you promptly to discuss your project
          requirements.
        </p>

        <a href={`mailto:${siteConfig.email}`}>
          <Button size="lg" className="text-base px-8 py-6 rounded-sm font-normal tracking-wide">
            <Mail className="mr-2 h-5 w-5" strokeWidth={1.5} />
            {siteConfig.email}
          </Button>
        </a>
      </div>
    </section>
  )
}
