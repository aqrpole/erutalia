import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Brain, BarChart3, Code, Smartphone, Server, Cpu, Database, Sprout } from "lucide-react"

const services = [
  {
    icon: Sprout,
    title: "AgriTech AI",
    description: "Detection systems using AI and predictive analysis for agricultural applications",
  },
  {
    icon: BarChart3,
    title: "FinTech + Economics",
    description: "Dashboard creations, KPI monitoring, and comprehensive financial analytics",
  },
  {
    icon: Code,
    title: "Custom Full Stack Apps",
    description:
      "MERN (JavaScript), Python, or Flutter based applications. Customization of OpenEMR, Odoo, ERPNext, Moodle, and other open-source platforms",
  },
  {
    icon: Smartphone,
    title: "Mobile Apps",
    description: "React Native or Flutter based mobile applications for iOS and Android",
  },
  {
    icon: Cpu,
    title: "Scientific Applications",
    description: "HPC, Big Data processing, and high-performance computing solutions",
  },
  {
    icon: Server,
    title: "Server Management",
    description: "Daily monitoring, security hardening, and backup maintenance services",
  },
  {
    icon: Brain,
    title: "Personalized AI",
    description: "Custom AI solutions using open source libraries tailored to your specific needs",
  },
  {
    icon: Database,
    title: "Private AI Systems",
    description:
      "Chroma or Qdrant based private/public AI systems using AWS Bedrock or OpenRouter. Privacy-first solutions with private server deployment options",
  },
]

export function ServicesSection() {
  return (
    <section id="services" className="py-32 bg-secondary/20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-20 max-w-3xl mx-auto">
          <span className="text-sm uppercase tracking-widest text-muted-foreground font-light">Services</span>
          <h2 className="text-4xl md:text-5xl font-normal mb-6 tracking-tight mt-2">What We Offer</h2>
          <p className="text-lg text-muted-foreground font-light leading-relaxed">
            From web development to AI solutions, we bring expertise across the technology spectrum
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
          {services.map((service, index) => (
            <Card
              key={index}
              className="hover:shadow-md transition-all duration-300 border-border/50 bg-card/50 backdrop-blur"
            >
              <CardHeader className="space-y-4">
                <service.icon className="h-10 w-10 text-foreground/70" strokeWidth={1.5} />
                <CardTitle className="text-lg font-medium tracking-tight">{service.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed font-light">{service.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
