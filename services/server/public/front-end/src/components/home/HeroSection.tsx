"use client";
//Remove heroBg CSS background
//Use <Image fill />
/*{/* Background Image ** /}
      <Image
        src={heroBg}
        alt="Hero background"
        fill
        priority
        className="object-cover"
      />
*/

import Link                  from "next/link";
import Image                 from "next/image";
import { ArrowRight, Check } from "lucide-react";
import { Button }            from "@/components/ui/button";
import { useLanguage }       from "@/contexts/LanguageContext";
import heroBg                from "@/assets/hero-bg.jpg";

export function HeroSection () {
    const { t } = useLanguage ();

    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
            {/* Background Image */}
            <Image
                src={heroBg}
                alt="Hero background"
                fill
                priority
                className="object-cover"
            />

            {/* Overlay */}
            <div className="absolute inset-0 bg-background/90" />

            <div className="container relative z-10 py-24 md:py-32">
                <div className="max-w-4xl mx-auto text-center">
                    <p
                        className="text-primary font-medium mb-4 animate-fade-up"
                        style={{ animationDelay: "0ms" }}
                    >
                        {t.hero.punchline}
                    </p>

                    <h1
                        className="font-display text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6 animate-fade-up text-balance"
                        style={{ animationDelay: "100ms" }}
                    >
                        {t.hero.headline}
                    </h1>

                    <p
                            className="text-lg md:text-xl text-muted-foreground mb-6 max-w-3xl mx-auto animate-fade-up text-balance"
                            style={{ animationDelay: "200ms" }}
                    >
                        {t.hero.subheadline}
                    </p>

                    <div
                        className="flex items-center justify-center gap-2 mb-10 animate-fade-up"
                        style={{ animationDelay: "300ms" }}
                    >
                        <Check className="w-5 h-5 text-success" />
                        <span className="text-foreground font-medium">{t.hero.privacyEmphasis}</span>
                    </div>

                    <div
                        className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-up"
                        style={{ animationDelay: "400ms" }}
                    >
                        <Link href="/register">
                            <Button variant="hero" size="xl">
                                {t.hero.ctaPrimary}
                                <ArrowRight className="w-5 h-5" />
                            </Button>
                        </Link>

                        <Link href="/#what-we-do">
                            <Button variant="heroOutline" size="xl">
                                {t.hero.ctaSecondary}
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </section>
    );
}
