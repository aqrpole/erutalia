// src/lib/runtime.ts
// How to use:
//   import { getApiBaseUrl } from "@/lib/runtime";
//
//   const baseUrl = getApiBaseUrl();

export function getApiBaseUrl () {
    if (process.env.NEXT_PUBLIC_API_BASE_URL) {
        return process.env.NEXT_PUBLIC_API_BASE_URL;
    }

    if (typeof window !== "undefined") {
        return window.location.origin;
    }

    return "";
}
