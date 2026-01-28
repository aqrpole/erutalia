"use client";

import React, { createContext, useContext,
    useState, useCallback, useMemo }       from "react";
import { translations }                    from "@/i18n/translations";
import { config, type Language }           from "@/config";

const STORAGE_PREFIX = "erutalia:";

type TranslationType = typeof translations.it | typeof translations.en;

interface LanguageContextType {
    language   : Language;
    setLanguage: (lang: Language) => void;
    t          : TranslationType;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [language, setLanguageState] = useState<Language>(() => {
        if (typeof window === "undefined")
            return config.defaultLanguage;
        return (
            (localStorage.getItem (`${STORAGE_PREFIX}language`) as Language) ||
                config.defaultLanguage
        );
    });

    const setLanguage = useCallback ((lang: Language) => {
        setLanguageState (lang);

        if (typeof document !== "undefined")
            document.documentElement.lang = lang;

        if (typeof window !== "undefined")
            localStorage.setItem (`${STORAGE_PREFIX}language`, lang);
    }, []);

    const t = useMemo (() => translations[language], [language]);

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
        {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => {
    const context = useContext (LanguageContext);
    if (!context) {
        throw new Error ("useLanguage must be used within a LanguageProvider");
    }
    return context;
};
