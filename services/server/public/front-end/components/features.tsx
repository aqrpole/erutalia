import { Card } from "@/components/ui/card"
import { Sparkles, Zap, Shield, Code2 } from "lucide-react"

export function Features() {
  const features = [
    {
      icon: Sparkles,
      title: "Advanced AI Models",
      description:
        "Access GPT-5, Claude, and custom models. Powerful general purpose capabilities for a variety of real-world tasks with cutting-edge performance.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description:
        "Optimized infrastructure delivering responses in milliseconds. Built for production workloads with 99.9% uptime SLA.",
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description:
        "SOC 2 Type II compliant with end-to-end encryption. Your data is protected with industry-leading security standards.",
    },
    {
      icon: Code2,
      title: "Developer First",
      description:
        "Simple REST APIs, comprehensive SDKs, and detailed documentation. Build and deploy in minutes, not weeks.",
    },
  ]

  return (
    <section className="py-20 sm:py-28">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight mb-4">Flagship Models</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Our AI models provide powerful capabilities for building the next generation of intelligent applications.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
          {features.map((feature) => (
            <Card
              key={feature.title}
              className="p-8 border-border/50 bg-card/50 backdrop-blur-sm hover:border-border transition-colors"
            >
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <feature.icon className="h-6 w-6" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
