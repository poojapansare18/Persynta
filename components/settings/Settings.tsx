"use client";

import Link from "next/link";
import {
  Bell,
  CalendarDays,
  ChevronRight,
  Mail,
  MessageCircle,
  Phone,
  Shield,
  User,
} from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";

const settingsItems = [
  {
    title: "Profile",
    description: "Manage your personal information.",
    icon: User,
    href: "#",
  },
  {
    title: "Digital Friend",
    description: "Manage your Persynta phone assistant.",
    icon: Phone,
    href: "/settings/digital-friend",
  },
  {
    title: "Integrations",
    description: "Manage Google Calendar, WhatsApp and Email.",
    icon: CalendarDays,
    href: "/settings/integrations",
  },
  {
    title: "Communication Preferences",
    description: "Choose how Persynta should contact you.",
    icon: MessageCircle,
    href: "/settings/notifications",
  },
  {
    title: "Morning Briefing",
    description: "Configure your daily briefing.",
    icon: Bell,
    href: "/settings/morning-briefing",
  },
  {
    title: "Email",
    description: "Manage email notifications.",
    icon: Mail,
    href: "#",
  },
  {
    title: "Privacy",
    description: "Manage your data and privacy settings.",
    icon: Shield,
    href: "#",
  },
];

export default function Settings() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Settings
        </h1>

        <p className="mt-1 text-sm text-muted-foreground">
          Manage your Persynta account and preferences.
        </p>
      </div>

      {/* Settings list */}
      <div className="grid gap-3">
        {settingsItems.map((item) => {
          const Icon = item.icon;

          const content = (
            <Card className="transition hover:border-black">
              <CardContent className="flex items-center gap-4 p-5">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border bg-muted/40">
                  <Icon className="h-5 w-5" />
                </div>

                <div className="min-w-0 flex-1">
                  <p className="font-medium">{item.title}</p>

                  <p className="mt-1 text-sm text-muted-foreground">
                    {item.description}
                  </p>
                </div>

                <ChevronRight className="h-5 w-5 shrink-0 text-muted-foreground" />
              </CardContent>
            </Card>
          );

          if (item.href === "#") {
            return (
              <div key={item.title} className="cursor-pointer">
                {content}
              </div>
            );
          }

          return (
            <Link key={item.title} href={item.href}>
              {content}
            </Link>
          );
        })}
      </div>
    </div>
  );
}