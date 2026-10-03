"use client";

import Link from "next/link";
import {
  ArrowRight,
  Bell,
  CalendarDays,
  CheckCircle2,
  Clock,
  History,
  Phone,
  Plus,
  Sparkles,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const todayTasks = [
  {
    title: "Submit application",
    time: "5:00 PM",
    status: "Waiting",
  },
  {
    title: "Interview preparation",
    time: "6:00 PM",
    status: "Scheduled",
  },
];

export default function Home() {
  return (
    <div className="space-y-6">
      {/* Welcome */}
      <section>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm text-muted-foreground">
              Sunday, 27 September 2026
            </p>

            <h1 className="mt-1 text-2xl font-semibold tracking-tight">
              Good evening, Pooja.
            </h1>

            <p className="mt-1 text-sm text-muted-foreground">
              Here is what needs your attention today.
            </p>
          </div>

          <Link href="/calendar/new">
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              New Meeting
            </Button>
          </Link>
        </div>
      </section>

      {/* Overview */}
      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <OverviewCard
          icon={<CheckCircle2 className="h-5 w-5" />}
          label="Tasks today"
          value="2"
          detail="1 waiting"
        />

        <OverviewCard
          icon={<CalendarDays className="h-5 w-5" />}
          label="Meetings"
          value="1"
          detail="Next at 3:00 PM"
        />

        <OverviewCard
          icon={<Clock className="h-5 w-5" />}
          label="Follow-ups"
          value="2"
          detail="Need attention"
        />

        <OverviewCard
          icon={<History className="h-5 w-5" />}
          label="Recent activity"
          value="4"
          detail="Since yesterday"
        />
      </section>

      {/* Main content */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Today's focus */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base">
                Today&apos;s focus
              </CardTitle>

              <p className="mt-1 text-sm text-muted-foreground">
                Tasks and meetings that matter today.
              </p>
            </div>

            <Link href="/tasks">
              <Button variant="ghost" size="sm">
                View all
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </CardHeader>

          <CardContent className="space-y-3">
            {todayTasks.map((task) => (
              <div
                key={task.title}
                className="flex items-center justify-between gap-4 rounded-xl border p-4"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                    <CheckCircle2 className="h-4 w-4" />
                  </div>

                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">
                      {task.title}
                    </p>

                    <p className="mt-1 text-xs text-muted-foreground">
                      Today · {task.time}
                    </p>
                  </div>
                </div>

                <Badge variant="outline">{task.status}</Badge>
              </div>
            ))}

            {/* Meeting */}
            <div className="rounded-xl border p-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex min-w-0 gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                    <CalendarDays className="h-4 w-4" />
                  </div>

                  <div>
                    <p className="text-sm font-medium">
                      Campus AI Discussion
                    </p>

                    <p className="mt-1 text-xs text-muted-foreground">
                      Today · 3:00 PM · 30 min
                    </p>

                    <p className="mt-2 text-xs text-muted-foreground">
                      Rahul · Priya · Google Meet
                    </p>
                  </div>
                </div>

                <Badge>Meeting</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Digital Friend */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Digital Friend
            </CardTitle>
          </CardHeader>

          <CardContent>
            <div className="rounded-xl border p-4">
              <div className="flex items-center gap-3">
                <div className="relative flex h-10 w-10 items-center justify-center rounded-full bg-black text-white">
                  <Phone className="h-4 w-4" />

                  <span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full border-2 border-white bg-green-500" />
                </div>

                <div>
                  <p className="text-sm font-medium">
                    Persynta DF
                  </p>

                  <p className="text-xs text-muted-foreground">
                    Active
                  </p>
                </div>
              </div>

              <div className="mt-4">
                <p className="text-xs text-muted-foreground">
                  Your Digital Friend number
                </p>

                <p className="mt-1 text-sm font-medium">
                  +91 XXXXX XXXXX
                </p>
              </div>

              <Button
                variant="outline"
                className="mt-4 w-full"
              >
                <Phone className="mr-2 h-4 w-4" />
                Call Digital Friend
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Follow-ups + Memory */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base">
                Follow-ups
              </CardTitle>

              <p className="mt-1 text-sm text-muted-foreground">
                Things Persynta is waiting on.
              </p>
            </div>

            <Bell className="h-5 w-5 text-muted-foreground" />
          </CardHeader>

          <CardContent className="space-y-3">
            <FollowUp
              title="Submit application"
              detail="You said: Not yet"
              status="Waiting"
            />

            <FollowUp
              title="Project document"
              detail="Follow up tomorrow"
              status="Scheduled"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base">
                Recent memory
              </CardTitle>

              <p className="mt-1 text-sm text-muted-foreground">
                Information Persynta remembers.
              </p>
            </div>

            <Sparkles className="h-5 w-5 text-muted-foreground" />
          </CardHeader>

          <CardContent>
            <div className="rounded-xl border p-4">
              <p className="text-sm font-medium">
                Interview — Rahul
              </p>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Rahul said the interview may focus on AI agents
                and system design.
              </p>

              <p className="mt-3 text-xs text-muted-foreground">
                Added today · From Digital Friend conversation
              </p>
            </div>

            <Link href="/notes">
              <Button
                variant="ghost"
                size="sm"
                className="mt-3 px-0"
              >
                View notes
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function OverviewCard({
  icon,
  label,
  value,
  detail,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <Card>
      <CardContent className="p-5">
        <div className="flex items-center justify-between">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-muted">
            {icon}
          </div>

          <span className="text-xs text-muted-foreground">
            {detail}
          </span>
        </div>

        <p className="mt-4 text-sm text-muted-foreground">
          {label}
        </p>

        <p className="mt-1 text-2xl font-semibold">
          {value}
        </p>
      </CardContent>
    </Card>
  );
}

function FollowUp({
  title,
  detail,
  status,
}: {
  title: string;
  detail: string;
  status: string;
}) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-xl border p-4">
      <div className="min-w-0">
        <p className="text-sm font-medium">{title}</p>

        <p className="mt-1 text-xs text-muted-foreground">
          {detail}
        </p>
      </div>

      <Badge variant="outline">{status}</Badge>
    </div>
  );
}