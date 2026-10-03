"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  CheckSquare,
  CalendarDays,
  NotebookPen,
  MoreHorizontal,
} from "lucide-react";

const links = [
  { label: "Home", href: "/", icon: Home },
  { label: "Tasks", href: "/tasks", icon: CheckSquare },
  { label: "Calendar", href: "/calendar", icon: CalendarDays },
  { label: "Notes", href: "/notes", icon: NotebookPen },
  { label: "More", href: "/settings", icon: MoreHorizontal },
];

export default function MobileNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex border-t bg-white md:hidden">
      {links.map((item) => {
        const Icon = item.icon;

        const active =
          item.href === "/"
            ? pathname === "/"
            : pathname.startsWith(item.href);

        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-1 flex-col items-center gap-1 py-3 text-xs ${
              active ? "text-black" : "text-muted-foreground"
            }`}
          >
            <Icon className="h-5 w-5" />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}