export const siteConfig = {
  name: "erutalia.com",
  tagline: {
    en: "trust our connectedness",
    it: "fidiamoci della nostra connessione",
  },
  description: {
    en: "From simple webapps to graph analytics, HPC applications, and AI solutions",
    it: "Da semplici webapp all'analisi dei grafi, applicazioni HPC e soluzioni AI",
  },
  address: "via nicolo tommaseo 1, PD, Veneto, Italy",
  email: "ashwini.erutalia@trustpec.it",
  pec: "ashwini.erutalia@trustpec.it",
  socialLinks: {
    linkedin: "",
    instagram: "",
    twitter: "",
  },
  blog: {
    featured: [
      {
        id: "1",
        slug: "getting-started-graph-analytics",
        title: { en: "Getting Started with Graph Analytics", it: "Iniziare con l'analisi dei grafi" },
      },
      {
        id: "2",
        slug: "ai-in-agritech",
        title: { en: "AI in AgriTech: Detection Systems", it: "AI in AgriTech: Sistemi di Rilevamento" },
      },
      {
        id: "3",
        slug: "hpc-applications",
        title: { en: "High Performance Computing Applications", it: "Applicazioni di calcolo ad alte prestazioni" },
      },
    ],
  },
  features: {
    underConstruction: true,
    underConstructionBannerColor: "#d97706", // amber-600
  },
  dashboard: {
    maxChatTokens: 4000,
    maxChatCharacters: 16000,
  },
}

export type SiteConfig = typeof siteConfig
