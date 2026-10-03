"use client";

import { useMemo, useState } from "react";
import {
  Check,
  Clock,
  MoreHorizontal,
  Plus,
  RotateCcw,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

type TaskStatus = "Scheduled" | "Waiting" | "Completed";

type Task = {
  id: number;
  title: string;
  time: string;
  status: TaskStatus;
  followUp: boolean;
};

const initialTasks: Task[] = [
  {
    id: 1,
    title: "Submit application",
    time: "Today · 5:00 PM",
    status: "Waiting",
    followUp: true,
  },
  {
    id: 2,
    title: "Prepare interview questions",
    time: "Tomorrow · 10:00 AM",
    status: "Scheduled",
    followUp: false,
  },
  {
    id: 3,
    title: "Send project document",
    time: "28 Sep · 11:30 AM",
    status: "Scheduled",
    followUp: true,
  },
];

const filters = [
  "All",
  "Today",
  "Upcoming",
  "Pending",
  "Completed",
] as const;

type Filter = (typeof filters)[number];

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [filter, setFilter] = useState<Filter>("All");

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      if (filter === "All") return true;

      if (filter === "Completed") {
        return task.status === "Completed";
      }

      if (filter === "Pending") {
        return task.status === "Waiting";
      }

      if (filter === "Today") {
        return task.time.startsWith("Today");
      }

      if (filter === "Upcoming") {
        return !task.time.startsWith("Today") &&
          task.status !== "Completed";
      }

      return true;
    });
  }, [tasks, filter]);

  const completeTask = (id: number) => {
    setTasks((current) =>
      current.map((task) =>
        task.id === id
          ? { ...task, status: "Completed" }
          : task
      )
    );
  };

  const reopenTask = (id: number) => {
    setTasks((current) =>
      current.map((task) =>
        task.id === id
          ? { ...task, status: "Scheduled" }
          : task
      )
    );
  };

  const snoozeTask = (id: number) => {
    setTasks((current) =>
      current.map((task) =>
        task.id === id
          ? {
              ...task,
              time: "Tomorrow · 10:00 AM",
              status: "Scheduled",
            }
          : task
      )
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Tasks
          </h1>

          <p className="mt-1 text-sm text-muted-foreground">
            Manage tasks, reminders and follow-through.
          </p>
        </div>

        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 overflow-x-auto pb-1">
        {filters.map((item) => (
          <Button
            key={item}
            variant={filter === item ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter(item)}
          >
            {item}
          </Button>
        ))}
      </div>

      {/* Tasks */}
      <div className="space-y-3">
        {filteredTasks.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12 text-center">
              <Check className="h-8 w-8 text-muted-foreground" />

              <p className="mt-3 font-medium">
                No tasks here
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                Nothing matches the current filter.
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredTasks.map((task) => (
            <Card key={task.id}>
              <CardContent className="p-4">
                <div className="flex items-center gap-4">
                  {/* Status */}
                  <button
                    type="button"
                    onClick={() =>
                      task.status === "Completed"
                        ? reopenTask(task.id)
                        : completeTask(task.id)
                    }
                    className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border transition ${
                      task.status === "Completed"
                        ? "border-black bg-black text-white"
                        : "hover:bg-muted"
                    }`}
                    aria-label={
                      task.status === "Completed"
                        ? "Reopen task"
                        : "Complete task"
                    }
                  >
                    {task.status === "Completed" && (
                      <Check className="h-4 w-4" />
                    )}
                  </button>

                  {/* Details */}
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <p
                        className={`text-sm font-medium ${
                          task.status === "Completed"
                            ? "text-muted-foreground line-through"
                            : ""
                        }`}
                      >
                        {task.title}
                      </p>

                      {task.followUp && (
                        <Badge variant="outline">
                          Follow-up
                        </Badge>
                      )}
                    </div>

                    <div className="mt-1 flex items-center gap-1.5 text-xs text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      {task.time}
                    </div>
                  </div>

                  {/* Status */}
                  <Badge
                    variant={
                      task.status === "Completed"
                        ? "default"
                        : "outline"
                    }
                    className="hidden sm:inline-flex"
                  >
                    {task.status}
                  </Badge>

                  {/* Actions */}
                  {task.status !== "Completed" && (
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => snoozeTask(task.id)}
                        title="Snooze"
                      >
                        <RotateCcw className="h-4 w-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        size="icon"
                        title="More"
                      >
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}