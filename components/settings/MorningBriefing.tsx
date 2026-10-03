"use client";

import { useState } from "react";
import {
  CalendarDays,
  CheckSquare,
  Clock,
  Mail,
  MessageCircle,
  NotebookPen,
  Phone,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function MorningBriefing() {
  const [enabled, setEnabled] = useState(true);
  const [time, setTime] = useState("08:00");

  const [channels, setChannels] = useState({
    whatsapp: true,
    email: false,
    phone: false,
  });

  const [content, setContent] = useState({
    meetings: true,
    tasks: true,
    followUps: true,
    notes: false,
  });

  const toggleChannel = (key: keyof typeof channels) => {
    setChannels((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const toggleContent = (key: keyof typeof content) => {
    setContent((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Morning Briefing
          </h1>

          <p className="mt-1 text-sm text-muted-foreground">
            Start your day with a summary of what needs your attention.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setEnabled(!enabled)}
          className={`relative h-6 w-11 rounded-full transition ${
            enabled ? "bg-black" : "bg-muted"
          }`}
        >
          <span
            className={`absolute top-1 h-4 w-4 rounded-full bg-white transition ${
              enabled ? "left-6" : "left-1"
            }`}
          />
        </button>
      </div>

      <Card className={!enabled ? "opacity-50" : ""}>
        <CardHeader>
          <CardTitle className="text-base">Delivery time</CardTitle>
        </CardHeader>

        <CardContent>
          <div className="flex max-w-xs items-center gap-3">
            <Clock className="h-5 w-5 text-muted-foreground" />

            <Input
              type="time"
              value={time}
              disabled={!enabled}
              onChange={(e) => setTime(e.target.value)}
            />
          </div>

          <p className="mt-2 text-xs text-muted-foreground">
            Persynta will prepare your briefing every day at this time.
          </p>
        </CardContent>
      </Card>

      <Card className={!enabled ? "opacity-50" : ""}>
        <CardHeader>
          <CardTitle className="text-base">Send briefing through</CardTitle>
        </CardHeader>

        <CardContent className="grid gap-3 sm:grid-cols-3">
          <ChannelButton
            icon={<MessageCircle className="h-5 w-5" />}
            title="WhatsApp"
            selected={channels.whatsapp}
            disabled={!enabled}
            onClick={() => toggleChannel("whatsapp")}
          />

          <ChannelButton
            icon={<Mail className="h-5 w-5" />}
            title="Email"
            selected={channels.email}
            disabled={!enabled}
            onClick={() => toggleChannel("email")}
          />

          <ChannelButton
            icon={<Phone className="h-5 w-5" />}
            title="Phone call"
            selected={channels.phone}
            disabled={!enabled}
            onClick={() => toggleChannel("phone")}
          />
        </CardContent>
      </Card>

      <Card className={!enabled ? "opacity-50" : ""}>
        <CardHeader>
          <CardTitle className="text-base">
            Include in my briefing
          </CardTitle>
        </CardHeader>

        <CardContent className="grid gap-3 sm:grid-cols-2">
          <BriefingItem
            icon={<CalendarDays className="h-5 w-5" />}
            title="Today's meetings"
            selected={content.meetings}
            disabled={!enabled}
            onClick={() => toggleContent("meetings")}
          />

          <BriefingItem
            icon={<CheckSquare className="h-5 w-5" />}
            title="Tasks due today"
            selected={content.tasks}
            disabled={!enabled}
            onClick={() => toggleContent("tasks")}
          />

          <BriefingItem
            icon={<Clock className="h-5 w-5" />}
            title="Pending follow-ups"
            selected={content.followUps}
            disabled={!enabled}
            onClick={() => toggleContent("followUps")}
          />

          <BriefingItem
            icon={<NotebookPen className="h-5 w-5" />}
            title="Important notes"
            selected={content.notes}
            disabled={!enabled}
            onClick={() => toggleContent("notes")}
          />
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button disabled={!enabled}>Save preferences</Button>
      </div>
    </div>
  );
}

function ChannelButton({
  icon,
  title,
  selected,
  disabled,
  onClick,
}: {
  icon: React.ReactNode;
  title: string;
  selected: boolean;
  disabled: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`flex items-center gap-3 rounded-xl border p-4 text-left transition ${
        selected
          ? "border-black bg-black text-white"
          : "bg-white hover:bg-muted/40"
      }`}
    >
      {icon}
      <span className="text-sm font-medium">{title}</span>
    </button>
  );
}

function BriefingItem({
  icon,
  title,
  selected,
  disabled,
  onClick,
}: {
  icon: React.ReactNode;
  title: string;
  selected: boolean;
  disabled: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`flex items-center justify-between rounded-xl border p-4 text-left transition ${
        selected ? "border-black bg-muted/40" : "bg-white"
      }`}
    >
      <div className="flex items-center gap-3">
        {icon}
        <span className="text-sm font-medium">{title}</span>
      </div>

      <div
        className={`flex h-5 w-5 items-center justify-center rounded-full border ${
          selected ? "border-black bg-black text-white" : ""
        }`}
      >
        {selected && <span className="text-xs">✓</span>}
      </div>
    </button>
  );
}