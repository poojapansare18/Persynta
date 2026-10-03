"use client";

import { useMemo, useState } from "react";
import {
  Bell,
  CalendarDays,
  CheckCircle2,
  Clock,
  FileText,
  Phone,
  Search,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type ActivityType =
  | "Call"
  | "Task"
  | "Meeting"
  | "Note";

type Activity = {
  id: number;
  type: ActivityType;
  title: string;
  description: string;
  time: string;
  result: string;
};

const activities: Activity[] = [
  {
    id: 1,
    type: "Call",
    title: "Follow-up call",
    description: 'Submit application — You said "Not yet."',
    time: "Today · 9:05 AM",
    result: "Follow-up scheduled",
  },
  {
    id: 2,
    type: "Meeting",
    title: "Meeting reminder",
    description: "Campus AI Discussion",
    time: "Today · 2:00 PM",
    result: "Meeting at 3:00 PM",
  },
  {
    id: 3,
    type: "Note",
    title: "Note created",
    description: "Interview — Rahul",
    time: "Today · 10:30 AM",
    result: "Saved to memory",
  },
  {
    id: 4,
    type: "Task",
    title: "Task completed",
    description: "Interview preparation",
    time: "Yesterday · 6:20 PM",
    result: "Completed",
  },
];

const filters = [
  "All",
  "Calls",
  "Tasks",
  "Meetings",
  "Notes",
] as const;

type Filter = (typeof filters)[number];

export default function History() {
  const [filter, setFilter] = useState<Filter>("All");
  const [search, setSearch] = useState("");

  const filteredActivities = useMemo(() => {
    const query = search.toLowerCase().trim();

    return activities.filter((activity) => {
      const matchesSearch =
        !query ||
        activity.title.toLowerCase().includes(query) ||
        activity.description.toLowerCase().includes(query) ||
        activity.result.toLowerCase().includes(query);

      if (!matchesSearch) return false;

      if (filter === "All") return true;

      return activity.type === filter.slice(0, -1);
    });
  }, [filter, search]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          History
        </h1>

        <p className="mt-1 text-sm text-muted-foreground">
          See what Persynta did and what happened.
        </p>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

        <Input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search history..."
          className="pl-9"
        />
      </div>

      {/* Filters */}
      <div className="flex gap-2 overflow-x-auto pb-1">
        {filters.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => setFilter(item)}
            className={`rounded-lg border px-3 py-2 text-sm transition ${
              filter === item
                ? "border-black bg-black text-white"
                : "bg-white hover:bg-muted"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      {/* Timeline */}
      <Card>
        <CardContent className="p-5">
          {filteredActivities.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Search className="h-8 w-8 text-muted-foreground" />

              <p className="mt-3 font-medium">
                No activity found
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                Try a different search or filter.
              </p>
            </div>
          ) : (
            <div className="space-y-0">
              {filteredActivities.map((activity, index) => (
                <div
                  key={activity.id}
                  className="flex gap-4"
                >
                  {/* Timeline */}
                  <div className="flex flex-col items-center">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border bg-white">
                      <ActivityIcon type={activity.type} />
                    </div>

                    {index !== filteredActivities.length - 1 && (
                      <div className="h-full min-h-16 w-px bg-border" />
                    )}
                  </div>

                  {/* Content */}
                  <div className="min-w-0 flex-1 pb-7">
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                      <div>
                        <p className="text-sm font-medium">
                          {activity.title}
                        </p>

                        <p className="mt-1 text-sm text-muted-foreground">
                          {activity.description}
                        </p>
                      </div>

                      <span className="shrink-0 text-xs text-muted-foreground">
                        {activity.time}
                      </span>
                    </div>

                    <div className="mt-3 flex flex-wrap items-center gap-2">
                      <Badge variant="outline">
                        {activity.type}
                      </Badge>

                      <span className="text-xs text-muted-foreground">
                        {activity.result}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function ActivityIcon({
  type,
}: {
  type: ActivityType;
}) {
  if (type === "Call") {
    return <Phone className="h-4 w-4" />;
  }

  if (type === "Meeting") {
    return <CalendarDays className="h-4 w-4" />;
  }

  if (type === "Note") {
    return <FileText className="h-4 w-4" />;
  }

  return <CheckCircle2 className="h-4 w-4" />;
}