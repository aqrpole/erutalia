// /middleware.ts
// next.js detects auto
// NOTE:
// Used only for request logging and route guarding.
// Not API proxying. Safe to keep until Next.js fully removes middleware.
// https://nextjs.org/docs/messages/middleware-to-proxy
import { NextResponse }     from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_FILE = /\.(.*)$/;

// Known top-level routes
const KNOWN_ROUTES = [
    "/",
    "/blog",
    "/projects",
    "/login",
    "/register",
    "/dashboard",
    "/privacy",
    "/terms",
    "/product/dicopia-backup-software",
];

export function middleware (request: NextRequest) {
    const { pathname } = request.nextUrl;

    // Ignore Next.js internals & static assets
    if (
        pathname.startsWith("/_next") ||
        pathname.startsWith("/api") ||
    PUBLIC_FILE.test (pathname)
    ) {
        return NextResponse.next ();
    }

    const isKnownRoute = KNOWN_ROUTES.some (
        (route) => pathname === route || pathname.startsWith(`${route}/`)
    );

    if (!isKnownRoute) {
        console.warn ("[404 attempt]", pathname);

        // Optional: send to FastAPI later
        // fetch("https://api.example.com/log/404", {...})
    }

    return NextResponse.next ();
}

