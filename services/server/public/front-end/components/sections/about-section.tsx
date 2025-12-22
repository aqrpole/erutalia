export function AboutSection() {
  return (
    <section id="about" className="py-32 border-t border-border/50">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 gap-16 items-center max-w-6xl mx-auto">
          <div>
            <div className="mb-6">
              <span className="text-sm uppercase tracking-widest text-muted-foreground font-light">About</span>
              <h2 className="text-4xl md:text-5xl font-normal mb-8 tracking-tight mt-2">Our Story</h2>
            </div>
            <div className="space-y-6 text-muted-foreground leading-relaxed">
              <p className="text-base md:text-lg">
                We started this company in 2021, initially as freelancers. After graduation, we formalized our
                operations and expanded our offerings from simple web applications to sophisticated graph analytics
                solutions.
              </p>
              <p className="text-base md:text-lg">
                Our expertise spans finding relationships, contradictions, narrative intelligence, and editorial memory,
                extending to high-performance computing applications that solve complex computational challenges.
              </p>
              <p className="text-base md:text-lg">
                We are a group of friends with experience from startups, education from international universities, and
                hands-on industry knowledge working together to deliver exceptional technology solutions.
              </p>
            </div>
          </div>

          <div className="relative h-[500px] rounded overflow-hidden">
            <img
              src="/team-working-meticulously-on-technology-projects.jpg"
              alt="Our team working meticulously"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
