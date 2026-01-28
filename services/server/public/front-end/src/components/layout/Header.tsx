"use client";

import React, { useState }   from "react";
import Link                  from "next/link";
//import { Link, useNavigate } from "react-router-dom";
import { useRouter }         from "next/navigation";
import { Menu, X, Globe }    from "lucide-react";
import { Button }            from "@/components/ui/button";
import { config }            from "@/config";
import { useLanguage }       from "@/contexts/LanguageContext";
import { useAuth }           from "@/contexts/AuthContext";

export const Header: React.FC = () => {
    const [isMenuOpen, setIsMenuOpen]  = useState (false);
    const { language, setLanguage, t } = useLanguage ();
    const { isAuthenticated, logout }  = useAuth ();
    const router                       = useRouter ();

    const toggleLanguage = () => {
        setLanguage (language === "it" ? "en" : "it");
    };

    const handleLogout = async () => {
        await logout ();
        router.push ("/");
    };

    return (
        <header className="sticky top-8 z-40 w-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 border-b border-border">
            <div className="container flex h-16 items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center space-x-2">
                    <span className="font-display text-2xl font-bold text-primary">
                        {config.companyName}
                    </span>
                </Link>

                {/* Desktop Navigation */}
                <nav className="hidden md:flex items-center gap-6">
                    <Link
                        href="/#about"
                        className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                        {t.nav.aboutUs}
                    </Link>
                    <Link
                        href="/projects"
                        className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                        {t.nav.projects}
                    </Link>
                    <Link
                        href="/blog"
                        className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                        {t.nav.blog}
                    </Link>
                    <a
                        href={config.contactApiEndpoint}
                        className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                        {t.nav.contact}
                    </a>

                    <button
                        onClick={toggleLanguage}
                        className="flex items-center gap-1 text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                        <Globe className="w-4 h-4" />
                        {language.toUpperCase ()}
                    </button>

                    {isAuthenticated ? (
                        <>
                            <Link href="/dashboard">
                                <Button variant="ghost" size="sm">
                                    {t.nav.dashboard}
                                </Button>
                            </Link>
                            <Button variant="outline" size="sm" onClick={handleLogout}>
                                {t.nav.logout}
                            </Button>
                        </>
                    ) : (
                        <>
                            <Link href="/login">
                                <Button variant="ghost" size="sm">
                                    {t.nav.login}
                                </Button>
                            </Link>
                            <Link href="/register">
                                <Button size="sm">
                                    {t.nav.register}
                                </Button>
                            </Link>
                        </>
                    )}
                </nav>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2"
                    onClick={() => setIsMenuOpen (!isMenuOpen)}
                    aria-label="Toggle menu"
                >
                    {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                </button>
            </div>

            {/* Mobile Navigation */}
            {isMenuOpen && (
                <div className="md:hidden border-t border-border bg-background">
                    <nav className="container py-4 flex flex-col gap-4">
                        <Link
                            href="/#about"
                            className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                            onClick={() => setIsMenuOpen (false)}
                        >
                            {t.nav.aboutUs}
                        </Link>
                        <Link
                            href="/projects"
                            className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                            onClick={() => setIsMenuOpen (false)}
                        >
                            {t.nav.projects}
                        </Link>
                        <Link
                            href="/blog"
                            className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                            onClick={() => setIsMenuOpen (false)}
                        >
                            {t.nav.blog}
                        </Link>
                        <a
                            href={config.contactApiEndpoint}
                            className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                        >
                            {t.nav.contact}
                        </a>

                        <button
                            onClick={toggleLanguage}
                            className="flex items-center gap-1 text-sm font-medium text-foreground/80 hover:text-primary transition-colors"
                        >
                            <Globe className="w-4 h-4" />
                            {language === "it" ? "English" : "Italiano"}
                        </button>

                        <div className="flex gap-2 pt-2">
                            {isAuthenticated ? (
                                <>
                                    <Link href="/dashboard" className="flex-1">
                                        <Button variant="ghost" className="w-full" onClick={() => setIsMenuOpen (false)}>
                                            {t.nav.dashboard}
                                        </Button>
                                    </Link>
                                    <Button variant="outline" className="flex-1" onClick={handleLogout}>
                                        {t.nav.logout}
                                    </Button>
                                </>
                            ) : (
                                <>
                                    <Link href="/login" className="flex-1">
                                        <Button variant="ghost" className="w-full" onClick={() => setIsMenuOpen (false)}>
                                            {t.nav.login}
                                        </Button>
                                    </Link>
                                    <Link href="/register" className="flex-1">
                                        <Button className="w-full" onClick={() => setIsMenuOpen (false)}>
                                            {t.nav.register}
                                        </Button>
                                    </Link>
                                </>
                            )}
                        </div>
                    </nav>
                </div>
            )}
        </header>
    );
};
