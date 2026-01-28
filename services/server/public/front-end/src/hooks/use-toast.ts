/* From React APP
 * export function useToast() {
 *  return { toasts: [] };
 }*/

"use client";

import * as React from "react";

export type Toast = {
    id: string;
    title?: React.ReactNode;
    description?: React.ReactNode;
    action?: React.ReactNode;
    variant?: "default" | "destructive";
};

export function useToast () {
    const [toasts] = React.useState<Toast[]>([]);

    return { toasts };
}
