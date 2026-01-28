export interface BlogPost {
    slug: string;
    title: {
        it: string;
        en: string;
    };
    excerpt: {
        it: string;
        en: string;
    };
    content: {
        it: string;
        en: string;
    };
    date: string;
    author: string;
}

export const blogPosts: BlogPost[] = [
    {
        slug: "why-graphs-matter",
        title: {
            it: "Perché i grafici sono importanti e cosa possono fare di straordinario",
            en: "Why Graphs Matter — and What They Can Do Tremendously"
        },
        excerpt: {
            it: "Scopri come i database a grafo stanno rivoluzionando il modo in cui gestiamo le relazioni complesse nei dati.",
            en: "Discover how graph databases are revolutionizing the way we handle complex relationships in data."
        },
        content: {
            it: `# Perché i grafici sono importanti

            I database a grafo rappresentano una rivoluzione nel modo in cui modelliamo e interroghiamo le relazioni tra i dati. A differenza dei database relazionali tradizionali, i grafi eccellono nel rappresentare connessioni complesse.

                ## Vantaggi principali

            ### 1. Relazioni naturali
            I grafi permettono di modellare le relazioni in modo intuitivo, esattamente come le concepiamo naturalmente.

                ### 2. Query efficienti
            Le traversate di grafo sono estremamente veloci per query che coinvolgono relazioni multiple.

                ### 3. Flessibilità dello schema
            I grafi permettono di evolvere lo schema senza costose migrazioni.

                ## Applicazioni pratiche

            - **Social Networks**: Modellare amicizie e interazioni
            - **Sistemi di raccomandazione**: Trovare prodotti correlati
            - **Fraud Detection**: Identificare pattern sospetti
            - **Knowledge Graphs**: Costruire basi di conoscenza intelligenti

            ## Conclusione

            I grafi non sono solo una tecnologia, sono un nuovo modo di pensare ai dati e alle loro relazioni.`,
            en: `# Why Graphs Matter

            Graph databases represent a revolution in how we model and query relationships between data. Unlike traditional relational databases, graphs excel at representing complex connections.

                ## Key Advantages

            ### 1. Natural Relationships
            Graphs allow modeling relationships intuitively, exactly as we naturally conceive them.

                ### 2. Efficient Queries
            Graph traversals are extremely fast for queries involving multiple relationships.

                    ### 3. Schema Flexibility
                Graphs allow schema evolution without expensive migrations.

                ## Practical Applications

            - **Social Networks**: Modeling friendships and interactions
            - **Recommendation Systems**: Finding related products
            - **Fraud Detection**: Identifying suspicious patterns
            - **Knowledge Graphs**: Building intelligent knowledge bases

            ## Conclusion

            Graphs are not just a technology, they're a new way of thinking about data and their relationships.`
        },
        date: "2025-12-15",
        author: "Erutalia Team"
    },
    {
        slug: "choosing-databases",
        title: {
            it: "Come scegliere il database giusto per il tuo progetto",
            en: "How to Choose the Right Database for Your Project"
        },
        excerpt: {
            it: "Una guida completa per selezionare il database più adatto alle tue esigenze specifiche.",
            en: "A comprehensive guide to selecting the database that best fits your specific needs."
        },
        content: {
            it: `# Come scegliere il database giusto

            La scelta del database è una delle decisioni architetturali più importanti per qualsiasi progetto software.

                ## Tipi di database

            ### Relazionali (SQL)
            - PostgreSQL, MySQL, SQLite
            - Ideali per dati strutturati con relazioni ben definite
            - ACID compliance

            ### Document (NoSQL)
            - MongoDB, CouchDB
            - Flessibilità dello schema
            - Scalabilità orizzontale

            ### Graph
            - Neo4j, ArangoDB
            - Relazioni complesse
            - Query di traversamento

            ### Vector
            - Pinecone, Weaviate, Qdrant
            - Ricerca semantica
            - AI/ML applications

            ## Criteri di scelta

            1. **Tipo di dati**: Strutturati vs non strutturati
            2. **Scalabilità**: Verticale vs orizzontale
            3. **Consistenza**: ACID vs eventual consistency
            4. **Query patterns**: Letture vs scritture`,
            en: `# How to Choose the Right Database

            Database selection is one of the most important architectural decisions for any software project.

                    ## Database Types

                ### Relational (SQL)
                - PostgreSQL, MySQL, SQLite
                - Ideal for structured data with well-defined relationships
                    - ACID compliance

                ### Document (NoSQL)
                - MongoDB, CouchDB
                - Schema flexibility
                - Horizontal scalability

                ### Graph
                - Neo4j, ArangoDB
                - Complex relationships
                - Traversal queries

                ### Vector
                - Pinecone, Weaviate, Qdrant
                - Semantic search
                - AI/ML applications

                ## Selection Criteria

                1. **Data type**: Structured vs unstructured
                2. **Scalability**: Vertical vs horizontal
                3. **Consistency**: ACID vs eventual consistency
                4. **Query patterns**: Reads vs writes`
        },
        date: "2025-12-10",
        author: "Erutalia Team"
    },
    {
        slug: "getting-started-graph-analytics",
        title: {
            it: "Introduzione all'analisi dei grafi",
            en: "Getting Started with Graph Analytics"
        },
        excerpt: {
            it: "Impara i concetti fondamentali dell'analisi dei grafi e come applicarli ai tuoi progetti.",
            en: "Learn the fundamental concepts of graph analytics and how to apply them to your projects."
        },
        content: {
            it: `# Introduzione all'analisi dei grafi

            L'analisi dei grafi è una disciplina potente che permette di estrarre insight dalle relazioni tra entità.

                ## Concetti fondamentali

            ### Nodi e Archi
            - **Nodi**: Entità nel grafo
            - **Archi**: Relazioni tra entità

            ### Metriche chiave

            1. **Degree Centrality**: Numero di connessioni
            2. **Betweenness Centrality**: Importanza come ponte
            3. **PageRank**: Importanza basata sui link
            4. **Community Detection**: Identificare gruppi

            ## Strumenti consigliati

            - NetworkX (Python)
            - Neo4j Graph Data Science
            - Apache Spark GraphX`,
            en: `# Getting Started with Graph Analytics

            Graph analytics is a powerful discipline that extracts insights from relationships between entities.

                ## Fundamental Concepts

            ### Nodes and Edges
            - **Nodes**: Entities in the graph
            - **Edges**: Relationships between entities

            ### Key Metrics

            1. **Degree Centrality**: Number of connections
            2. **Betweenness Centrality**: Importance as a bridge
            3. **PageRank**: Link-based importance
            4. **Community Detection**: Identifying groups

            ## Recommended Tools

            - NetworkX (Python)
            - Neo4j Graph Data Science
            - Apache Spark GraphX`
        },
        date: "2025-12-05",
        author: "Erutalia Team"
    },
    {
        slug: "high-performance-computing",
        title: {
            it: "Applicazioni del calcolo ad alte prestazioni",
            en: "High Performance Computing Applications"
        },
        excerpt: {
            it: "Esplora come l'HPC sta trasformando la ricerca scientifica e l'industria.",
            en: "Explore how HPC is transforming scientific research and industry."
        },
        content: {
            it: `# Calcolo ad alte prestazioni

            L'High Performance Computing (HPC) è fondamentale per risolvere problemi computazionalmente intensivi.

                ## Applicazioni

            ### Ricerca scientifica
            - Simulazioni climatiche
            - Modellazione molecolare
            - Genomica

            ### Industria
            - CFD (Computational Fluid Dynamics)
            - Crash simulation
            - Rendering 3D

            ### AI/ML
            - Training di modelli large-scale
            - Inference distribuita
            - Data processing

            ## Tecnologie

            - GPU Computing (CUDA, ROCm)
            - Cluster computing
            - MPI/OpenMP`,
            en: `# High Performance Computing

            High Performance Computing (HPC) is fundamental for solving computationally intensive problems.

                    ## Applications

                ### Scientific Research
                - Climate simulations
                - Molecular modeling
                - Genomics

                ### Industry
                - CFD (Computational Fluid Dynamics)
                - Crash simulation
                - 3D Rendering

                ### AI/ML
                - Large-scale model training
                - Distributed inference
                - Data processing

                ## Technologies

                - GPU Computing (CUDA, ROCm)
                - Cluster computing
                - MPI/OpenMP`
        },
        date: "2025-12-01",
        author: "Erutalia Team"
    }
];
