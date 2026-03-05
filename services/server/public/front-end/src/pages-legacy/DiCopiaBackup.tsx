"use client";

import React           from "react";
import { Layout }      from "@/components/layout/Layout";
import { useLanguage } from "@/contexts/LanguageContext";
import { Button }      from "@/components/ui/button";
import { config }      from "@/config";
import {
  XCircle,
  AlertTriangle,
  Headphones,
  Eye,
  RefreshCw,
  Monitor,
  Settings,
  Zap,
  Shield,
  Lock,
  FileCheck,
  Database,
  Download,
  Mail,
  ChevronDown,
  Check,
} from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import dicopiaScreenshots from "@/assets/dicopia-screenshots.png";
import dicopiaHeroBg      from "@/assets/dicopia-hero-bg.jpg";

import Image              from "next/image";

const t = {
  en: {
    hero: {
      sub: "Stop configuring. Start protecting.",
      headline: "DiCopia: Automatic backup and easy recovery for Linux desktops.",
      painPoints: [
        "Are you a system admin? No? Then why are you scripting backups?",
        "Is your data free, or is it held hostage by a cloud provider?",
        "Do you really enjoy tweaking backup settings every week?",
        "Tired of diving into manuals just to restore a single file?",
      ],
      body: "The simple answer to all those headaches: no commands, no vendor lock-in, and no decisions.",
      cta1: "Download",
      cta2: "Request Early Access",
    },
    problem: {
      headline: "When a Linux PC fails, work stops.",
      bullets: [
        "One hardware failure can halt entire operations.",
        "Recovery currently depends on deep technical knowledge.",
        "Restore procedures are rarely tested until disaster strikes.",
      ],
      bigHeadline: "Backup shouldn't require expertise.",
      cta1: "Start 6 months trial",
      cta2: "Contact Us",
    },
    features: {
      headline: "Backup should be boring",
      cards: [
        { icon: "Headphones", title: "Support", desc: "Any problem, we listen. Dedicated assistance when you need it." },
        { icon: "Eye", title: "Transparency", desc: "No hidden surprises, no proprietary lock-in." },
        { icon: "RefreshCw", title: "Updates", desc: "No forced auto-updates in the middle of your work. Update when you want." },
        { icon: "Monitor", title: "Experience", desc: "The same premium, native UI experience you expect from commercial OS apps." },
        { icon: "Settings", title: "Administration", desc: "Easy administration for IT teams with a centralized web dashboard." },
        { icon: "Zap", title: "Simplest", desc: "Frictionless deployment scaling from normal daily users to advanced sysadmins." },
      ],
    },
    howItWorks: {
      headline: "How it works",
      steps: [
        { title: "Install", desc: "Download the AppImage and run. Zero dependencies." },
        { title: "Register & Run", desc: "One-time setup. The background daemon runs silently and automatically." },
        { title: "Restore", desc: "Point, click, and recover files instantly when needed." },
      ],
    },
    pricing: {
      headline: "Simple, transparent pricing",
      tiers: [
        {
          price: "€0",
          title: "Free Trial",
          features: ["6 months free", "OS notifications", "Limited backup size", "Client-side encryption", "Default retention policy", "Bring your own storage (BYOS) or buy from us"],
          cta: "Download",
          highlighted: false,
        },
        {
          price: "€36.60",
          period: "/ 1 yr",
          title: "1 yr license (VAT included)",
          features: ["Editable backup scheduler", "OS notifications & Email alerts", "Limited backup size", "Custom exclusion rules", "BYOS or buy from us"],
          cta: "Contact Us",
          highlighted: true,
        },
        {
          price: "Corporate",
          title: "Corporate Customers",
          features: ["Contract-based subscriptions", "Central Admin Dashboard", "Remote scheduling", "Advanced alerts", "Fleet summary reports", "Multi-user/tenant support", "Controlled retention policies", "BYOS or buy from us"],
          cta: "Contact Us",
          highlighted: false,
        },
      ],
    },
    security: {
      headline: "Security & Data Protection",
      sub: "Your data remains yours. Always.",
      items: [
        { title: "Encryption Standards", desc: "Industry standard AES-256-GCM client-side encryption and TLS 1.3 for transit." },
        { title: "GDPR Alignment", desc: "Supports GDPR requirements: data minimization, secure storage, and data portability." },
        { title: "No Data Reselling", desc: "We do not scan, analyze, monetize, or resell your data. Backups exist only for retention." },
        { title: "Full Data Ownership", desc: "You control exactly where your backups are stored. We take zero ownership." },
      ],
    },
    faq: {
      headline: "Frequently Asked Questions",
      items: [
        { q: "Where is data stored?", a: "We prefer that users bring their own storage (BYOS) based on their needs. However, we do supply storage if you are not interested in managing it yourself, with no extra setup charges." },
        { q: "Does it support all Linux distributions?", a: "Currently supports Linux-based OS (Ubuntu 20.04 and above, RHEL, OpenSUSE, and similar AppImage-compatible distros). We are working to expand platform support." },
        { q: "What happens after the trial?", a: "We notify the user/admin about expiry in advance. Within a week after expiry, the automated backup service stops gracefully." },
        { q: "Can we use our own S3 storage?", a: "Absolutely. We highly recommend Bring Your Own (BYO) storage to facilitate a \"no vendor lock-in\" future." },
        { q: "Is internet required?", a: "Yes, to upload the snapshot backups to your remote storage, the software requires internet access." },
      ],
    },
    finalCta: {
      headline: "Stop hoping your backups work.",
      sub: "Make recovery predictable.",
      cta: "Start free trial",
    },
  },
  it: {
    hero: {
      sub: "Smetti di configurare. Inizia a proteggere.",
      headline: "DiCopia: Backup automatico e ripristino facile per desktop Linux.",
      painPoints: [
        "Sei un amministratore di sistema? No? Allora perché scrivi script per i backup?",
        "I tuoi dati sono liberi o sono in ostaggio di un provider cloud?",
        "Ti piace davvero modificare le impostazioni di backup ogni settimana?",
        "Stanco di immergerti nei manuali solo per ripristinare un singolo file?",
      ],
      body: "La risposta semplice a tutti questi mal di testa: nessun comando, nessun vendor lock-in e nessuna decisione.",
      cta1: "Scarica",
      cta2: "Richiedi Accesso Anticipato",
    },
    problem: {
      headline: "Quando un PC Linux si guasta, il lavoro si ferma.",
      bullets: [
        "Un singolo guasto hardware può bloccare intere operazioni.",
        "Attualmente il ripristino dipende da profonde conoscenze tecniche.",
        "Le procedure di ripristino vengono raramente testate finché non si verifica un disastro.",
      ],
      bigHeadline: "Il backup non dovrebbe richiedere competenze tecniche.",
      cta1: "Inizia la prova di 6 mesi",
      cta2: "Contattaci",
    },
    features: {
      headline: "Il backup dovrebbe essere noioso",
      cards: [
        { icon: "Headphones", title: "Supporto", desc: "Qualsiasi problema, ti ascoltiamo. Assistenza dedicata quando ne hai bisogno." },
        { icon: "Eye", title: "Trasparenza", desc: "Nessuna sorpresa nascosta, nessun vincolo proprietario." },
        { icon: "RefreshCw", title: "Aggiornamenti", desc: "Nessun aggiornamento automatico forzato nel bel mezzo del lavoro. Aggiorna quando tu vuoi." },
        { icon: "Monitor", title: "Esperienza", desc: "La stessa esperienza UI nativa e premium che ti aspetti dalle app commerciali." },
        { icon: "Settings", title: "Amministrazione", desc: "Gestione semplice per i team IT con una dashboard web centralizzata." },
        { icon: "Zap", title: "Semplicità", desc: "Distribuzione senza attriti, adatta sia agli utenti comuni che ai sysadmin avanzati." },
      ],
    },
    howItWorks: {
      headline: "Come funziona",
      steps: [
        { title: "Installa", desc: "Scarica l'AppImage ed esegui. Zero dipendenze." },
        { title: "Registra ed Esegui", desc: "Configurazione una tantum. Il demone in background viene eseguito in modo silenzioso e automatico." },
        { title: "Ripristina", desc: "Punta, clicca e recupera i file istantaneamente quando necessario." },
      ],
    },
    pricing: {
      headline: "Prezzi semplici e trasparenti",
      tiers: [
        {
          price: "€0",
          title: "Prova Gratuita",
          features: ["6 mesi gratuiti", "Notifiche OS", "Dimensioni di backup limitate", "Crittografia lato client", "Policy di conservazione predefinita", "Porta il tuo storage (BYOS) o acquistalo da noi"],
          cta: "Scarica",
          highlighted: false,
        },
        {
          price: "€36.60",
          period: "/ 1 anno",
          title: "Licenza 1 anno (IVA inclusa)",
          features: ["Pianificatore di backup modificabile", "Notifiche OS e avvisi email", "Dimensioni di backup limitate", "Regole di esclusione personalizzate", "BYOS o acquistalo da noi"],
          cta: "Contattaci",
          highlighted: true,
        },
        {
          price: "Corporate",
          title: "Clienti Corporate",
          features: ["Abbonamenti basati su contratto", "Dashboard di Amministrazione Centrale", "Pianificazione remota", "Avvisi avanzati", "Report di flotta", "Supporto multi-utente/tenant", "Policy di conservazione controllate", "BYOS o acquistalo da noi"],
          cta: "Contattaci",
          highlighted: false,
        },
      ],
    },
    security: {
      headline: "Sicurezza e Protezione dei Dati",
      sub: "I tuoi dati restano tuoi. Sempre.",
      items: [
        { title: "Standard di Crittografia", desc: "Crittografia lato client AES-256-GCM standard del settore e TLS 1.3 per il transito." },
        { title: "Allineamento GDPR", desc: "Supporta i requisiti GDPR: minimizzazione dei dati, archiviazione sicura e portabilità dei dati." },
        { title: "Nessuna Rivendita", desc: "Non scansioniamo, analizziamo, monetizziamo o rivendiamo i tuoi dati. I backup esistono solo per la conservazione." },
        { title: "Piena Proprietà dei Dati", desc: "Sei tu a controllare esattamente dove sono archiviati i tuoi backup. Noi non assumiamo alcuna proprietà." },
      ],
    },
    faq: {
      headline: "Domande Frequenti (FAQ)",
      items: [
        { q: "Dove sono archiviati i dati?", a: "Preferiamo che gli utenti portino il proprio spazio di archiviazione (BYOS) in base alle loro esigenze. Tuttavia, forniamo spazio se non sei interessato a gestirlo da solo, senza costi di configurazione aggiuntivi." },
        { q: "Supporta tutte le distribuzioni Linux?", a: "Attualmente supporta i sistemi operativi basati su Linux (Ubuntu 20.04 e successivi, RHEL, OpenSUSE e distro compatibili con AppImage simili). Stiamo lavorando per espandere il supporto della piattaforma." },
        { q: "Cosa succede dopo la prova?", a: "Avvisiamo in anticipo l'utente/amministratore della scadenza. Entro una settimana dalla scadenza, il servizio di backup automatico si interrompe in modo graduale." },
        { q: "Possiamo usare il nostro spazio di archiviazione S3?", a: "Assolutamente. Consigliamo vivamente di portare il proprio spazio di archiviazione (BYO) per facilitare un futuro senza vincoli di fornitore (no vendor lock-in)." },
        { q: "È necessaria una connessione internet?", a: "Sì, per caricare i backup delle snapshot sull'archiviazione remota, il software richiede l'accesso a internet." },
      ],
    },
    finalCta: {
      headline: "Smetti di sperare che i tuoi backup funzionino.",
      sub: "Rendi il ripristino prevedibile.",
      cta: "Inizia la prova gratuita",
    },
  },
};

