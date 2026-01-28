"use client";

import {
    Sprout,
    TrendingUp,
    Code,
    Settings,
    Smartphone,
    Cpu,
    Server,
    Bot,
    Lock,
    GitBranch,
} from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

const icons = [
    Sprout,
    TrendingUp,
    Code,
    Settings,
    Smartphone,
    Cpu,
    Server,
    Bot,
    Lock,
    GitBranch,
];

export function ExpertiseSection () {
    const { t } = useLanguage ();

    return (
        <section className="py-24 bg-secondary">
            <div className="container">
                <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-12 text-center">
                    {t.expertise.headline}
                </h2>

                <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {t.expertise.items.map ((item, index) => {
                        const Icon = icons[index] || Code;

                        return (
                            <div
                                key={index}
                                className="bg-background p-6 rounded-lg card-shadow hover:card-shadow-hover transition-all duration-300 hover:-translate-y-1 group"
                            >
                                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                                    <Icon className="w-6 h-6 text-primary" />
                                </div>

                                <h3 className="font-semibold text-foreground mb-2">{item.title}</h3>
                                <p className="text-sm text-muted-foreground">{item.description}</p>
                            </div>
                        );
                    })}
                </div>
            </div>
        </section>
    );
}
