"use client";

import React      from "react";
import { Banner } from "./Banner";
import { Header } from "./Header";
import { Footer } from "./Footer";

interface LayoutProps {
    children   : React.ReactNode;
    showBanner?: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, showBanner = true }) => {
    return (
        <div className="min-h-screen flex flex-col">
            {showBanner && <Banner />}
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
        </div>
    );
};
