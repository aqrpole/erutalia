"use client";

import { useLanguage } from "@/contexts/LanguageContext";

export function CraftSection () {
    const { t } = useLanguage ();

    return (
        <section className="py-24 bg-secondary">
            <div className="container">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
                        {t.craft.headline}
                    </h2>

                    {/* Decorative line */}
                    <div className="flex items-center justify-center gap-4 mt-8">
                        <div className="h-px w-16 bg-primary/30" />
                        <div className="w-3 h-3 rounded-full bg-primary" />
                        <div className="h-px w-16 bg-primary/30" />
                    </div>
                </div>
            </div>
        </section>
    );
}
