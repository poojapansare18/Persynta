"use client";

import {
  CalendarDays,
  CheckCircle2,
  Mail,
  MessageCircle,
  Phone,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const integrations = [
  {
    name: "Google Calendar",
    description:
      "Create meetings, check schedules and manage calendar events.",
    icon: CalendarDays,
    status: "Connected",
  },
  {
    name: "WhatsApp",
    description:
      "Receive reminders, meeting confirmations and daily briefings.",
    icon: MessageCircle,
    status: "Connected",
  },
  {
    name: "Email",
    description:
      "Receive meeting invitations, summaries and important notifications.",
    icon: Mail,
    status: "Connected",
  },
  {
    name: "Digital Friend",
    description:
      "Your personal phone number for calling Persynta.",
    icon: Phone,
    status: "Active",
  },
];

export default function Integrations() {
  return (
    <div className="space-y-8">
      <div>
        <p className="text-sm text-muted-foreground">
          Connect Persynta to your everyday tools
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight">
          Integrations
        </h1>
      </div>

      <div className="space-y-4">
        {integrations.map((integration) => {
          const Icon = integration.icon;

          return (
            <Card key={integration.name}>
              <CardContent className="flex flex-col gap-5 p-5 sm:flex-row sm:items-center">
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-muted">
                  <Icon size={21} />
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h2 className="font-medium">
                      {integration.name}
                    </h2>

                    <Badge variant="secondary">
                      <CheckCircle2 />
                      {integration.status}
                    </Badge>
                  </div>

                  <p className="mt-1 text-sm text-muted-foreground">
                    {integration.description}
                  </p>
                </div>

                <Button variant="outline">
                  Manage
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}