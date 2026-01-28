"use client";

export function ToastProvider({ children }: { children: React.ReactNode }) {
    return <>{children}</>;
}

export function ToastViewport() {
    return null;
}

/*export function Toast() {
  return null;
  }*/

export function Toast({
    children,
    ...props
}: React.PropsWithChildren<Record<string, unknown>>) {
    return <div {...props}>{children}</div>;
}

/*export function ToastTitle() {
  return null;
  }*/

export function ToastTitle({
    children,
}: React.PropsWithChildren) {
    return <div>{children}</div>;
}

/*export function ToastDescription() {
  return null;
  }*/

export function ToastDescription({
    children,
}: React.PropsWithChildren) {
    return <div>{children}</div>;
}

export function ToastClose() {
    return null;
}
