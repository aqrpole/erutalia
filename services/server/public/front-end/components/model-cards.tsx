import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Check } from "lucide-react"

export function ModelCards() {
  const models = [
    {
      name: "GPT-5",
      tagline: "Smartest model for complex tasks",
      features: ["Text and vision", "128K context length", "Advanced reasoning", "Function calling"],
    },
    {
      name: "GPT-5 mini",
      tagline: "Affordable model balancing speed and intelligence",
      features: ["Text and vision", "128K context length", "Fast responses", "Cost effective"],
    },
    {
      name: "GPT-5 nano",
      tagline: "Fastest, most cost-effective model for low-latency tasks",
      features: ["Text and vision", "64K context length", "Sub-second latency", "Lowest cost"],
    },
  ]

  return (
    <section className="py-20 sm:py-28 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight mb-4">Our GPT models</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Powerful general purpose models for a variety of real-world tasks with a refreshed knowledge cutoff of June
            2024.
          </p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {models.map((model, index) => (
            <Card key={model.name} className="p-8 border-border/50 bg-card backdrop-blur-sm">
              {index === 0 && (
                <Badge className="mb-4 bg-primary/10 text-primary hover:bg-primary/20">Most Capable</Badge>
              )}
              <h3 className="text-2xl font-bold mb-2">{model.name}</h3>
              <p className="text-sm text-muted-foreground mb-6 leading-relaxed">{model.tagline}</p>
              <ul className="space-y-3">
                {model.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3 text-sm">
                    <Check className="h-4 w-4 text-primary flex-shrink-0" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
