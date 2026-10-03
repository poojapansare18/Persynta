"use client";

import Link from "next/link";
import {
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  Clock,
  MapPin,
  Plus,
  Users,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const events = [
  {
    time: "09:00",
    title: "Submit application",
    type: "Task",
    duration: "30 min",
  },
  {
    time: "15:00",
    title: "Campus AI Discussion",
    type: "Meeting",
    duration: "30 min",
    guests: "Rahul · Priya",
    location: "Google Meet",
  },
  {
    time: "18:00",
    title: "Interview preparation",
    type: "Task",
    duration: "60 min",
  },
];

const weekDays = [
  { day: "Mon", date: 21 },
  { day: "Tue", date: 22 },
  { day: "Wed", date: 23 },
  { day: "Thu", date: 24 },
  { day: "Fri", date: 25 },
  { day: "Sat", date: 26 },
  { day: "Sun", date: 27 },
];

export default function Calendar() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Calendar
          </h1>

          <p className="mt-1 text-sm text-muted-foreground">
            Manage meetings, tasks and reminders.
          </p>
        </div>

        <Link href="/calendar/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            New Meeting
          </Button>
        </Link>
      </div>

      {/* Calendar toolbar */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-2">
              <Button variant="outline" size="icon">
                <ChevronLeft className="h-4 w-4" />
              </Button>

              <Button variant="outline" size="icon">
                <ChevronRight className="h-4 w-4" />
              </Button>

              <h2 className="ml-2 text-lg font-semibold">
                September 2026
              </h2>
            </div>

            <Button variant="outline">
              <CalendarDays className="mr-2 h-4 w-4" />
              Today
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Week */}
      <Card>
        <CardContent className="p-0">
          <div className="grid grid-cols-7 divide-x">
            {weekDays.map((day) => {
              const selected = day.date === 27;

              return (
                <div
                  key={day.date}
                  className={`min-h-20 p-2 text-center sm:p-4 ${
                    selected ? "bg-muted/50" : ""
                  }`}
                >
                  <p className="text-xs text-muted-foreground">
                    {day.day}
                  </p>

                  <div
                    className={`mx-auto mt-2 flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium ${
                      selected
                        ? "bg-black text-white"
                        : "text-foreground"
                    }`}
                  >
                    {day.date}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Selected day */}
      <div>
        <div className="mb-4">
          <h2 className="text-lg font-semibold">
            Sunday, 27 September
          </h2>

          <p className="text-sm text-muted-foreground">
            3 events scheduled
          </p>
        </div>

        <div className="space-y-3">
          {events.map((event) => (
            <Card key={`${event.time}-${event.title}`}>
              <CardContent className="p-4">
                <div className="flex gap-4">
                  {/* Time */}
                  <div className="w-14 shrink-0">
                    <p className="text-sm font-medium">{event.time}</p>

                    <div className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      {event.duration}
                    </div>
                  </div>

                  {/* Event */}
                  <div className="min-w-0 flex-1 border-l pl-4">
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                      <div>
                        <p className="font-medium">{event.title}</p>

                        <p className="mt-1 text-xs text-muted-foreground">
                          {event.type}
                        </p>
                      </div>

                      {event.type === "Meeting" && (
                        <span className="w-fit rounded-full bg-muted px-2.5 py-1 text-xs font-medium">
                          Meeting
                        </span>
                      )}
                    </div>

                    {event.guests && (
                      <div className="mt-3 flex items-center gap-2 text-sm text-muted-foreground">
                        <Users className="h-4 w-4" />
                        {event.guests}
                      </div>
                    )}

                    {event.location && (
                      <div className="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
                        <MapPin className="h-4 w-4" />
                        {event.location}
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}