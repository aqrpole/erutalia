export interface Project {
    id: string;
    name: string;
    type: {
        it: string;
        en: string;
    };
    url: string | null;
    description: {
        it: string;
        en: string;
    };
    highlights: {
        it: string[];
        en: string[];
    };
    previewType: "iframe" | "image";
}

export const projects: Project[] = [
    {
        id: "overseas-one",
        name: "overseas.one",
        type: {
            it: "CSR / Piattaforma Educativa",
            en: "CSR / Education Platform",
        },
        url: "https://overseas.one",
        description: {
            it: "Piattaforma CSR progettata per aiutare gli studenti a trovare borse di studio e opportunità di studio all'estero. Il sistema offre una mappa interattiva delle ammissioni, delle borse di studio e dei programmi accademici, permettendo correlazioni tra diversi dataset.",
            en: "A CSR platform designed to help students find scholarships and study-abroad opportunities. The system provides a live map of admissions, scholarships, and academic programs, enabling correlation across multiple datasets.",
        },
        highlights: {
            it: [
                "Mappa geografica in tempo reale",
                "Correlazione tra borse di studio, ammissioni e istituzioni",
                "Supporto decisionale basato sui dati",
            ],
            en: [
                "Real-time geographic visualization",
                "Data correlation across institutions and programs",
                "Data-driven student guidance",
            ],
        },
        previewType: "iframe",
    },
    {
        id: "nimanpower",
        name: "nimanpower.com",
        type: {
            it: "Piattaforma Industriale / Sistema Database",
            en: "Industry Platform / Database System",
        },
        url: "https://nimanpower.com",
        description: {
            it: "Piattaforma per il settore elettrico che consente a produttori e appaltatori di individuarsi rapidamente all'interno di specifici ambiti industriali.",
            en: "A platform for the electrical industry that enables manufacturers and contractors to discover and connect with each other efficiently.",
        },
        highlights: {
            it: [
                "Database strutturato di settore",
                "Ricerca rapida e filtri avanzati",
                "Ottimizzazione dei flussi operativi",
            ],
            en: [
                "Structured industry database",
                "Fast search and filtering",
                "Operational efficiency by design",
            ],
        },
        previewType: "iframe",
    },
    {
        id: "financial-analytics",
        name: "Financial Analytics Dashboard",
        type: {
            it: "Piattaforma Analitica Enterprise",
            en: "Enterprise Analytics Platform",
        },
        url: null,
        description: {
            it: "Sviluppo e manutenzione di una dashboard analitica cloud per aziende farmaceutiche, utilizzata per il monitoraggio di KPI finanziari e operativi.",
            en: "Development and maintenance of a cloud-based analytics dashboard for large pharmaceutical companies to monitor financial and operational KPIs.",
        },
        highlights: {
            it: [
                "Ingestione mensile dei dati",
                "KPI: margini, ROI, costi, utilizzo chimico",
                "Grafici, mappe e visualizzazioni interattive",
                "Autenticazione sicura con Single Sign-On (SSO)",
            ],
            en: [
                "Monthly data ingestion and processing",
                "KPI monitoring: margins, ROI, costing",
                "Interactive charts, maps, and graphs",
                "Secure authentication with Single Sign-On (SSO)",
            ],
        },
        previewType: "image",
    },
    {
        id: "hpc-simulations",
        name: "HPC Scientific Simulations",
        type: {
            it: "Calcolo Scientifico / High-Performance Computing",
            en: "Scientific Computing / High-Performance Computing",
        },
        url: null,
        description: {
            it: "Simulazioni scientifiche ad alte prestazioni basate su librerie open-source, incluse simulazioni di proteine e modellazione di antenne con metodi FDTD.",
            en: "High-performance scientific simulations using open-source libraries, including protein simulations and antenna modeling with FDTD/FEM methods.",
        },
        highlights: {
            it: [
                "Accuratezza scientifica",
                "Ottimizzazione delle prestazioni numeriche",
                "Pipeline di calcolo per la ricerca",
            ],
            en: [
                "Scientific accuracy",
                "Optimized numerical performance",
                "Research-grade computing pipelines",
            ],
        },
        previewType: "image",
    },
    {
        id: "private-mobile-app",
        name: "Private Mobile Application",
        type: {
            it: "Applicazione Mobile / Piattaforma Dati",
            en: "Mobile Application / Data Platform",
        },
        url: null,
        description: {
            it: "Applicazione mobile privata con progettazione UI/UX, sviluppo backend e deployment su Google Cloud Platform (GCP).",
            en: "A private mobile application involving UI/UX design, backend development, and deployment on Google Cloud Platform (GCP) or similar.",
        },
        highlights: {
            it: [
                "Rilascio APK Android",
                "Funzionalità offline con sincronizzazione dati",
                "Processi ETL per analisi e insight",
                "Documentazione tecnica e manuali utente",
            ],
            en: [
                "Android APK release",
                "Offline functionality with data synchronization",
                "ETL pipelines for insights",
                "Technical documentation and user manuals",
            ],
        },
        previewType: "image",
    },
    {
        id: "erutalia-rag",
        name: "erutalia.com – Private AI / RAG System",
        type: {
            it: "Piattaforma AI Privata",
            en: "Private AI Platform",
        },
        url: "https://erutalia.com",
        description: {
            it: "Sistema privato di Question & Answer e Retrieval-Augmented Generation (RAG) progettato per lavorare su documenti riservati.",
            en: "A private Question & Answer and Retrieval-Augmented Generation (RAG) system designed to work with confidential documents.",
        },
        highlights: {
            it: [
                "Deploy locale o cloud",
                "Stack AI open-source",
                "Architettura orientata alla privacy",
            ],
            en: [
                "Fully local or cloud-based deployment",
                "Open-source AI stack",
                "Privacy-first architecture",
            ],
        },
        previewType: "iframe",
    },
];
