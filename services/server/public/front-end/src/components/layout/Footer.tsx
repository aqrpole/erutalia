"use client";

import React                            from "react";
import Link                             from "next/link";
import { Linkedin, Instagram, Facebook } from "lucide-react";
import { config }                       from "@/config";
import { useLanguage }                  from "@/contexts/LanguageContext";

export const Footer: React.FC = () => {
    const { t }       = useLanguage ();
    const currentYear = new Date ().getFullYear ();

    return (
        <footer className="bg-secondary border-t border-border">
            <div className="container py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Company Info */}
                    <div className="md:col-span-2">
                        <span className="font-display text-2xl font-bold text-primary">
                            {config.companyName}
                        </span>
                        
                        <p className="mt-4 text-sm text-muted-foreground max-w-md">
                            {config.address}
                        </p>

                        {/* Social Links */}
                        <div className="flex gap-4 mt-6">
                            <a
                                href={config.social.linkedin}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="p-2 rounded-full bg-background hover:bg-primary hover:text-primary-foreground transition-colors"
                                aria-label="LinkedIn"
                            >
                                <Linkedin className="w-5 h-5" />
                            </a>
                            <a
                                href={config.social.instagram}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="p-2 rounded-full bg-background hover:bg-primary hover:text-primary-foreground transition-colors"
                                aria-label="Instagram"
                            >
                                <Instagram className="w-5 h-5" />
                            </a>
                            <a
                                href={config.social.facebook}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="p-2 rounded-full bg-background hover:bg-primary hover:text-primary-foreground transition-colors"
                                aria-label="Facebook"
                            >
                                <Facebook className="w-5 h-5" />
                            </a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="font-semibold text-foreground mb-4">Links</h4>
                            <ul className="space-y-2">
                                <li>
                                    <Link
                                        href="/#about"
                                        className="text-sm text-muted-foreground hover:text-primary transition-colors"
                                    >
                                        {t.nav.aboutUs}
                                    </Link>
                                </li>
                                <li>
                                    <Link
                                        href="/projects"
                                        className="text-sm text-muted-foreground hover:text-primary transition-colors"
                                    >
                                        {t.nav.projects}
                                    </Link>
                                </li>
                                <li>
                                    <Link
                                        href="/blog"
                                        className="text-sm text-muted-foreground hover:text-primary transition-colors"
                                    >
                                        {t.nav.blog}
                                    </Link>
                                </li>
                                <li>
                                    <a
                                        href={config.contactApiEndpoint}
                                        className="text-sm text-muted-foreground hover:text-primary transition-colors"
                                    >
                                        {t.nav.contact}
                                    </a>
                                </li>
                            </ul>
                        </div>

                    {/* Legal */}
                    <div>
                        <h4 className="font-semibold text-foreground mb-4">Legal</h4>
                        <ul className="space-y-2">
                            <li>
                                <Link
                                    href="/privacy"
                                    className="text-sm text-muted-foreground hover:text-primary transition-colors"
                                >
                                    {t.footer.privacyPolicy}
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/terms"
                                    className="text-sm text-muted-foreground hover:text-primary transition-colors"
                                >
                                    {t.footer.termsConditions}
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Copyright */}
                <div className="mt-12 pt-8 border-t border-border text-center text-sm text-muted-foreground">
                    © {currentYear} {config.companyName}. {t.footer.allRightsReserved}.
                </div>
            </div>
        </footer>
    );
};
