import React           from "react";
import { Layout }      from "@/components/layout/Layout";
import { useLanguage } from "@/contexts/LanguageContext";
import { Button }      from "@/components/ui/button";
import { config }      from "@/config";
import {
  XCircle,
  AlertTriangle,
  Headphones,
  Eye,
  RefreshCw,
  Monitor,
  Settings,
  Zap,
  Shield,
  Lock,
  FileCheck,
  Database,
  Download,
  Mail,
  ChevronDown,
  Check,
} from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import dicopiaScreenshots from "@/assets/dicopia-screenshots.png";
import dicopiaHeroBg from "@/assets/dicopia-hero-bg.jpg";
import Link            from "next/link";

const NotFound = () => {
    return (
        <div className="flex min-h-screen items-center justify-center bg-muted">
            <div className="text-center">
                <h1 className="mb-4 text-4xl font-bold">Dicopia Backup software Page</h1>
                <Link href="/" className="text-primary underline hover:text-primary/90">
                    Return to Home
                </Link>
            </div>
        </div>
    );
};

export default NotFound;
