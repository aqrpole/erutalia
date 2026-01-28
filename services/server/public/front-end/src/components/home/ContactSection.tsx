"use client";

import { Mail }        from "lucide-react";
import { Button }      from "@/components/ui/button";
import { config }      from "@/config";
import { useLanguage } from "@/contexts/LanguageContext";

export function ContactSection () {
    const { t } = useLanguage ();

    return (
        <section className="py-24 bg-primary">
            <div className="container">
                <div className="max-w-3xl mx-auto text-center">
                    <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-foreground mb-8">
                        {t.contact.headline}
                    </h2>

                    <Button
                        asChild
                        variant="secondary"
                        size="xl"
                        className="bg-background text-primary hover:bg-background/90"
                    >
                        <a href={config.contactApiEndpoint}>
                            <Mail className="w-5 h-5" />
                                {t.contact.cta}
                        </a>
                    </Button>
                </div>
            </div>
        </section>
    );
}
