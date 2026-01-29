// Application Configuration
export const config = {
  companyName       : "erutalia.com",
  address           : "Via Nicolo Tommaseo 1, Padova (PD), Veneto, Italy",
  contactApiEndpoint: "/api/contact-email",
  
  // API Configuration, next.js can;t work, need deterministic. so always get it in frontend
  //apiBaseUrl: typeof window !== 'undefined' ? window.location.origin : '',
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL ?? "",
  //env never created so find origin in each API
  
  // Token limits
  tokenLimits: {
    maxTokens    : 4096,
    maxCharacters: 16000,
  },
  
  // Banner Configuration
  banner: {
    visible: true,
    text: {
      it: "Sito in costruzione",
      en: "Under Construction"
    }
  },
  
  // Social Links
  social: {
    linkedin : "https://linkedin.com/company/erutalia",
    instagram: "https://instagram.com/erutalia",
    twitter  : "https://twitter.com/erutalia", //NOT CREATED
    github   : "https://github.com/erutalia", //NOT CREATED
    facebook : "https://www.facebook.com/Erutalia",
  },
  
  // Blog Featured Posts
  featuredBlogSlugs: [
    "why-graphs-matter",
    "choosing-databases",
    "getting-started-graph-analytics",
    "high-performance-computing"
  ],
  
  // Default Language
  defaultLanguage: "it" as const,
} as const;

export type Language = "it" | "en";
