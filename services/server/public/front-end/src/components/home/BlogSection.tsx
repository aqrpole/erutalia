"use client";

import Link            from "next/link";
import { ArrowRight }  from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import { blogPosts }   from "@/data/blogPosts";

export function BlogSection () {
    const { t, language } = useLanguage ();
    const displayPosts    = blogPosts.slice (0, 3);

    return (
        <section className="py-24 bg-background">
            <div className="container">
                <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-12 text-center">
                    {t.blog.headline}
                </h2>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {displayPosts.map((post) => (
                        <Link
                            key={post.slug}
                            href={`/blog/${post.slug}`}
                            className="group bg-secondary rounded-lg overflow-hidden card-shadow hover:card-shadow-hover transition-all duration-300"
                        >
                            <div className="aspect-video bg-primary/10 flex items-center justify-center">
                                <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center">
                                    <span className="text-2xl font-display font-bold text-primary">
                                        {post.title[language].charAt(0)}
                                    </span>
                                </div>
                            </div>

                            <div className="p-6">
                                <h3 className="font-display text-xl font-semibold text-foreground mb-3 group-hover:text-primary transition-colors">
                                    {post.title[language]}
                                </h3>
                                <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                                    {post.excerpt[language]}
                                </p>
                                <span className="inline-flex items-center text-sm font-medium text-primary">
                                    {t.blog.readMore}
                                    <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                                </span>
                            </div>
                        </Link>
                    ))}
                </div>

                <div className="text-center mt-12">
                    <Link
                        href="/blog"
                        className="inline-flex items-center text-primary font-medium hover:underline"
                    >
                        View all posts
                        <ArrowRight className="w-4 h-4 ml-1" />
                    </Link>
                </div>
            </div>
        </section>
    );
}
