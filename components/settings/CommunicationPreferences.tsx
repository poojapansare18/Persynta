"use client";

import { useState } from "react";
import { Bell, Mail, MessageCircle, Phone, Smartphone } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function CommunicationPreferences() {
  const [preferences, setPreferences] = useState({
    whatsapp: true,
    email: true,
    phone: true,
    push: true,
    taskReminders: true,
    meetingReminders: true,
    followUps: true,
  });

  const toggle = (key: keyof typeof preferences) => {
    setPreferences((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Communication Preferences
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Choose how Persynta should reach you.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Communication channels</CardTitle>
        </CardHeader>

        <CardContent className="divide-y">
          <PreferenceRow
            icon={<MessageCircle className="h-5 w-5" />}
            title="WhatsApp"
            description="Receive confirmations, reminders and updates."
            enabled={preferences.whatsapp}
            onToggle={() => toggle("whatsapp")}
          />

          <PreferenceRow
            icon={<Mail className="h-5 w-5" />}
            title="Email"
            description="Receive important confirmations and summaries."
            enabled={preferences.email}
            onToggle={() => toggle("email")}
          />

          <PreferenceRow
            icon={<Phone className="h-5 w-5" />}
            title="Phone calls"
            description="Let Digital Friend call you for important actions."
            enabled={preferences.phone}
            onToggle={() => toggle("phone")}
          />

          <PreferenceRow
            icon={<Smartphone className="h-5 w-5" />}
            title="Push notifications"
            description="Receive notifications through the Persynta app."
            enabled={preferences.push}
            onToggle={() => toggle("push")}
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">What should Persynta remind you about?</CardTitle>
        </CardHeader>

        <CardContent className="divide-y">
          <PreferenceRow
            icon={<Bell className="h-5 w-5" />}
            title="Task reminders"
            description="Reminders for scheduled tasks."
            enabled={preferences.taskReminders}
            onToggle={() => toggle("taskReminders")}
          />

          <PreferenceRow
            icon={<Bell className="h-5 w-5" />}
            title="Meeting reminders"
            description="Reminders before upcoming meetings."
            enabled={preferences.meetingReminders}
            onToggle={() => toggle("meetingReminders")}
          />

          <PreferenceRow
            icon={<Bell className="h-5 w-5" />}
            title="Follow-ups"
            description="Follow up when something is still pending."
            enabled={preferences.followUps}
            onToggle={() => toggle("followUps")}
          />
        </CardContent>
      </Card>
    </div>
  );
}

function PreferenceRow({
  icon,
  title,
  description,
  enabled,
  onToggle,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  enabled: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="flex items-center justify-between gap-4 py-4">
      <div className="flex items-center gap-3">
        <div className="rounded-lg border bg-muted/40 p-2">
          {icon}
        </div>

        <div>
          <p className="text-sm font-medium">{title}</p>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      </div>

      <button
        type="button"
        onClick={onToggle}
        className={`relative h-6 w-11 rounded-full transition ${
          enabled ? "bg-black" : "bg-muted"
        }`}
        aria-label={`Toggle ${title}`}
      >
        <span
          className={`absolute top-1 h-4 w-4 rounded-full bg-white transition ${
            enabled ? "left-6" : "left-1"
          }`}
        />
      </button>
    </div>
  );
}