const featureIcons: Record<string, React.ElementType> = {
  Headphones,
  Eye,
  RefreshCw,
  Monitor,
  Settings,
  Zap,
};

const securityIcons = [Lock, Shield, FileCheck, Database];
// {/* SEO */}
//<title>{language === "it" ? "DiCopia - Backup Linux Aziendale | erutalia.com" : "DiCopia - Enterprise Linux Backup | erutalia.com"}</title>

export default function DiCopiaPage () {
  const { language } = useLanguage ();
  const c            = t[language];

  return (
    <Layout>

      {/* ===== HERO ===== */}
      <section
        className="relative overflow-hidden bg-background"
      >
        <div 
          className="absolute inset-0 opacity-[0.06]"
          style={{
            backgroundImage: `url(${dicopiaHeroBg.src})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        />
        <div className="container relative z-10 py-20 md:py-28">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left */}
            <div className="animate-fade-up">
              <p className="text-primary font-semibold mb-3 tracking-wide uppercase text-sm">
                {c.hero.sub}
              </p>
              <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-8 text-balance">
                {c.hero.headline}
              </h1>
              <ul className="space-y-3 mb-8">
                {c.hero.painPoints.map((point, i) => (
                  <li key={i} className="text-muted-foreground">
                    {point}
                  </li>
                ))}
              </ul>
              <p className="text-foreground font-medium text-lg mb-8">
                {c.hero.body}
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button variant="hero" size="xl">
                  <Download className="w-5 h-5" />
                  {c.hero.cta1}
                </Button>
                <a href={config.contactApiEndpoint}>
                  <Button variant="heroOutline" size="xl">
                    <Mail className="w-5 h-5" />
                    {c.hero.cta2}
                  </Button>
                </a>
              </div>
            </div>
            {/* Right */}
            <div className="relative flex items-center justify-center animate-fade-in" style={{ animationDelay: "200ms" }}>
              <div className="absolute w-80 h-80 bg-primary/10 rounded-full blur-3xl" />
              <Image
                src={dicopiaScreenshots}
                alt="DiCopia backup software interface"
                className="relative z-10 rounded-xl shadow-2xl max-w-full"
                priority
              />
            </div>
          </div>
        </div>
      </section>

      {/* ===== THE PROBLEM ===== */}
      <section className="py-20 bg-secondary/30">
        <div className="container max-w-3xl text-center">
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-10">
            {c.problem.headline}
          </h2>
          <ul className="space-y-4 mb-10 max-w-xl mx-auto">
            {c.problem.bullets.map((b, i) => (
              <li key={i} className="text-muted-foreground text-center">
                {b}
              </li>
            ))}
          </ul>
          <h3 className="font-display text-2xl md:text-3xl font-bold text-primary mb-10">
            {c.problem.bigHeadline}
          </h3>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="hero" size="xl">
              {c.problem.cta1}
            </Button>
            <a href={config.contactApiEndpoint}>
              <Button variant="heroOutline" size="xl">
                {c.problem.cta2}
              </Button>
            </a>
          </div>
        </div>
      </section>

      {/* ===== FEATURES GRID ===== */}
      <section className="py-20 bg-background">
        <div className="container">
          <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground text-center mb-14">
            {c.features.headline}
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {c.features.cards.map((card, i) => {
              const Icon = featureIcons[card.icon] || Zap;
              return (
                <div
                  key={i}
                  className="p-6 rounded-lg border border-border bg-card card-shadow hover:card-shadow-hover transition-shadow"
                >
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="font-display text-xl font-semibold text-foreground mb-2">
                    {card.title}
                  </h3>
                  <p className="text-muted-foreground text-sm">{card.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ===== HOW IT WORKS ===== */}
      <section className="py-20 bg-secondary/30">
        <div className="container max-w-4xl">
          <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground text-center mb-14">
            {c.howItWorks.headline}
          </h2>
          <div className="grid md:grid-cols-3 gap-10">
            {c.howItWorks.steps.map((step, i) => (
              <div key={i} className="text-center">
                <div className="w-16 h-16 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-2xl font-bold mx-auto mb-6 font-display">
                  {i + 1}
                </div>
                <h3 className="font-display text-xl font-semibold text-foreground mb-3">
                  {step.title}
                </h3>
                <p className="text-muted-foreground text-sm">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== PRICING ===== */}
      <section className="py-20 bg-background">
        <div className="container">
          <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground text-center mb-14">
            {c.pricing.headline}
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {c.pricing.tiers.map((tier, i) => (
              <div
                key={i}
                className={`rounded-xl border p-8 flex flex-col ${
                  tier.highlighted
                    ? "border-primary bg-primary/5 shadow-lg ring-2 ring-primary/20 scale-105"
                    : "border-border bg-card card-shadow"
                }`}
              >
                <div className="mb-6">
                  <span className="font-display text-3xl font-bold text-foreground">
                    {tier.price}
                  </span>
                  {"period" in tier && (
                    <span className="text-muted-foreground text-sm ml-1">
                      {tier.period}
                    </span>
                  )}
                </div>
                <h3 className="font-display text-lg font-semibold text-foreground mb-4">
                  {tier.title}
                </h3>
                <ul className="space-y-3 mb-8 flex-1">
                  {tier.features.map((f, j) => (
                    <li key={j} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <Check className="w-4 h-4 text-success shrink-0 mt-0.5" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                {tier.cta === "Download" || tier.cta === "Scarica" ? (
                  <Button variant={tier.highlighted ? "hero" : "outline"} size="lg" className="w-full">
                    <Download className="w-4 h-4" />
                    {tier.cta}
                  </Button>
                ) : (
                  <a href={config.contactApiEndpoint}>
                    <Button variant={tier.highlighted ? "hero" : "outline"} size="lg" className="w-full">
                      <Mail className="w-4 h-4" />
                      {tier.cta}
                    </Button>
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== SECURITY ===== */}
      <section className="py-20 bg-primary/5">
        <div className="container">
          <div className="text-center mb-14">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
              {c.security.headline}
            </h2>
            <p className="text-muted-foreground text-lg">{c.security.sub}</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {c.security.items.map((item, i) => {
              const Icon = securityIcons[i];
              return (
                <div key={i} className="text-center">
                  <div className="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-7 h-7 text-primary" />
                  </div>
                  <h3 className="font-display text-lg font-semibold text-foreground mb-2">
                    {item.title}
                  </h3>
                  <p className="text-muted-foreground text-sm">{item.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ===== FAQ ===== */}
      <section className="py-20 bg-background">
        <div className="container max-w-3xl">
          <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground text-center mb-14">
            {c.faq.headline}
          </h2>
          <Accordion type="single" collapsible className="w-full">
            {c.faq.items.map((item, i) => (
              <AccordionItem key={item.q} value={`faq-${i}`}> {/* ===== key={i} value={`faq-${i}`} ===== */}
                <AccordionTrigger className="text-left font-medium text-foreground">
                  {item.q}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground">
                  {item.a}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>

      {/* ===== FINAL CTA ===== */}
      <section className="py-24 bg-primary/5">
        <div className="container text-center">
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            {c.finalCta.headline}
          </h2>
          <p className="text-lg text-muted-foreground mb-10">
            {c.finalCta.sub}
          </p>
          <Button variant="hero" size="xl">
            <Download className="w-5 h-5" />
            {c.finalCta.cta}
          </Button>
        </div>
      </section>
    </Layout>
  );
};
