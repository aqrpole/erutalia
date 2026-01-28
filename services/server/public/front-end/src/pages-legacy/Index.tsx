import { Layout }           from "@/components/layout/Layout";
import { HeroSection }      from "@/components/home/HeroSection";
import { WhatWeDoSection }  from "@/components/home/WhatWeDoSection";
import { CraftSection }     from "@/components/home/CraftSection";
import { AboutSection }     from "@/components/home/AboutSection";
import { ExpertiseSection } from "@/components/home/ExpertiseSection";
import { BlogSection }      from "@/components/home/BlogSection";
import { ContactSection }   from "@/components/home/ContactSection";

export default function HomePage () {
    return (
        <Layout>
            <HeroSection />
            <WhatWeDoSection />
            <CraftSection />
            <AboutSection />
            <ExpertiseSection />
            <BlogSection />
            <ContactSection />
        </Layout>
    );
};
