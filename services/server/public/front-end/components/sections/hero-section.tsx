import { siteConfig } from "@/config/site"

export function HeroSection() {
  return (
    <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 architectural-grid" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/50 to-background z-0" />

      <div className="container mx-auto px-4 z-10 text-center max-w-5xl">
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-normal mb-8 tracking-tight text-balance leading-tight">
          {siteConfig.tagline.en}
        </h1>
        <p className="text-2xl md:text-3xl text-muted-foreground mb-4 font-light italic tracking-wide">
          {siteConfig.tagline.it}
        </p>
        <div className="mt-12 w-16 h-px bg-foreground/30 mx-auto" />
        <p className="text-base md:text-lg text-muted-foreground max-w-2xl mx-auto mt-12 leading-relaxed font-light">
          {siteConfig.description.en}
        </p>
      </div>
    </section>
  )
}
