"use client";

import { CheckCircle } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

export function WhatWeDoSection () {
    const { t } = useLanguage ();

    return (
        <section id="what-we-do" className="py-24 bg-background">
            <div className="container">
                <div className="max-w-4xl mx-auto">
                    <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-8 text-center">
                        {t.whatWeDo.headline}
                    </h2>

                    <p className="text-lg text-muted-foreground mb-12 text-center max-w-3xl mx-auto">
                        {t.whatWeDo.body}
                    </p>

                    <div className="grid md:grid-cols-2 gap-6">
                        {t.whatWeDo.bullets.map ((bullet, index) => (
                            <div 
                                key={index}
                                className="flex items-start gap-4 p-6 bg-secondary rounded-lg card-shadow hover:card-shadow-hover transition-shadow duration-300"
                            >
                                <CheckCircle className="w-6 h-6 text-primary flex-shrink-0 mt-0.5" />
                                <span className="text-foreground font-medium">{bullet}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
};
