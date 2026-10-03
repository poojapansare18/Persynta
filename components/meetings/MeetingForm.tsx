"use client";

import { useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CalendarDays,
  CheckCircle2,
  Clock,
  Mail,
  MapPin,
  Users,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

type Guest = {
  id: number;
  name: string;
  email: string;
};

const availableGuests: Guest[] = [
  {
    id: 1,
    name: "Rahul",
    email: "rahul@example.com",
  },
  {
    id: 2,
    name: "Priya",
    email: "priya@example.com",
  },
];

export default function MeetingForm() {
  const [showReview, setShowReview] = useState(false);
  const [scheduled, setScheduled] = useState(false);

  const [agenda, setAgenda] = useState("Campus AI Discussion");
  const [date, setDate] = useState("2026-09-27");
  const [time, setTime] = useState("15:00");
  const [duration, setDuration] = useState("30");
  const [notes, setNotes] = useState("");

  const [selectedGuests, setSelectedGuests] = useState<Guest[]>([
    availableGuests[0],
    availableGuests[1],
  ]);

  const toggleGuest = (guest: Guest) => {
    const exists = selectedGuests.some(
      (item) => item.id === guest.id
    );

    if (exists) {
      setSelectedGuests((current) =>
        current.filter((item) => item.id !== guest.id)
      );
    } else {
      setSelectedGuests((current) => [...current, guest]);
    }
  };

  const formatDate = () => {
    return new Date(`${date}T00:00:00`).toLocaleDateString(
      "en-US",
      {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
      }
    );
  };

  const formatTime = () => {
    return new Date(`2026-01-01T${time}`).toLocaleTimeString(
      "en-US",
      {
        hour: "numeric",
        minute: "2-digit",
      }
    );
  };

  const endTime = () => {
    const [hours, minutes] = time.split(":").map(Number);

    const start = new Date();
    start.setHours(hours, minutes, 0, 0);
    start.setMinutes(start.getMinutes() + Number(duration));

    return start.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
    });
  };

  if (scheduled) {
    return (
      <div className="mx-auto max-w-2xl">
        <Card>
          <CardContent className="flex flex-col items-center px-6 py-12 text-center">
            <div className="flex h-14 w-14 items-center justify-center rounded-full bg-black text-white">
              <CheckCircle2 className="h-7 w-7" />
            </div>

            <h1 className="mt-5 text-2xl font-semibold">
              Meeting scheduled
            </h1>

            <p className="mt-2 max-w-md text-sm text-muted-foreground">
              Your meeting has been added to your calendar.
              Invitations will be sent to the selected guests.
            </p>

            <div className="mt-6 w-full rounded-xl border p-5 text-left">
              <p className="font-medium">{agenda}</p>

              <p className="mt-2 text-sm text-muted-foreground">
                {formatDate()}
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                {formatTime()} – {endTime()}
              </p>

              <p className="mt-3 text-sm text-muted-foreground">
                {selectedGuests.length} guest
                {selectedGuests.length === 1 ? "" : "s"}
              </p>
            </div>

            <div className="mt-6 flex gap-3">
              <Link href="/calendar">
                <Button>View Calendar</Button>
              </Link>

              <Link href="/">
                <Button variant="outline">Go Home</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (showReview) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        {/* Header */}
        <div>
          <Button
            variant="ghost"
            className="mb-3 px-0"
            onClick={() => setShowReview(false)}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Change details
          </Button>

          <h1 className="text-2xl font-semibold tracking-tight">
            Review meeting
          </h1>

          <p className="mt-1 text-sm text-muted-foreground">
            Check the details before Persynta schedules it.
          </p>
        </div>

        {/* Review */}
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between gap-4">
              <div>
                <CardTitle>{agenda}</CardTitle>

                <Badge className="mt-2">
                  Ready to schedule
                </Badge>
              </div>

              <CalendarDays className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>

          <CardContent className="space-y-5">
            <ReviewRow
              icon={<CalendarDays className="h-4 w-4" />}
              label="Date"
              value={formatDate()}
            />

            <ReviewRow
              icon={<Clock className="h-4 w-4" />}
              label="Time"
              value={`${formatTime()} – ${endTime()} (${duration} min)`}
            />

            <div>
              <div className="flex items-center gap-2 text-sm font-medium">
                <Users className="h-4 w-4" />
                Guests
              </div>

              <div className="mt-3 space-y-2">
                {selectedGuests.map((guest) => (
                  <div
                    key={guest.id}
                    className="rounded-lg border p-3"
                  >
                    <p className="text-sm font-medium">
                      {guest.name}
                    </p>

                    <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                      <Mail className="h-3 w-3" />
                      {guest.email}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <ReviewRow
              icon={<MapPin className="h-4 w-4" />}
              label="Location"
              value="Google Meet"
            />

            {notes && (
              <div>
                <p className="text-sm font-medium">
                  Meeting notes
                </p>

                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  {notes}
                </p>
              </div>
            )}

            <div className="rounded-lg bg-muted/50 p-4 text-sm text-muted-foreground">
              After confirmation, Persynta will create the
              calendar event and send invitations to the selected
              guests.
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <Button
            variant="outline"
            onClick={() => setShowReview(false)}
          >
            Change
          </Button>

          <Button onClick={() => setScheduled(true)}>
            <CheckCircle2 className="mr-2 h-4 w-4" />
            Confirm & Schedule
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      {/* Header */}
      <div>
        <Link href="/calendar">
          <Button variant="ghost" className="mb-3 px-0">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to calendar
          </Button>
        </Link>

        <h1 className="text-2xl font-semibold tracking-tight">
          New Meeting
        </h1>

        <p className="mt-1 text-sm text-muted-foreground">
          Create a meeting with Persynta.
        </p>
      </div>

      {/* Form */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Meeting details
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">
          {/* Agenda */}
          <div className="space-y-2">
            <label className="text-sm font-medium">
              Agenda
            </label>

            <Input
              value={agenda}
              onChange={(e) => setAgenda(e.target.value)}
              placeholder="What is this meeting about?"
            />
          </div>

          {/* Date + Time */}
          <div className="grid gap-5 sm:grid-cols-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">
                Date
              </label>

              <Input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">
                Time
              </label>

              <Input
                type="time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
              />
            </div>
          </div>

          {/* Duration */}
          <div className="space-y-2">
            <label className="text-sm font-medium">
              Duration
            </label>

            <select
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              className="flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm"
            >
              <option value="15">15 minutes</option>
              <option value="30">30 minutes</option>
              <option value="45">45 minutes</option>
              <option value="60">1 hour</option>
              <option value="90">1 hour 30 minutes</option>
              <option value="120">2 hours</option>
            </select>
          </div>

          {/* Guests */}
          <div className="space-y-2">
            <label className="text-sm font-medium">
              Guests
            </label>

            <div className="space-y-2">
              {availableGuests.map((guest) => {
                const selected = selectedGuests.some(
                  (item) => item.id === guest.id
                );

                return (
                  <button
                    key={guest.id}
                    type="button"
                    onClick={() => toggleGuest(guest)}
                    className={`flex w-full items-center justify-between rounded-lg border p-3 text-left transition ${
                      selected
                        ? "border-black bg-muted/40"
                        : "hover:bg-muted/30"
                    }`}
                  >
                    <div>
                      <p className="text-sm font-medium">
                        {guest.name}
                      </p>

                      <p className="mt-1 text-xs text-muted-foreground">
                        {guest.email}
                      </p>
                    </div>

                    {selected && (
                      <CheckCircle2 className="h-5 w-5" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Calendar */}
          <div className="rounded-xl border p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <CalendarDays className="h-5 w-5" />

                <div>
                  <p className="text-sm font-medium">
                    Google Calendar
                  </p>

                  <p className="text-xs text-muted-foreground">
                    Connected
                  </p>
                </div>
              </div>

              <Badge>Connected</Badge>
            </div>
          </div>

          {/* Notes */}
          <div className="space-y-2">
            <label className="text-sm font-medium">
              Meeting notes
              <span className="ml-1 text-muted-foreground">
                (optional)
              </span>
            </label>

            <Textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Add context or anything Persynta should remember..."
              rows={4}
            />
          </div>
        </CardContent>
      </Card>

      {/* Review */}
      <div className="flex justify-end">
        <Button
          disabled={!agenda.trim() || selectedGuests.length === 0}
          onClick={() => setShowReview(true)}
        >
          Review Meeting
        </Button>
      </div>
    </div>
  );
}

function ReviewRow({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-start gap-3">
      <div className="mt-0.5 text-muted-foreground">
        {icon}
      </div>

      <div>
        <p className="text-xs text-muted-foreground">
          {label}
        </p>

        <p className="mt-1 text-sm font-medium">
          {value}
        </p>
      </div>
    </div>
  );
}