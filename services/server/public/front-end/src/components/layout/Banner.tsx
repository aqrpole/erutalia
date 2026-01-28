"use client";

import * as React      from "react";
import { useState }    from "react";
import { X }           from "lucide-react";
import { config }      from "@/config";
import { useLanguage } from "@/contexts/LanguageContext";

export const Banner: React.FC = () => {
    const [isVisible, setIsVisible] = useState<boolean>(config.banner.visible);
    const { t } = useLanguage ();

    if (!isVisible) return null;

    return (
        <div className="fixed top-0 left-0 right-0 z-50 flex items-center justify-center bg-banner px-4 py-2">
            <span className="text-sm font-medium text-banner-foreground">
                {t.banner.underConstruction}
            </span>
            <button
                onClick={() => setIsVisible (false)}
                className="absolute right-4 p-1 rounded-full hover:bg-warning/20 transition-colors"
                aria-label="Close banner"
            >
                <X className="w-4 h-4 text-banner-foreground" />
            </button>
        </div>
    );
};
