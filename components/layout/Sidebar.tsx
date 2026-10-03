"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  CheckSquare,
  CalendarDays,
  NotebookPen,
  History,
  Settings,
} from "lucide-react";

const mainLinks = [
  { label: "Home", href: "/", icon: Home },
  { label: "Tasks", href: "/tasks", icon: CheckSquare },
  { label: "Calendar", href: "/calendar", icon: CalendarDays },
  { label: "Notes", href: "/notes", icon: NotebookPen },
  { label: "History", href: "/history", icon: History },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 hidden h-screen w-60 flex-col border-r bg-white md:flex">
      <div className="flex h-16 items-center border-b px-6">
        <Link href="/" className="text-xl font-semibold tracking-tight">
          Persynta
        </Link>
      </div>

      <nav className="flex-1 space-y-1 p-3">
        {mainLinks.map((item) => {
          const Icon = item.icon;
          const active =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                active
                  ? "bg-black text-white"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t p-3">
        <Link
          href="/settings"
          className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
            pathname.startsWith("/settings")
              ? "bg-black text-white"
              : "text-muted-foreground hover:bg-muted hover:text-foreground"
          }`}
        >
          <Settings className="h-4 w-4" />
          Settings
        </Link>
      </div>
    </aside>
  );
}