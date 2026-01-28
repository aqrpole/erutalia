"use client";

import { useLanguage } from "@/contexts/LanguageContext";

export function AboutSection () {
    const { t } = useLanguage ();

    return (
        <section id="about" className="py-24 bg-background">
            <div className="container">
                <div className="max-w-4xl mx-auto">
                    <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-8 text-center">
                        {t.about.headline}
                    </h2>

                    <p className="text-lg text-muted-foreground text-center leading-relaxed">
                        {t.about.body}
                    </p>
                </div>
            </div>
        </section>
    );
}
