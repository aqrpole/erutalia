export function SocialProof() {
  const companies = [
    { name: "Stripe", width: "w-24" },
    { name: "Figma", width: "w-20" },
    { name: "Notion", width: "w-24" },
    { name: "Linear", width: "w-24" },
    { name: "Vercel", width: "w-24" },
  ]

  return (
    <section className="py-16 border-y border-border/40">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-muted-foreground mb-10">
          Trusted by innovative teams at leading companies
        </p>
        <div className="flex flex-wrap items-center justify-center gap-12 lg:gap-16">
          {companies.map((company) => (
            <div
              key={company.name}
              className={`${company.width} h-8 rounded bg-muted/50 flex items-center justify-center`}
            >
              <span className="text-sm font-medium text-muted-foreground">{company.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
