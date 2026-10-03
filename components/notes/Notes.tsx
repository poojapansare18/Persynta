"use client";

import { useMemo, useState } from "react";
import {
  Brain,
  CalendarDays,
  FileText,
  Plus,
  Search,
  Star,
  User,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type Note = {
  id: number;
  title: string;
  content: string;
  date: string;
  source: "Written" | "Digital Friend";
  important: boolean;
  memory: boolean;
};

const initialNotes: Note[] = [
  {
    id: 1,
    title: "Interview — Rahul",
    content:
      "Rahul said the interview may focus on AI agents and system design.",
    date: "Today",
    source: "Digital Friend",
    important: true,
    memory: true,
  },
  {
    id: 2,
    title: "Campus AI Architecture",
    content:
      "Campus AI should support students, teachers and administration through one system.",
    date: "Yesterday",
    source: "Written",
    important: true,
    memory: false,
  },
  {
    id: 3,
    title: "Dubai Job Search",
    content:
      "Research AI agent and automation opportunities and prepare for international interviews.",
    date: "24 Sep",
    source: "Written",
    important: false,
    memory: false,
  },
];

const filters = [
  "All",
  "Recent",
  "Important",
  "Memory",
] as const;

type Filter = (typeof filters)[number];

export default function Notes() {
  const [notes, setNotes] = useState<Note[]>(initialNotes);
  const [filter, setFilter] = useState<Filter>("All");
  const [search, setSearch] = useState("");

  const filteredNotes = useMemo(() => {
    const query = search.toLowerCase().trim();

    return notes.filter((note) => {
      const matchesSearch =
        !query ||
        note.title.toLowerCase().includes(query) ||
        note.content.toLowerCase().includes(query);

      if (!matchesSearch) return false;

      if (filter === "All") return true;

      if (filter === "Important") {
        return note.important;
      }

      if (filter === "Memory") {
        return note.memory;
      }

      if (filter === "Recent") {
        return note.date === "Today" || note.date === "Yesterday";
      }

      return true;
    });
  }, [notes, filter, search]);

  const toggleImportant = (id: number) => {
    setNotes((current) =>
      current.map((note) =>
        note.id === id
          ? { ...note, important: !note.important }
          : note
      )
    );
  };

  const toggleMemory = (id: number) => {
    setNotes((current) =>
      current.map((note) =>
        note.id === id
          ? { ...note, memory: !note.memory }
          : note
      )
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Notes & Memory
          </h1>

          <p className="mt-1 text-sm text-muted-foreground">
            Save information and let Persynta remember what matters.
          </p>
        </div>

        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Note
        </Button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search notes and memory..."
          className="pl-9"
        />
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

      {/* Results */}
      <div className="grid gap-4 lg:grid-cols-2">
        {filteredNotes.length === 0 ? (
          <Card className="lg:col-span-2">
            <CardContent className="flex flex-col items-center justify-center py-12 text-center">
              <Search className="h-8 w-8 text-muted-foreground" />

              <p className="mt-3 font-medium">
                No notes found
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                Try another search or filter.
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredNotes.map((note) => (
            <Card key={note.id}>
              <CardContent className="p-5">
                {/* Top */}
                <div className="flex items-start justify-between gap-4">
                  <div className="flex min-w-0 gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                      {note.memory ? (
                        <Brain className="h-4 w-4" />
                      ) : (
                        <FileText className="h-4 w-4" />
                      )}
                    </div>

                    <div className="min-w-0">
                      <p className="font-medium">{note.title}</p>

                      <div className="mt-1 flex flex-wrap items-center gap-2">
                        <span className="text-xs text-muted-foreground">
                          {note.date}
                        </span>

                        <span className="text-xs text-muted-foreground">
                          ·
                        </span>

                        <span className="text-xs text-muted-foreground">
                          {note.source}
                        </span>
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => toggleImportant(note.id)}
                    className="shrink-0"
                    aria-label="Toggle important"
                  >
                    <Star
                      className={`h-5 w-5 ${
                        note.important
                          ? "fill-black text-black"
                          : "text-muted-foreground"
                      }`}
                    />
                  </button>
                </div>

                {/* Content */}
                <p className="mt-4 text-sm leading-6 text-muted-foreground">
                  {note.content}
                </p>

                {/* Tags */}
                <div className="mt-4 flex flex-wrap gap-2">
                  {note.memory && (
                    <Badge variant="outline">
                      <Brain className="mr-1 h-3 w-3" />
                      Memory
                    </Badge>
                  )}

                  <Badge variant="outline">
                    {note.source === "Digital Friend" ? (
                      <>
                        <User className="mr-1 h-3 w-3" />
                        Conversation
                      </>
                    ) : (
                      <>
                        <FileText className="mr-1 h-3 w-3" />
                        Note
                      </>
                    )}
                  </Badge>
                </div>

                {/* Actions */}
                <div className="mt-4 flex items-center justify-between border-t pt-4">
                  <button
                    type="button"
                    onClick={() => toggleMemory(note.id)}
                    className="text-xs font-medium hover:underline"
                  >
                    {note.memory
                      ? "Remove from memory"
                      : "Remember this"}
                  </button>

                  <span className="flex items-center gap-1 text-xs text-muted-foreground">
                    <CalendarDays className="h-3 w-3" />
                    {note.date}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}